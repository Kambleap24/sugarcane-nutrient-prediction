from app import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Prediction(db.Model):
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Input features
    ndvi = db.Column(db.Float, nullable=False)
    chlorophyll = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    day_of_year = db.Column(db.Integer, nullable=True)
    
    # Predictions
    nitrogen = db.Column(db.Float, nullable=False)
    phosphorus = db.Column(db.Float, nullable=False)
    potassium = db.Column(db.Float, nullable=False)
    
    # Status classification
    nitrogen_status = db.Column(db.String(50), nullable=False)
    phosphorus_status = db.Column(db.String(50), nullable=False)
    potassium_status = db.Column(db.String(50), nullable=False)
    
    # Confidence scores
    nitrogen_confidence = db.Column(db.Float, nullable=True)
    phosphorus_confidence = db.Column(db.Float, nullable=True)
    potassium_confidence = db.Column(db.Float, nullable=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    field_id = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        """Convert prediction to JSON-serializable dict"""
        try:
            return {
                'id': self.id,
                'inputs': {
                    'ndvi': round(float(self.ndvi), 4),
                    'chlorophyll': round(float(self.chlorophyll), 2),
                    'latitude': round(float(self.latitude), 4) if self.latitude else None,
                    'longitude': round(float(self.longitude), 4) if self.longitude else None,
                    'day_of_year': int(self.day_of_year) if self.day_of_year else None
                },
                'predictions': {
                    'nitrogen': round(float(self.nitrogen), 2),
                    'phosphorus': round(float(self.phosphorus), 2),
                    'potassium': round(float(self.potassium), 2)
                },
                'status': {
                    'nitrogen': self.nitrogen_status,
                    'phosphorus': self.phosphorus_status,
                    'potassium': self.potassium_status
                },
                'confidence': {
                    'nitrogen': round(float(self.nitrogen_confidence), 4) if self.nitrogen_confidence else None,
                    'phosphorus': round(float(self.phosphorus_confidence), 4) if self.phosphorus_confidence else None,
                    'potassium': round(float(self.potassium_confidence), 4) if self.potassium_confidence else None
                },
                'created_at': self.created_at.isoformat(),
                'field_id': self.field_id,
                'notes': self.notes
            }
        except Exception as e:
            logger.error(f"❌ Error converting prediction to dict: {str(e)}")
            raise
