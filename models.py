import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class TrafficLog(db.Model):
    """
    Database model for storing traffic data from all layers
    Persists Edge -> Fog -> Cloud data flow
    """
    __tablename__ = 'traffic_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    device_id = db.Column(db.String(100), nullable=False, index=True)
    location = db.Column(db.String(200), nullable=False)
    vehicle_count = db.Column(db.Integer, nullable=False)
    average_speed_kmh = db.Column(db.Integer)
    
    congestion_level = db.Column(db.String(20), nullable=False, index=True)
    processed_by_fog = db.Column(db.String(100))
    fog_latency_ms = db.Column(db.Float)
    
    sent_to_cloud = db.Column(db.Boolean, default=False, index=True)
    cloud_action = db.Column(db.String(100))
    cloud_recommendation = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'device_id': self.device_id,
            'location': self.location,
            'vehicle_count': self.vehicle_count,
            'average_speed_kmh': self.average_speed_kmh,
            'congestion_level': self.congestion_level,
            'processed_by_fog': self.processed_by_fog,
            'fog_latency_ms': self.fog_latency_ms,
            'sent_to_cloud': self.sent_to_cloud,
            'cloud_action': self.cloud_action,
            'cloud_recommendation': self.cloud_recommendation,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def __repr__(self):
        return f'<TrafficLog {self.id} - {self.device_id} - {self.congestion_level}>'


class FogStats(db.Model):
    """
    Database model for storing fog node statistics
    Tracks processing efficiency and filtering metrics
    """
    __tablename__ = 'fog_stats'
    
    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column(db.String(100), nullable=False, unique=True)
    total_processed = db.Column(db.Integer, default=0)
    forwarded_to_cloud = db.Column(db.Integer, default=0)
    filtered_locally = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_cloud_reduction_percentage(self):
        """Calculate percentage of data filtered by fog layer"""
        if self.total_processed == 0:
            return 0
        return round((self.filtered_locally / self.total_processed) * 100, 2)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'node_id': self.node_id,
            'total_processed': self.total_processed,
            'forwarded_to_cloud': self.forwarded_to_cloud,
            'filtered_locally': self.filtered_locally,
            'cloud_reduction_percentage': self.get_cloud_reduction_percentage(),
            'last_updated': self.last_updated.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def __repr__(self):
        return f'<FogStats {self.node_id} - Processed: {self.total_processed}>'
