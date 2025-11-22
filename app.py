import os
import random
import time
from flask import Flask, render_template, request, jsonify
from cloud import CloudServer
from fog import FogNode
from edge_simulator import EdgeDevice, create_sample_devices

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

cloud_server = CloudServer()
fog_node = FogNode("FOG_NODE_CENTRAL")
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
    Clear console logs
    """
    global console_logs
    console_logs = []
    return jsonify({
        "status": "success",
        "message": "Logs cleared"
    })


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
