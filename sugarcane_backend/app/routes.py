from flask import Blueprint, request, jsonify
from app import db, logger
from app.models import Prediction
from app.ml_models import get_model_manager
from datetime import datetime, timedelta
import traceback

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
def health():
    """Health check - verify backend is running"""
    logger.info("🏥 Health check called")
    return jsonify({
        'status': 'healthy',
        'message': '✅ Backend is running',
        'timestamp': datetime.utcnow().isoformat(),
        'database': 'connected'
    }), 200

@api_bp.route('/predict', methods=['POST', 'OPTIONS'])
def predict():
    """
    CRITICAL ENDPOINT - Make predictions
    
    Expected JSON:
    {
        "ndvi": 0.75,
        "chlorophyll": 35.5,
        "latitude": 19.1136,
        "longitude": 72.8697,
        "day_of_year": 150,
        "field_id": "FIELD_001"
    }
    """
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        logger.debug("CORS preflight request")
        return '', 204
    
    try:
        # Get JSON data
        data = request.get_json()
        logger.info(f"📥 Received prediction request: {data}")
        
        # Validate required fields
        if not data:
            logger.error("❌ No JSON data provided")
            return jsonify({'error': 'No data provided'}), 400
        
        if 'ndvi' not in data or 'chlorophyll' not in data:
            logger.error("❌ Missing required fields")
            return jsonify({
                'error': 'Missing required fields: ndvi, chlorophyll'
            }), 400
        
        # Extract and validate inputs
        try:
            ndvi = float(data['ndvi'])
            chlorophyll = float(data['chlorophyll'])
            latitude = float(data['latitude']) if 'latitude' in data else None
            longitude = float(data['longitude']) if 'longitude' in data else None
            day_of_year = int(data['day_of_year']) if 'day_of_year' in data else None
            field_id = data.get('field_id', 'UNKNOWN')
            notes = data.get('notes', '')
            
            logger.info(f"✅ Input validation passed")
            
        except ValueError as e:
            logger.error(f"❌ Input validation error: {str(e)}")
            return jsonify({'error': f'Invalid input format: {str(e)}'}), 400
        
        # Validate ranges
        if not (0 <= ndvi <= 1):
            logger.error(f"❌ NDVI out of range: {ndvi}")
            return jsonify({'error': 'NDVI must be between 0 and 1'}), 400
        
        if chlorophyll < 0:
            logger.error(f"❌ Chlorophyll negative: {chlorophyll}")
            return jsonify({'error': 'Chlorophyll must be non-negative'}), 400
        
        logger.info(f"✅ All validations passed")
        
        # Get model manager and make prediction
        models = get_model_manager()
        result = models.predict(ndvi, chlorophyll, latitude, longitude, day_of_year)
        
        if not result['success']:
            logger.error(f"❌ Model prediction failed: {result['error']}")
            return jsonify({
                'error': result['error'],
                'success': False
            }), 500
        
        logger.info(f"✅ Prediction successful")
        
        # Save to database
        try:
            prediction = Prediction(
                ndvi=ndvi,
                chlorophyll=chlorophyll,
                latitude=latitude,
                longitude=longitude,
                day_of_year=day_of_year,
                nitrogen=result['predictions']['nitrogen'],
                phosphorus=result['predictions']['phosphorus'],
                potassium=result['predictions']['potassium'],
                nitrogen_status=result['status']['nitrogen'],
                phosphorus_status=result['status']['phosphorus'],
                potassium_status=result['status']['potassium'],
                nitrogen_confidence=result['confidence']['nitrogen'],
                phosphorus_confidence=result['confidence']['phosphorus'],
                potassium_confidence=result['confidence']['potassium'],
                field_id=field_id,
                notes=notes
            )
            
            db.session.add(prediction)
            db.session.commit()
            
            logger.info(f"✅ Prediction saved to database with ID: {prediction.id}")
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"❌ Database save failed: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({
                'error': f'Failed to save prediction: {str(e)}',
                'success': False
            }), 500
        
        # Return response
        response = {
            'success': True,
            'prediction_id': prediction.id,
            'timestamp': prediction.created_at.isoformat(),
            'inputs': {
                'ndvi': ndvi,
                'chlorophyll': chlorophyll
            },
            'predictions': result['predictions'],
            'status': result['status'],
            'confidence': result['confidence'],
            'message': '✅ Prediction completed successfully'
        }
        
        logger.info(f"✅ Returning response: {response}")
        return jsonify(response), 201
    
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'error': f'Internal server error: {str(e)}',
            'success': False
        }), 500

@api_bp.route('/history', methods=['GET', 'OPTIONS'])
def history():
    """Get prediction history"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        limit = request.args.get('limit', 50, type=int)
        days = request.args.get('days', 30, type=int)
        field_id = request.args.get('field_id')
        
        logger.info(f"📜 History request: limit={limit}, days={days}")
        
        query = Prediction.query
        
        if field_id:
            query = query.filter_by(field_id=field_id)
        
        start_date = datetime.utcnow() - timedelta(days=days)
        query = query.filter(Prediction.created_at >= start_date)
        
        predictions = query.order_by(Prediction.created_at.desc()).limit(limit).all()
        
        logger.info(f"✅ Found {len(predictions)} predictions")
        
        return jsonify({
            'success': True,
            'count': len(predictions),
            'limit': limit,
            'days': days,
            'data': [p.to_dict() for p in predictions]
        }), 200
    
    except Exception as e:
        logger.error(f"❌ History error: {str(e)}")
        return jsonify({'error': str(e), 'success': False}), 500

@api_bp.route('/statistics', methods=['GET', 'OPTIONS'])
def statistics():
    """Get prediction statistics"""
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        days = request.args.get('days', 30, type=int)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        predictions = Prediction.query.filter(
            Prediction.created_at >= start_date
        ).all()
        
        if not predictions:
            return jsonify({
                'success': True,
                'count': 0,
                'message': 'No predictions in this period'
            }), 200
        
        import numpy as np
        
        nitrogen_values = [p.nitrogen for p in predictions]
        phosphorus_values = [p.phosphorus for p in predictions]
        potassium_values = [p.potassium for p in predictions]
        
        return jsonify({
            'success': True,
            'count': len(predictions),
            'nitrogen': {
                'mean': round(float(np.mean(nitrogen_values)), 2),
                'min': round(float(np.min(nitrogen_values)), 2),
                'max': round(float(np.max(nitrogen_values)), 2),
                'std': round(float(np.std(nitrogen_values)), 2)
            },
            'phosphorus': {
                'mean': round(float(np.mean(phosphorus_values)), 2),
                'min': round(float(np.min(phosphorus_values)), 2),
                'max': round(float(np.max(phosphorus_values)), 2),
                'std': round(float(np.std(phosphorus_values)), 2)
            },
            'potassium': {
                'mean': round(float(np.mean(potassium_values)), 2),
                'min': round(float(np.min(potassium_values)), 2),
                'max': round(float(np.max(potassium_values)), 2),
                'std': round(float(np.std(potassium_values)), 2)
            }
        }), 200
    
    except Exception as e:
        logger.error(f"❌ Statistics error: {str(e)}")
        return jsonify({'error': str(e), 'success': False}), 500
