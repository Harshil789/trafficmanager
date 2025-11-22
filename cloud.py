import json
from datetime import datetime
from models import TrafficLog


class CloudServer:
    """
    Cloud Server Class
    Represents the Cloud layer in Fog Computing architecture.
    Responsible for:
    - Final heavy analytics
    - Long-term data storage (using PostgreSQL database)
    - Processing aggregated data from Fog nodes
    """
    
    def __init__(self, db):
        self.db = db
        
    def store_data(self, data):
        """
        Store traffic data sent from Fog layer in database
        
        Args:
            data (dict): Traffic data containing vehicle count, congestion level, etc.
            
        Returns:
            dict: Response with storage confirmation and analytics
        """
        analytics = self.perform_analytics(data)
        
        traffic_log = TrafficLog(
            device_id=data.get('device_id', 'Unknown'),
            location=data.get('location', 'Unknown'),
            vehicle_count=data.get('vehicle_count', 0),
            average_speed_kmh=data.get('average_speed_kmh'),
            congestion_level=data.get('congestion_level', 'Low'),
            processed_by_fog=data.get('processed_by', 'Unknown'),
            fog_latency_ms=data.get('fog_latency_ms', 0),
            sent_to_cloud=True,
            cloud_action=analytics['action_required'],
            cloud_recommendation=analytics['recommendation']
        )
        
        self.db.session.add(traffic_log)
        self.db.session.commit()
        
        timestamp = traffic_log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        
        total_records = TrafficLog.query.filter_by(sent_to_cloud=True).count()
        
        print(f"\n{'='*60}")
        print(f"[CLOUD LAYER] Data Stored in Database at {timestamp}")
        print(f"{'='*60}")
        print(f"Vehicle Count: {data.get('vehicle_count', 'N/A')}")
        print(f"Congestion Level: {data.get('congestion_level', 'N/A')}")
        print(f"Edge Device ID: {data.get('device_id', 'N/A')}")
        print(f"Location: {data.get('location', 'N/A')}")
        print(f"\n[CLOUD ANALYTICS] Final Decision:")
        print(f"  - Action Required: {analytics['action_required']}")
        print(f"  - Recommendation: {analytics['recommendation']}")
        print(f"  - Total Records in Cloud DB: {total_records}")
        print(f"{'='*60}\n")
        
        return {
            "status": "success",
            "message": "Data stored in cloud database successfully",
            "record_id": traffic_log.id,
            "analytics": analytics
        }
    
    def perform_analytics(self, data):
        """
        Perform heavy analytics on traffic data
        This simulates complex cloud-based processing
        
        Args:
            data (dict): Traffic data
            
        Returns:
            dict: Analytics results with recommendations
        """
        vehicle_count = data.get('vehicle_count', 0)
        congestion_level = data.get('congestion_level', 'Low')
        
        if congestion_level == "High" or vehicle_count > 80:
            action = "ALERT_TRAFFIC_CONTROL"
            recommendation = "Deploy additional traffic officers and activate alternate routes"
        elif congestion_level == "Medium" or vehicle_count > 50:
            action = "MONITOR_CLOSELY"
            recommendation = "Adjust traffic signal timings to improve flow"
        else:
            action = "NO_ACTION"
            recommendation = "Traffic flow is normal, continue monitoring"
        
        recent_logs = TrafficLog.query.order_by(TrafficLog.timestamp.desc()).limit(10).all()
        
        if recent_logs:
            average_count = sum(log.vehicle_count for log in recent_logs) / len(recent_logs)
        else:
            average_count = vehicle_count
        
        return {
            "action_required": action,
            "recommendation": recommendation,
            "average_last_10": round(average_count, 2),
            "trend": "increasing" if vehicle_count > average_count else "decreasing"
        }
    
    def get_all_records(self):
        """
        Retrieve all stored records from database
        
        Returns:
            list: All stored traffic records
        """
        logs = TrafficLog.query.order_by(TrafficLog.timestamp.desc()).all()
        return [log.to_dict() for log in logs]
    
    def get_analytics_summary(self):
        """
        Get summary of all analytics performed
        
        Returns:
            dict: Summary of cloud analytics
        """
        total_records = TrafficLog.query.filter_by(sent_to_cloud=True).count()
        total_all_logs = TrafficLog.query.count()
        latest_log = TrafficLog.query.order_by(TrafficLog.timestamp.desc()).first()
        
        return {
            "total_records": total_records,
            "total_all_logs": total_all_logs,
            "latest_analytics": {
                "action": latest_log.cloud_action,
                "timestamp": latest_log.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            } if latest_log else None
        }
