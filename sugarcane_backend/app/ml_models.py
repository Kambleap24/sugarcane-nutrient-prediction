import joblib
import numpy as np
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ModelManager:
    """Load and manage ML models with proper error handling"""
    
    def __init__(self, models_path='trained_models'):
        self.models_path = Path(models_path).resolve()
        self.models = {}
        self.scalers = {}
        
        logger.info(f"📁 Model directory: {self.models_path}")
        logger.info(f"📁 Directory exists: {self.models_path.exists()}")
        
        if self.models_path.exists():
            logger.info(f"📁 Files in directory: {list(self.models_path.glob('*.pkl'))}")
        
        self.load_models()
    
    def load_models(self):
        """Load all trained models with detailed error reporting"""
        
        required_files = {
            'nitrogen': 'model_nitrogen_rf.pkl',
            'phosphorus': 'model_phosphorus_svr.pkl',
            'potassium': 'model_potassium_xgb.pkl',
            'features_scaler': 'scaler_features.pkl'
        }
        
        logger.info("🔄 Starting model loading...")
        
        # Check files exist
        missing_files = []
        for key, filename in required_files.items():
            filepath = self.models_path / filename
            if not filepath.exists():
                missing_files.append(f"{key} ({filename})")
            else:
                logger.info(f"✅ Found: {filename}")
        
        if missing_files:
            error_msg = f"❌ Missing model files: {', '.join(missing_files)}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        # Load models
        try:
            self.models['nitrogen'] = joblib.load(
                self.models_path / 'model_nitrogen_rf.pkl'
            )
            logger.info("✅ Loaded nitrogen model")
            
            self.models['phosphorus'] = joblib.load(
                self.models_path / 'model_phosphorus_svr.pkl'
            )
            logger.info("✅ Loaded phosphorus model")
            
            self.models['potassium'] = joblib.load(
                self.models_path / 'model_potassium_xgb.pkl'
            )
            logger.info("✅ Loaded potassium model")
            
            self.scalers['features'] = joblib.load(
                self.models_path / 'scaler_features.pkl'
            )
            logger.info("✅ Loaded feature scaler")
            
            logger.info("✅✅✅ ALL MODELS LOADED SUCCESSFULLY ✅✅✅")
            
        except Exception as e:
            error_msg = f"❌ Failed to load models: {str(e)}"
            logger.error(error_msg)
            raise
    
    def predict(self, ndvi, chlorophyll, latitude=None, longitude=None, day_of_year=None):
        """
        Make nutrient predictions
        
        CRITICAL: Features must match what models were trained with!
        Current: [NDVI, Chlorophyll, Latitude, Longitude, Day]
        
        Adjust if your models use different features
        """
        try:
            logger.debug(f"🔮 Predict called with NDVI={ndvi}, Chlorophyll={chlorophyll}")
            
            # Prepare features - MATCH YOUR TRAINING DATA
            features = [ndvi, chlorophyll]
            
            if latitude is not None:
                features.append(latitude)
            if longitude is not None:
                features.append(longitude)
            if day_of_year is not None:
                features.append(day_of_year)
            
            logger.debug(f"📊 Features prepared: {features}")
            
            # Convert to numpy array
            X = np.array([features])
            logger.debug(f"📊 Feature shape: {X.shape}")
            
            # Scale features
            try:
                X_scaled = self.scalers['features'].transform(X)
                logger.debug(f"✅ Features scaled: {X_scaled}")
            except Exception as e:
                logger.error(f"❌ Feature scaling failed: {str(e)}")
                logger.error(f"❌ Scaler type: {type(self.scalers['features'])}")
                raise
            
            # Make predictions
            nitrogen_pred = float(self.models['nitrogen'].predict(X_scaled))
            phosphorus_pred = float(self.models['phosphorus'].predict(X_scaled))
            potassium_pred = float(self.models['potassium'].predict(X_scaled))
            
            logger.info(f"✅ Predictions: N={nitrogen_pred:.2f}, P={phosphorus_pred:.2f}, K={potassium_pred:.2f}")
            
            # Classify status
            n_status = self._classify_nutrient(nitrogen_pred, 'nitrogen')
            p_status = self._classify_nutrient(phosphorus_pred, 'phosphorus')
            k_status = self._classify_nutrient(potassium_pred, 'potassium')
            
            logger.info(f"✅ Status: N={n_status}, P={p_status}, K={k_status}")
            
            return {
                'success': True,
                'predictions': {
                    'nitrogen': nitrogen_pred,
                    'phosphorus': phosphorus_pred,
                    'potassium': potassium_pred
                },
                'status': {
                    'nitrogen': n_status,
                    'phosphorus': p_status,
                    'potassium': k_status
                },
                'confidence': {
                    'nitrogen': 0.85,
                    'phosphorus': 0.85,
                    'potassium': 0.85
                }
            }
        
        except Exception as e:
            error_msg = f"❌ Prediction failed: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
    
    def _classify_nutrient(self, value, nutrient_type):
        """Classify nutrient level"""
        
        # CRITICAL: ADJUST THESE THRESHOLDS FOR YOUR DATA!
        thresholds = {
            'nitrogen': {'low': 50, 'high': 150},
            'phosphorus': {'low': 20, 'high': 40},
            'potassium': {'low': 150, 'high': 300}
        }
        
        if nutrient_type not in thresholds:
            return 'Unknown'
        
        thresh = thresholds[nutrient_type]
        
        if value < thresh['low']:
            return 'Deficient'
        elif value > thresh['high']:
            return 'Excess'
        else:
            return 'Adequate'

# Global instance
_model_manager = None

def get_model_manager():
    """Get or create model manager singleton"""
    global _model_manager
    if _model_manager is None:
        _model_manager = ModelManager('trained_models')
    return _model_manager
