import json
from datetime import datetime


class CloudServer:
    """
    Cloud Server Class
    Represents the Cloud layer in Fog Computing architecture.
    Responsible for:
    - Final heavy analytics
    - Long-term data storage
    - Processing aggregated data from Fog nodes
    """
    
    def __init__(self):
        self.storage = []
        self.analytics_results = []
        
    def store_data(self, data):
        """
        Store traffic data sent from Fog layer
        
        Args:
            data (dict): Traffic data containing vehicle count, congestion level, etc.
            
        Returns:
            dict: Response with storage confirmation and analytics
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        stored_record = {
            "timestamp": timestamp,
            "data": data,
            "source": "fog_layer"
        }
        
        self.storage.append(stored_record)
        
        analytics = self.perform_analytics(data)
        
        self.analytics_results.append({
            "timestamp": timestamp,
            "analytics": analytics
        })
        
        print(f"\n{'='*60}")
        print(f"[CLOUD LAYER] Data Stored at {timestamp}")
        print(f"{'='*60}")
        print(f"Vehicle Count: {data.get('vehicle_count', 'N/A')}")
        print(f"Congestion Level: {data.get('congestion_level', 'N/A')}")
        print(f"Edge Device ID: {data.get('device_id', 'N/A')}")
        print(f"Location: {data.get('location', 'N/A')}")
        print(f"\n[CLOUD ANALYTICS] Final Decision:")
        print(f"  - Action Required: {analytics['action_required']}")
        print(f"  - Recommendation: {analytics['recommendation']}")
        print(f"  - Total Records in Cloud: {len(self.storage)}")
        print(f"{'='*60}\n")
        
        return {
            "status": "success",
            "message": "Data stored in cloud successfully",
            "record_id": len(self.storage),
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
        
        average_count = sum(record['data'].get('vehicle_count', 0) 
                          for record in self.storage[-10:]) / max(len(self.storage[-10:]), 1)
        
        return {
            "action_required": action,
            "recommendation": recommendation,
            "average_last_10": round(average_count, 2),
            "trend": "increasing" if vehicle_count > average_count else "decreasing"
        }
    
    def get_all_records(self):
        """
        Retrieve all stored records
        
        Returns:
            list: All stored traffic records
        """
        return self.storage
    
    def get_analytics_summary(self):
        """
        Get summary of all analytics performed
        
        Returns:
            dict: Summary of cloud analytics
        """
        return {
            "total_records": len(self.storage),
            "total_analytics": len(self.analytics_results),
            "latest_analytics": self.analytics_results[-1] if self.analytics_results else None
        }
