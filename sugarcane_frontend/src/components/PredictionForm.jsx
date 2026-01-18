import { useState } from 'react';
import { predictNutrients } from '../services/api';
import '../styles/PredictionForm.css';

export default function PredictionForm({ onSuccess, onError }) {
  const [formData, setFormData] = useState({
    ndvi: '',
    chlorophyll: '',
    latitude: '',
    longitude: '',
    day_of_year: '',
    field_id: '',
    notes: ''
  });

  const [loading, setLoading] = useState(false);
  const [validationError, setValidationError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setValidationError('');
  };

  const validateForm = () => {
    console.log('🔍 Validating form...');
    
    if (!formData.ndvi || !formData.chlorophyll) {
      setValidationError('NDVI and Chlorophyll are required');
      return false;
    }

    const ndvi = parseFloat(formData.ndvi);
    const chlorophyll = parseFloat(formData.chlorophyll);

    if (isNaN(ndvi) || ndvi < 0 || ndvi > 1) {
      setValidationError('NDVI must be a number between 0 and 1');
      return false;
    }

    if (isNaN(chlorophyll) || chlorophyll < 0) {
      setValidationError('Chlorophyll must be a non-negative number');
      return false;
    }

    console.log('✅ Form validation passed');
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log('📤 Form submitted');

    if (!validateForm()) {
      return;
    }

    setLoading(true);
    setValidationError('');

    try {
      // Prepare payload - convert empty strings to undefined
      const payload = {
        ndvi: parseFloat(formData.ndvi),
        chlorophyll: parseFloat(formData.chlorophyll)
      };

      if (formData.latitude) payload.latitude = parseFloat(formData.latitude);
      if (formData.longitude) payload.longitude = parseFloat(formData.longitude);
      if (formData.day_of_year) payload.day_of_year = parseInt(formData.day_of_year);
      if (formData.field_id) payload.field_id = formData.field_id;
      if (formData.notes) payload.notes = formData.notes;

      console.log('📝 Payload:', payload);

      const result = await predictNutrients(payload);

      console.log('✅ SUCCESS! Received result:', result);
      onSuccess(result);

      // Reset form
      setFormData({
        ndvi: '',
        chlorophyll: '',
        latitude: '',
        longitude: '',
        day_of_year: '',
        field_id: '',
        notes: ''
      });

    } catch (error) {
      console.error('❌ Prediction failed:', error.message);
      setValidationError(`Error: ${error.message}`);
      onError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <h2>🌾 Sugarcane Nutrient Prediction</h2>
      <p>Enter crop parameters to get nutrient predictions</p>

      {validationError && (
        <div className="error-box">
          <span>❌ {validationError}</span>
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>NDVI (0-1) *</label>
          <input
            type="number"
            name="ndvi"
            min="0"
            max="1"
            step="0.01"
            value={formData.ndvi}
            onChange={handleChange}
            placeholder="0.75"
            required
          />
          <small>Normalized Difference Vegetation Index</small>
        </div>

        <div className="form-group">
          <label>Chlorophyll (mg/m²) *</label>
          <input
            type="number"
            name="chlorophyll"
            step="0.1"
            value={formData.chlorophyll}
            onChange={handleChange}
            placeholder="35.5"
            required
          />
          <small>Leaf chlorophyll content</small>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Latitude (optional)</label>
            <input
              type="number"
              name="latitude"
              step="0.0001"
              value={formData.latitude}
              onChange={handleChange}
              placeholder="19.1136"
            />
          </div>

          <div className="form-group">
            <label>Longitude (optional)</label>
            <input
              type="number"
              name="longitude"
              step="0.0001"
              value={formData.longitude}
              onChange={handleChange}
              placeholder="72.8697"
            />
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Day of Year (optional)</label>
            <input
              type="number"
              name="day_of_year"
              min="1"
              max="365"
              value={formData.day_of_year}
              onChange={handleChange}
              placeholder="150"
            />
            <small>1-365</small>
          </div>

          <div className="form-group">
            <label>Field ID (optional)</label>
            <input
              type="text"
              name="field_id"
              value={formData.field_id}
              onChange={handleChange}
              placeholder="FIELD_001"
            />
          </div>
        </div>

        <div className="form-group">
          <label>Notes (optional)</label>
          <textarea
            name="notes"
            rows="3"
            value={formData.notes}
            onChange={handleChange}
            placeholder="Any observations..."
          />
        </div>

        <button type="submit" className="submit-btn" disabled={loading}>
          {loading ? '⏳ Predicting...' : '🔮 Get Prediction'}
        </button>
      </form>
    </div>
  );
}
