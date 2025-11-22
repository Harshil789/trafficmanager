import json
import time
import random
from datetime import datetime


class FogNode:
    """
    Fog Node Class
    Represents the Fog layer in Fog Computing architecture.
    Responsible for:
    - Intermediate data processing
    - Quick decision making
    - Filtering data before sending to cloud
    - Reducing latency by processing at the edge of network
    """
    
    def __init__(self, node_id="FOG_NODE_01"):
        self.node_id = node_id
        self.processed_count = 0
        self.forwarded_to_cloud = 0
        self.filtered_count = 0
        
    def process_edge_data(self, edge_data):
        """
        Process data received from Edge devices
        Makes quick decisions about whether to forward to cloud
        
        Args:
            edge_data (dict): Data from edge device
            
        Returns:
            dict: Processing result with decision
        """
        start_time = time.time()
        
        self.processed_count += 1
        
        vehicle_count = edge_data.get('vehicle_count', 0)
        location = edge_data.get('location', 'Unknown')
        device_id = edge_data.get('device_id', 'Unknown')
        
        congestion_level = self._calculate_congestion(vehicle_count)
        
        send_to_cloud = self._should_send_to_cloud(congestion_level, vehicle_count)
        
        processing_time = (time.time() - start_time) * 1000
        
        fog_latency = random.randint(10, 30)
        
        processed_data = {
            "device_id": device_id,
            "location": location,
            "vehicle_count": vehicle_count,
            "congestion_level": congestion_level,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "processed_by": self.node_id,
            "fog_processing_time_ms": round(processing_time, 2),
            "fog_latency_ms": fog_latency
        }
        
        print(f"\n{'*'*60}")
        print(f"[FOG LAYER] Processing Data from {device_id}")
        print(f"{'*'*60}")
        print(f"Location: {location}")
        print(f"Vehicle Count: {vehicle_count}")
        print(f"Calculated Congestion: {congestion_level}")
        print(f"Fog Processing Time: {round(processing_time, 2)} ms")
        print(f"Edge → Fog Latency: {fog_latency} ms")
        
        if send_to_cloud:
            self.forwarded_to_cloud += 1
            print(f"[FOG DECISION] ⚠️  ALERT! Forwarding to CLOUD (High Traffic Detected)")
        else:
            self.filtered_count += 1
            print(f"[FOG DECISION] ✓ Normal Traffic - Handled Locally (No Cloud Needed)")
        
        print(f"Fog Stats - Processed: {self.processed_count} | To Cloud: {self.forwarded_to_cloud} | Filtered: {self.filtered_count}")
        print(f"{'*'*60}\n")
        
        return {
            "status": "success",
            "data": processed_data,
            "send_to_cloud": send_to_cloud,
            "fog_decision": "Forward to Cloud" if send_to_cloud else "Handle Locally",
            "latency_ms": fog_latency
        }
    
    def _calculate_congestion(self, vehicle_count):
        """
        Calculate congestion level based on vehicle count
        This is the quick decision-making logic of Fog
        
        Args:
            vehicle_count (int): Number of vehicles detected
            
        Returns:
            str: Congestion level (Low/Medium/High)
        """
        if vehicle_count < 30:
            return "Low"
        elif vehicle_count < 70:
            return "Medium"
        else:
            return "High"
    
    def _should_send_to_cloud(self, congestion_level, vehicle_count):
        """
        Decide whether data should be sent to cloud for heavy analytics
        Fog filters out normal traffic, only sends critical data to cloud
        
        Args:
            congestion_level (str): Calculated congestion level
            vehicle_count (int): Number of vehicles
            
        Returns:
            bool: True if should send to cloud, False otherwise
        """
        if congestion_level == "High":
            return True
        
        if vehicle_count > 60:
            return True
        
        return False
    
    def get_stats(self):
        """
        Get statistics of fog node processing
        
        Returns:
            dict: Fog node statistics
        """
        return {
            "node_id": self.node_id,
            "total_processed": self.processed_count,
            "forwarded_to_cloud": self.forwarded_to_cloud,
            "filtered_locally": self.filtered_count,
            "cloud_reduction_percentage": round(
                (self.filtered_count / max(self.processed_count, 1)) * 100, 2
            )
        }
