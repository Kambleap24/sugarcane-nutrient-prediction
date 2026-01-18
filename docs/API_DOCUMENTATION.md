# API Documentation

## Base URL
```
http://localhost:5000/api
```

## Health Check Endpoint

### `GET /health`

Check if the backend API is running and models are loaded.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-18T10:30:45.123456",
  "database": "connected",
  "models_loaded": true,
  "version": "1.0.0"
}
```

**Status Codes:**
- `200 OK` - Backend is healthy
- `503 Service Unavailable` - Backend or models not available

---

## Prediction Endpoint

### `POST /predict`

Make a nutrient prediction based on NDVI and Chlorophyll values.

**Request Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "ndvi": 0.75,
  "chlorophyll": 35.5,
  "latitude": 19.1136,
  "longitude": 72.8697,
  "day_of_year": 150,
  "field_id": "FIELD_001",
  "notes": "Morning measurement"
}
```

**Required Fields:**
- `ndvi` (float): 0-1, Normalized Difference Vegetation Index
- `chlorophyll` (float): > 0, Chlorophyll content in mg/m²

**Optional Fields:**
- `latitude` (float): Field location latitude (-90 to 90)
- `longitude` (float): Field location longitude (-180 to 180)
- `day_of_year` (int): 1-365, Day of the year
- `field_id` (string): Identifier for the field
- `notes` (string): Additional notes about the measurement

**Response (Success - 200):**
```json
{
  "success": true,
  "prediction_id": 1,
  "timestamp": "2024-01-18T10:30:45.123456Z",
  "input": {
    "ndvi": 0.75,
    "chlorophyll": 35.5
  },
  "predictions": {
    "nitrogen": {
      "value": 85.5,
      "unit": "mg/kg"
    },
    "phosphorus": {
      "value": 32.1,
      "unit": "mg/kg"
    },
    "potassium": {
      "value": 220.3,
      "unit": "mg/kg"
    }
  },
  "status": {
    "nitrogen": "Adequate",
    "phosphorus": "Adequate",
    "potassium": "Adequate"
  },
  "confidence": {
    "nitrogen": 0.85,
    "phosphorus": 0.82,
    "potassium": 0.88
  },
  "recommendations": {
    "nitrogen": "Current level is optimal. Continue current fertilization schedule.",
    "phosphorus": "Current level is adequate. Monitor in next week.",
    "potassium": "Current level is good. No immediate action needed."
  }
}
```

**Response (Validation Error - 400):**
```json
{
  "success": false,
  "error": "Invalid input",
  "details": {
    "ndvi": "Value must be between 0 and 1",
    "chlorophyll": "Value must be greater than 0"
  }
}
```

**Response (Server Error - 500):**
```json
{
  "success": false,
  "error": "Prediction failed",
  "message": "Model inference error",
  "timestamp": "2024-01-18T10:30:45.123456Z"
}
```

**Status Codes:**
- `200 OK` - Prediction successful
- `400 Bad Request` - Invalid input data
- `422 Unprocessable Entity` - Validation failed
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Models not loaded

---

## History Endpoint

### `GET /history`

Retrieve prediction history with optional filtering.

**Query Parameters:**
```
?limit=50&days=30&field_id=FIELD_001&offset=0
```

- `limit` (int, optional): Number of records to return. Default: 50, Max: 500
- `days` (int, optional): Filter last N days. Default: 30
- `field_id` (string, optional): Filter by field ID
- `offset` (int, optional): Pagination offset. Default: 0

**Response (200):**
```json
{
  "success": true,
  "total": 150,
  "limit": 50,
  "offset": 0,
  "data": [
    {
      "prediction_id": 150,
      "timestamp": "2024-01-18T10:30:45Z",
      "field_id": "FIELD_001",
      "ndvi": 0.75,
      "chlorophyll": 35.5,
      "predictions": {
        "nitrogen": 85.5,
        "phosphorus": 32.1,
        "potassium": 220.3
      },
      "status": {
        "nitrogen": "Adequate",
        "phosphorus": "Adequate",
        "potassium": "Adequate"
      }
    },
    {
      "prediction_id": 149,
      "timestamp": "2024-01-17T14:22:30Z",
      "field_id": "FIELD_001",
      "ndvi": 0.72,
      "chlorophyll": 33.2,
      "predictions": {
        "nitrogen": 82.1,
        "phosphorus": 30.8,
        "potassium": 215.5
      },
      "status": {
        "nitrogen": "Adequate",
        "phosphorus": "Adequate",
        "potassium": "Adequate"
      }
    }
  ]
}
```

**Status Codes:**
- `200 OK` - History retrieved
- `400 Bad Request` - Invalid query parameters
- `500 Internal Server Error` - Server error

---

## Statistics Endpoint

### `GET /statistics`

Get statistical summary of predictions.

**Query Parameters:**
```
?days=30&field_id=FIELD_001
```

- `days` (int, optional): Analyze last N days. Default: 30
- `field_id` (string, optional): Filter by field ID

