import os
import random
import time
import threading
from flask import Flask, render_template, request, jsonify
from werkzeug.middleware.proxy_fix import ProxyFix
from models import db, TrafficLog, FogStats
from cloud import CloudServer
from fog import FogNode
from edge_simulator import EdgeDevice, create_sample_devices

app = Flask(__name__)

# Generate .env file if missing
if not os.path.exists('.env'):
    with open('.env', 'w') as f:
        f.write('# Auto-generated on first run\n')
        f.write('DATABASE_URL=sqlite:///traffic_monitoring.db\n')
        f.write('SESSION_SECRET=dev_secret_key_change_in_production\n')
    print("✓ Auto-generated .env file (using SQLite for local development)")

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Use SQLite for local development if DATABASE_URL not set or is None
database_url = os.environ.get("DATABASE_URL")
if not database_url or database_url == "None":
    database_url = "sqlite:///traffic_monitoring.db"
    print("✓ Using SQLite database for local development")
else:
    print(f"✓ Using configured database: {database_url.split('@')[0] if '@' in database_url else database_url}")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

db.init_app(app)

with app.app_context():
    db.create_all()
    print("✓ Database tables created successfully")

cloud_server = CloudServer(db)
fog_node = FogNode("FOG_NODE_CENTRAL", db)
edge_devices = create_sample_devices()

console_logs = []


def add_console_log(message, log_type="info"):
    """
    Add a message to console logs for display in UI
    
    Args:
        message (str): Log message
        log_type (str): Type of log (info, success, warning, error)
    """
    from datetime import datetime
    timestamp = datetime.now().strftime("%H:%M:%S")
    console_logs.append({
        "timestamp": timestamp,
        "message": message,
        "type": log_type
    })
    if len(console_logs) > 100:
        console_logs.pop(0)


@app.route('/')
def index():
    """
    Main dashboard page
    Displays the Fog + Edge Computing architecture visualization
    """
    return render_template('index.html')


@app.route('/edge/send-data', methods=['POST'])
def edge_send_data():
    """
    Edge Layer Endpoint
    Simulates edge device generating and sending traffic data to fog layer
    
    Flow: Edge Device → Fog Node
    """
    try:
        edge_device = random.choice(edge_devices)
        
        edge_data = edge_device.generate_traffic_data()
        
        add_console_log(
            f"[EDGE] {edge_device.device_id} generated data: {edge_data['vehicle_count']} vehicles at {edge_data['location']}", 
            "info"
        )
        
        edge_to_fog_latency = random.randint(10, 30)
        time.sleep(edge_to_fog_latency / 1000)
        
        add_console_log(
            f"[LATENCY] Edge → Fog: {edge_to_fog_latency}ms", 
            "success"
        )
        
        fog_result = fog_node.process_edge_data(edge_data)
        
        add_console_log(
            f"[FOG] Processing complete. Congestion: {fog_result['data']['congestion_level']}", 
            "info"
        )
        
        cloud_response = None
        fog_to_cloud_latency = 0
        
        if fog_result['send_to_cloud']:
            fog_to_cloud_latency = random.randint(50, 100)
            time.sleep(fog_to_cloud_latency / 1000)
            
            add_console_log(
                f"[LATENCY] Fog → Cloud: {fog_to_cloud_latency}ms", 
                "warning"
            )
            
            cloud_response = cloud_server.store_data(fog_result['data'])
            
            add_console_log(
                f"[CLOUD] Data stored. Action: {cloud_response['analytics']['action_required']}", 
                "warning"
            )
        else:
            add_console_log(
                f"[FOG] Traffic normal. Handled locally. Cloud processing NOT needed!", 
                "success"
            )
        
        total_latency = edge_to_fog_latency + fog_to_cloud_latency
        
        return jsonify({
            "status": "success",
            "edge_data": edge_data,
            "fog_result": fog_result,
            "cloud_response": cloud_response,
            "latency": {
                "edge_to_fog_ms": edge_to_fog_latency,
                "fog_to_cloud_ms": fog_to_cloud_latency,
                "total_ms": total_latency
            },
            "flow": "Edge → Fog → Cloud" if fog_result['send_to_cloud'] else "Edge → Fog (Local)"
        })
        
    except Exception as e:
        add_console_log(f"[ERROR] {str(e)}", "error")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/fog/process', methods=['POST'])
