import json
import time
import random
import numpy as np
from datetime import datetime
from models import TrafficLog, FogStats


class FogNode:
    """
    Fog Node Class
    Represents the Fog layer in Fog Computing architecture.
    Responsible for:
    - Intermediate data processing
    - Quick decision making
    - Filtering data before sending to cloud
    - Reducing latency by processing at the edge of network
    - Persisting fog statistics in database
    """
    
    def __init__(self, node_id="FOG_NODE_01", db=None):
        self.node_id = node_id
        self.db = db
        self._stats_initialized = False
        self.history = []
    
    def _ensure_stats_initialized(self):
        """
        Ensure fog stats record exists in database
        Called lazily when needed within app context
        """
        if self.db and not self._stats_initialized:
            fog_stats = FogStats.query.filter_by(node_id=self.node_id).first()
            if not fog_stats:
                fog_stats = FogStats(node_id=self.node_id)
                self.db.session.add(fog_stats)
                self.db.session.commit()
            self._stats_initialized = True
        
    def process_edge_data(self, edge_data):
        """
        Process data received from Edge devices
        Makes quick decisions about whether to forward to cloud
        Stores all data in database
        
        Args:
            edge_data (dict): Data from edge device
            
        Returns:
            dict: Processing result with decision
        """
        self._ensure_stats_initialized()
        
        start_time = time.time()
        
        vehicle_count = edge_data.get('vehicle_count', 0)
        location = edge_data.get('location', 'Unknown')
        device_id = edge_data.get('device_id', 'Unknown')
        
        congestion_level = self._calculate_congestion(vehicle_count)
        
        predicted_congestion = self._predict_congestion(vehicle_count)
        
        send_to_cloud = self._should_send_to_cloud(congestion_level, vehicle_count)
        
        processing_time = (time.time() - start_time) * 1000
        
        fog_latency = random.randint(10, 30)
        
        processed_data = {
            "device_id": device_id,
            "location": location,
            "vehicle_count": vehicle_count,
            "congestion_level": congestion_level,
            "predicted_congestion": predicted_congestion,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "processed_by": self.node_id,
            "fog_processing_time_ms": round(processing_time, 2),
            "fog_latency_ms": fog_latency,
            "average_speed_kmh": edge_data.get('average_speed_kmh')
        }
        
        if self.db:
            traffic_log = TrafficLog(
                device_id=device_id,
                location=location,
                vehicle_count=vehicle_count,
                average_speed_kmh=edge_data.get('average_speed_kmh'),
                congestion_level=congestion_level,
                processed_by_fog=self.node_id,
                fog_latency_ms=fog_latency,
                sent_to_cloud=send_to_cloud
            )
            self.db.session.add(traffic_log)
            
            fog_stats = FogStats.query.filter_by(node_id=self.node_id).first()
            if fog_stats:
                fog_stats.total_processed += 1
                if send_to_cloud:
                    fog_stats.forwarded_to_cloud += 1
                else:
                    fog_stats.filtered_locally += 1
            
            self.db.session.commit()
        
        fog_stats_dict = self.get_stats()
        
        print(f"\n{'*'*60}")
        print(f"[FOG LAYER] Processing Data from {device_id}")
        print(f"{'*'*60}")
        print(f"Location: {location}")
        print(f"Vehicle Count: {vehicle_count}")
        print(f"Calculated Congestion: {congestion_level}")
        print(f"ML Predicted Next: {predicted_congestion}")
        print(f"Fog Processing Time: {round(processing_time, 2)} ms")
        print(f"Edge → Fog Latency: {fog_latency} ms")
        
        if send_to_cloud:
            print(f"[FOG DECISION] ⚠️  ALERT! Forwarding to CLOUD (High Traffic Detected)")
        else:
            print(f"[FOG DECISION] ✓ Normal Traffic - Handled Locally (No Cloud Needed)")
        
        print(f"Fog Stats - Processed: {fog_stats_dict['total_processed']} | To Cloud: {fog_stats_dict['forwarded_to_cloud']} | Filtered: {fog_stats_dict['filtered_locally']}")
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
    
    def _predict_congestion(self, vehicle_count):
        """
        ML-based congestion prediction using simple regression
        Uses historical traffic patterns to predict next congestion level
        
        Args:
            vehicle_count (int): Current vehicle count
            
        Returns:
            str: Predicted congestion level
        """
        self.history.append(vehicle_count)
        
        if len(self.history) > 20:
            self.history = self.history[-20:]
        
        if len(self.history) < 3:
            return self._calculate_congestion(vehicle_count)
        
        try:
            recent_data = np.array(self.history[-5:])
            
            avg_trend = np.mean(np.diff(recent_data))
            
            predicted_count = vehicle_count + avg_trend
            
            predicted_count = max(0, min(predicted_count, 120))
            
            return self._calculate_congestion(int(predicted_count))
            
        except Exception:
            return self._calculate_congestion(vehicle_count)
    
    def get_stats(self):
        """
        Get statistics of fog node processing from database
        
        Returns:
            dict: Fog node statistics
        """
        if self.db:
            fog_stats = FogStats.query.filter_by(node_id=self.node_id).first()
            if fog_stats:
                return fog_stats.to_dict()
        
        return {
            "node_id": self.node_id,
            "total_processed": 0,
            "forwarded_to_cloud": 0,
            "filtered_locally": 0,
            "cloud_reduction_percentage": 0
        }