**Response (200):**
```json
{
  "success": true,
  "period": {
    "start_date": "2023-12-19",
    "end_date": "2024-01-18",
    "days": 30
  },
  "total_predictions": 45,
  "nitrogen": {
    "mean": 85.5,
    "min": 72.3,
    "max": 95.8,
    "std_dev": 6.2,
    "trend": "increasing"
  },
  "phosphorus": {
    "mean": 31.2,
    "min": 25.1,
    "max": 38.5,
    "std_dev": 3.1,
    "trend": "stable"
  },
  "potassium": {
    "mean": 218.4,
    "min": 190.5,
    "max": 245.3,
    "std_dev": 15.8,
    "trend": "increasing"
  },
  "field_statistics": {
    "FIELD_001": {
      "predictions": 30,
      "avg_ndvi": 0.73,
      "avg_chlorophyll": 34.2
    }
  }
}
```

**Status Codes:**
- `200 OK` - Statistics retrieved
- `400 Bad Request` - Invalid query parameters
- `500 Internal Server Error` - Server error

---

## Export Endpoint

### `GET /export`

Export prediction data in various formats.

**Query Parameters:**
```
?format=json&days=30&field_id=FIELD_001
```

- `format` (string, required): `json` or `csv`
- `days` (int, optional): Export last N days. Default: 30
- `field_id` (string, optional): Filter by field ID

**JSON Export Response (200):**
```json
{
  "export_metadata": {
    "format": "json",
    "exported_at": "2024-01-18T10:35:00Z",
    "total_records": 45,
    "period_days": 30
  },
  "data": [
    {
      "prediction_id": 150,
      "timestamp": "2024-01-18T10:30:45Z",
      "ndvi": 0.75,
      "chlorophyll": 35.5,
      "nitrogen": 85.5,
      "phosphorus": 32.1,
      "potassium": 220.3,
      "nitrogen_status": "Adequate",
      "phosphorus_status": "Adequate",
      "potassium_status": "Adequate"
    }
  ]
}
```

**CSV Export Response (200):**
```
prediction_id,timestamp,ndvi,chlorophyll,nitrogen,phosphorus,potassium,nitrogen_status,phosphorus_status,potassium_status
150,2024-01-18T10:30:45Z,0.75,35.5,85.5,32.1,220.3,Adequate,Adequate,Adequate
149,2024-01-17T14:22:30Z,0.72,33.2,82.1,30.8,215.5,Adequate,Adequate,Adequate
```

**Status Codes:**
- `200 OK` - Export successful
- `400 Bad Request` - Invalid format or parameters
- `500 Internal Server Error` - Server error

---

## Error Handling

### Error Response Format

All error responses follow this format:

```json
{
  "success": false,
  "error": "Error type",
  "message": "Descriptive error message",
  "timestamp": "2024-01-18T10:30:45.123456Z",
  "details": {
    "field_name": "Validation error message"
  }
}
```

### Common HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | OK | Request successful |
| 400 | Bad Request | Missing required field |
| 422 | Unprocessable Entity | Invalid data type |
| 500 | Internal Server Error | Model inference failed |
| 503 | Service Unavailable | Models not loaded |

### Validation Rules

**NDVI:**
- Type: float
- Range: 0.0 to 1.0
- Error: "NDVI must be between 0 and 1"

**Chlorophyll:**
- Type: float
- Range: > 0
- Error: "Chlorophyll must be greater than 0"

**Latitude (optional):**
- Type: float
- Range: -90 to 90
- Error: "Latitude must be between -90 and 90"

**Longitude (optional):**
- Type: float
- Range: -180 to 180
- Error: "Longitude must be between -180 and 180"

**Day of Year (optional):**
- Type: integer
- Range: 1 to 365
- Error: "Day of year must be between 1 and 365"

---

## Rate Limiting

Currently, there is **no rate limiting** implemented. For production, consider adding:
- 100 requests per minute per IP
- Implement using Flask-Limiter

---

## Authentication

Currently, **no authentication** is implemented. For production, consider adding:
- API Key authentication
- JWT tokens
- OAuth 2.0

---

## CORS Configuration

The API accepts requests from:
- `http://localhost:3000`
- `http://localhost:5173`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:5173`

To add more origins, modify `app/__init__.py`.

---

## Example Requests

### Using cURL

**Health Check:**
```bash
curl http://localhost:5000/api/health
```

**Make Prediction:**
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "ndvi": 0.75,
    "chlorophyll": 35.5,
    "field_id": "FIELD_001"
  }'
```

**Get History:**
```bash
curl "http://localhost:5000/api/history?limit=10&days=7"
```

**Export as CSV:**
```bash
curl "http://localhost:5000/api/export?format=csv&days=30" > predictions.csv
```

### Using JavaScript/Fetch

```javascript
// Make prediction
const response = await fetch('http://localhost:5000/api/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    ndvi: 0.75,
    chlorophyll: 35.5
  })
});

const data = await response.json();
console.log(data);
```

### Using Python/Requests

```python
import requests

# Make prediction
response = requests.post(
    'http://localhost:5000/api/predict',
    json={
        'ndvi': 0.75,
        'chlorophyll': 35.5,
        'field_id': 'FIELD_001'
    }
)

data = response.json()
print(data)
```

---

## API Versioning

Current API Version: **v1.0**

API versioning is not implemented yet. Future versions may include:
- `/api/v1/predict`
- `/api/v2/predict` (with enhanced features)

---

## Contact & Support

For API issues or questions:
- Email: support@example.com
- GitHub Issues: [Project Issues](https://github.com/yourusername/sugarcane-nutrient-prediction/issues)
- Documentation: [API Documentation](docs/API_DOCUMENTATION.md)

---

Last Updated: January 18, 2024