def fog_process():
    """
    Fog Layer Endpoint
    Processes data at fog layer
    
    This endpoint can be called directly for testing fog processing
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400
        
        result = fog_node.process_edge_data(data)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/cloud/store', methods=['POST'])
def cloud_store():
    """
    Cloud Layer Endpoint
    Stores and analyzes data at cloud layer
    
    This endpoint can be called directly for testing cloud storage
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400
        
        result = cloud_server.store_data(data)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Get statistics from all layers
    """
    try:
        fog_stats = fog_node.get_stats()
        cloud_stats = cloud_server.get_analytics_summary()
        
        edge_stats = [device.get_device_info() for device in edge_devices]
        
        return jsonify({
            "status": "success",
            "edge": edge_stats,
            "fog": fog_stats,
            "cloud": cloud_stats
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/logs', methods=['GET'])
def get_logs():
    """
    Get console logs for UI display
    """
    return jsonify({
        "status": "success",
        "logs": console_logs
    })


@app.route('/api/clear-logs', methods=['POST'])
def clear_logs():
    """
    Clear console logs and database records
    """
    global console_logs
    console_logs = []
    
    try:
        # Delete all traffic logs and fog stats from database
        TrafficLog.query.delete()
        FogStats.query.delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
    return jsonify({
        "status": "success",
        "message": "Logs and data cleared"
    })


@app.route('/api/locations', methods=['GET'])
def get_locations():
    """
    Get all unique locations from traffic logs
    Used for location-based filtering dropdown
    """
    try:
        locations = db.session.query(TrafficLog.location).distinct().all()
        location_list = [loc[0] for loc in locations if loc[0]]
        
        return jsonify({
            "status": "success",
            "locations": sorted(location_list)
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/location-stats/<location>', methods=['GET'])
def get_location_stats(location):
    """
    Get statistics for a specific location
    Returns vehicle count, congestion levels, and trends
    """
    try:
        logs = TrafficLog.query.filter_by(location=location).order_by(TrafficLog.timestamp.desc()).limit(20).all()
        logs.reverse()
        
        if not logs:
            return jsonify({
                "status": "success",
                "location": location,
                "data": {
                    "labels": [],
                    "vehicle_counts": [],
                    "congestion_levels": [],
                    "avg_congestion": "N/A",
                    "peak_vehicles": 0,
                    "total_readings": 0
                }
            })
        
        vehicle_counts = [log.vehicle_count for log in logs]
        congestion_levels = [log.congestion_level for log in logs]
        
        high_count = congestion_levels.count('High')
        avg_congestion = f"{(high_count / len(congestion_levels) * 100):.1f}%"
        
        location_stats = {
            "labels": [log.timestamp.strftime("%H:%M:%S") for log in logs],
            "vehicle_counts": vehicle_counts,
            "congestion_levels": congestion_levels,
            "avg_congestion": avg_congestion,
            "peak_vehicles": max(vehicle_counts) if vehicle_counts else 0,
            "total_readings": len(logs)
        }
        
        return jsonify({
            "status": "success",
            "location": location,
            "data": location_stats
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/compare-locations', methods=['POST'])
def compare_locations():
    """
    Compare statistics across multiple locations
    """
    try:
        selected_locations = request.json.get('locations', [])
        
        comparison_data = {}
        for location in selected_locations:
            logs = TrafficLog.query.filter_by(location=location).order_by(TrafficLog.timestamp.desc()).limit(15).all()
            
            if logs:
                vehicle_counts = [log.vehicle_count for log in logs]
                congestion_levels = [log.congestion_level for log in logs]
                
                # Proportional congestion percentage based on actual vehicle counts
                # Assume 0 vehicles = 0% congestion, 120 vehicles = 100% congestion
                max_capacity = 120
                congestion_percentage = (sum(vehicle_counts) / (len(vehicle_counts) * max_capacity) * 100) if vehicle_counts else 0
                
                high_count = congestion_levels.count('High')
                
                comparison_data[location] = {
                    "avg_vehicles": sum(vehicle_counts) / len(vehicle_counts) if vehicle_counts else 0,
                    "peak_vehicles": max(vehicle_counts) if vehicle_counts else 0,
                    "congestion_percentage": congestion_percentage,
                    "total_high_alerts": high_count
                }
        
        return jsonify({
            "status": "success",
            "comparison": comparison_data
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/chart-data', methods=['GET'])
def get_chart_data():
    """
    Get data for charts and visualization
    Returns recent traffic logs for visualization
    """
    try:
        recent_logs = TrafficLog.query.order_by(TrafficLog.timestamp.desc()).limit(20).all()
        recent_logs.reverse()
        
        chart_data = {
            "labels": [log.timestamp.strftime("%H:%M:%S") for log in recent_logs],
            "vehicle_counts": [log.vehicle_count for log in recent_logs],
            "locations": [log.location for log in recent_logs],
            "congestion_levels": [log.congestion_level for log in recent_logs],
            "sent_to_cloud": [log.sent_to_cloud for log in recent_logs]
        }
        
        return jsonify({
            "status": "success",
            "data": chart_data
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/all-logs', methods=['GET'])
def get_all_logs():
    """
    Get all traffic logs from database
    """
    try:
        logs = TrafficLog.query.order_by(TrafficLog.timestamp.desc()).limit(100).all()
        return jsonify({
            "status": "success",
            "logs": [log.to_dict() for log in logs]
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/edge/send-concurrent-data', methods=['POST'])
def edge_send_concurrent_data():
    """
    Concurrent Edge Layer Endpoint
    Simulates multiple edge devices generating and sending data simultaneously
    Uses threading to process multiple devices in parallel
    
    Flow: Multiple Edge Devices → Fog Node (concurrent)
    """
    try:
        data = request.get_json() or {}
        num_devices = min(data.get('num_devices', 3), 5)
        
        results = []
        threads = []
        lock = threading.Lock()
        
        def process_device(device):
            """Process single device in thread"""
            with app.app_context():
                try:
                    edge_data = device.generate_traffic_data()
                    
                    with lock:
                        add_console_log(
                            f"[CONCURRENT-EDGE] {device.device_id}: {edge_data['vehicle_count']} vehicles", 
                            "info"
                        )
                    
                    edge_to_fog_latency = random.randint(10, 30)
                    time.sleep(edge_to_fog_latency / 1000)
                    
                    fog_result = fog_node.process_edge_data(edge_data)
                    
                    cloud_response = None
                    fog_to_cloud_latency = 0
                    
                    if fog_result['send_to_cloud']:
                        fog_to_cloud_latency = random.randint(50, 100)
                        time.sleep(fog_to_cloud_latency / 1000)
                        cloud_response = cloud_server.store_data(fog_result['data'])
                    
                    with lock:
                        results.append({
                            "device_id": device.device_id,
                            "edge_data": edge_data,
                            "fog_result": fog_result,
                            "cloud_response": cloud_response,
                            "latency": {
                                "edge_to_fog_ms": edge_to_fog_latency,
                                "fog_to_cloud_ms": fog_to_cloud_latency
                            }
                        })
                        
                except Exception as e:
                    with lock:
                        add_console_log(f"[ERROR] Device {device.device_id}: {str(e)}", "error")
        
        selected_devices = random.sample(edge_devices, num_devices)
        
        add_console_log(
            f"[CONCURRENT MODE] Starting {num_devices} edge devices simultaneously", 
            "warning"
        )
        
        for device in selected_devices:
            thread = threading.Thread(target=process_device, args=(device,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        add_console_log(
            f"[CONCURRENT COMPLETE] Processed {len(results)} devices in parallel", 
            "success"
        )
        
        return jsonify({
            "status": "success",
            "num_devices": num_devices,
            "results": results,
            "message": f"Processed {num_devices} edge devices concurrently"
        })
        
    except Exception as e:
        add_console_log(f"[ERROR] {str(e)}", "error")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚦 SMART TRAFFIC MONITORING SYSTEM - FOG + EDGE COMPUTING 🚦")
    print("="*70)
    print("\n📡 System Architecture:")
    print("   [Edge Layer] → Sensors/Cameras generating traffic data")
    print("   [Fog Layer]  → Quick processing & filtering")
    print("   [Cloud Layer] → Heavy analytics & storage\n")
    print("🌐 Server starting on http://0.0.0.0:5000")
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
