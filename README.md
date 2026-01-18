# Sugarcane Nutrient Prediction System

A **production-ready machine learning application** that predicts nutrient levels (Nitrogen, Phosphorus, Potassium) in sugarcane crops using NDVI and Chlorophyll indices.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)
![React](https://img.shields.io/badge/React-18+-61DAFB.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)

## 🎯 Overview

This project provides:
- **ML Models** for nutrient prediction (Random Forest, SVR, XGBoost)
- **REST API** built with Flask for real-time predictions
- **React Frontend** with interactive UI for farmers
- **SQLite Database** for storing prediction history
- **Analytics Dashboard** with historical trends

## 🚀 Features

✅ Real-time nutrient prediction from satellite imagery data
✅ Prediction history and trend analysis
✅ REST API with comprehensive error handling
✅ Responsive web interface
✅ Data export (JSON, CSV)
✅ Production-ready logging
✅ CORS enabled for multi-origin requests
✅ Comprehensive validation and error handling

## 📋 Tech Stack

### Backend
- **Flask** - REST API framework
- **Flask-CORS** - Cross-Origin Resource Sharing
- **Flask-SQLAlchemy** - ORM database
- **scikit-learn** - Machine Learning models
- **joblib** - Model serialization
- **SQLite** - Database

### Frontend
- **React** - UI framework
- **Vite** - Build tool
- **Axios** - HTTP client
- **CSS3** - Styling

### ML Models
- Random Forest Regressor (Nitrogen prediction)
- Support Vector Regression (Phosphorus prediction)
- XGBoost (Potassium prediction)
- StandardScaler (Feature normalization)

## 📁 Project Structure

```
sugarcane-nutrient-prediction/
├── backend/
│   ├── app/
│   │   ├── __init__.py           # Flask app factory
│   │   ├── models.py             # SQLAlchemy models
│   │   ├── ml_models.py          # ML model manager
│   │   └── routes.py             # API endpoints
│   ├── trained_models/           # Serialized ML models
│   │   ├── nitrogen_model.pkl
│   │   ├── phosphorus_model.pkl
│   │   ├── potassium_model.pkl
│   │   └── scaler_features.pkl
│   ├── logs/                     # Application logs
│   ├── run.py                    # Flask entry point
│   ├── requirements.txt          # Python dependencies
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── components/           # React components
│   │   │   ├── PredictionForm.jsx
│   │   │   └── Results.jsx
│   │   ├── services/             # API communication
│   │   │   └── api.js
│   │   ├── App.jsx               # Main component
│   │   ├── App.css               # Styling
│   │   └── main.jsx              # Entry point
│   ├── public/
│   ├── package.json              # NPM dependencies
│   └── README.md
│
├── docs/
│   ├── API_DOCUMENTATION.md
│   ├── DEPLOYMENT.md
│   └── MODEL_TRAINING.md
│
├── .gitignore
├── LICENSE
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

```bash
# Clone repository
git clone https://github.com/yourusername/sugarcane-nutrient-prediction.git
cd sugarcane-nutrient-prediction

# Backend setup
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Flask server
python run.py
```

Backend will start on `http://localhost:5000`

### Frontend Setup

```bash
# In new terminal, from project root
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will start on `http://localhost:5173`

## 📡 API Endpoints

### Health Check
```bash
GET /api/health
```
Returns: Backend status and database connection

### Make Prediction
```bash
POST /api/predict
Content-Type: application/json

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

Returns:
```json
{
  "success": true,
  "prediction_id": 1,
  "timestamp": "2024-01-18T...",
  "predictions": {
    "nitrogen": 85.5,
    "phosphorus": 32.1,
    "potassium": 220.3
  },
  "status": {
    "nitrogen": "Adequate",
    "phosphorus": "Adequate",
    "potassium": "Adequate"
  },
  "confidence": {
    "nitrogen": 0.85,
    "phosphorus": 0.85,
    "potassium": 0.85
  }
}
```

### Get History
```bash
GET /api/history?limit=50&days=30&field_id=FIELD_001
```

### Get Statistics
```bash
GET /api/statistics?days=30
```

### Export Data
```bash
GET /api/export?format=json&days=30
# or format=csv
```

## 🤖 Model Information

### Features Required
- **NDVI** (0-1): Normalized Difference Vegetation Index
- **Chlorophyll** (mg/m²): Leaf chlorophyll content
- **Latitude** (optional): Field location
- **Longitude** (optional): Field location
- **Day of Year** (1-365, optional): Growth stage indicator

### Output
- **Nitrogen**: Predicted value in mg/kg
- **Phosphorus**: Predicted value in mg/kg
- **Potassium**: Predicted value in mg/kg
- **Status**: Deficient / Adequate / Excess

### Classification Thresholds
```python
Nitrogen:     Low < 50,  High > 150
Phosphorus:   Low < 20,  High > 40
Potassium:    Low < 150, High > 300
```
*Customize these in `app/ml_models.py` based on your agronomic standards*

## 📊 Data Flow

```
User Input (Frontend)
    ↓
Validation (Client-side)
    ↓
HTTP POST /api/predict
    ↓
Input Validation (Server)
    ↓
Feature Scaling
    ↓
ML Model Prediction
    ↓
Status Classification
    ↓
Database Save
    ↓
JSON Response
    ↓
Display Results (Frontend)
```

## 🔧 Configuration

### Backend Configuration (`app/__init__.py`)
```python
# Database
DATABASE_URL = 'sqlite:///predictions.db'

# CORS Origins
ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:5173'
]

# Logging
LOG_LEVEL = logging.DEBUG
LOG_FILE = 'logs/app.log'
```

### Frontend Configuration (`.env`)
```
VITE_API_URL=http://localhost:5000/api
```

## 🧪 Testing

### Test Backend Health
```bash
curl http://localhost:5000/api/health
```

### Test Prediction
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "ndvi": 0.75,
    "chlorophyll": 35.5
  }'
```

### Test Frontend
Open `http://localhost:5173/` in browser and:
1. Check if "Backend: Connected" shows green indicator
2. Fill in NDVI and Chlorophyll values
3. Click "Get Prediction"
4. Verify results display immediately

## 📈 Performance

- **API Response Time**: < 500ms per prediction
- **Database Queries**: Optimized with proper indexing
- **Frontend Load Time**: < 2 seconds
- **Model Inference**: < 100ms

## 🔐 Security Considerations

- Input validation on all endpoints
- SQL injection prevention via SQLAlchemy ORM
- CORS properly configured
- Error messages don't expose sensitive information
- Models are read-only after deployment

## 🐛 Troubleshooting

### Backend Issues
```bash
# Check if models are loaded
cat logs/app.log | grep "Models"

# Verify database
ls -la predictions.db

# Check CORS errors
# Open browser console (F12) and look for CORS error messages
```

### Frontend Issues
```bash
# Check network requests
# Open DevTools > Network tab
# Look for /api/predict request

# Check console errors
# DevTools > Console tab
# Look for red error messages
```

### Model Not Found Error
```bash
# Verify model files exist
ls -la backend/trained_models/

# Ensure file names match exactly:
# - nitrogen_model.pkl
# - phosphorus_model.pkl
# - potassium_model.pkl
# - scaler_features.pkl
```

## 📚 Documentation

- [API Documentation](docs/API_DOCUMENTATION.md) - Detailed API reference
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment instructions
- [Model Training](docs/MODEL_TRAINING.md) - How to train your own models

## 🚀 Deployment

### Production Deployment
```bash
# Build frontend
cd frontend
npm run build

# Run backend with gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Docker Deployment
```bash
# Build images
docker build -t sugarcane-backend ./backend
docker build -t sugarcane-frontend ./frontend

# Run containers
docker run -p 5000:5000 sugarcane-backend
docker run -p 3000:80 sugarcane-frontend
```

See [Deployment Guide](docs/DEPLOYMENT.md) for detailed instructions.

## 📊 Results Example

Input:
```
NDVI: 0.75
Chlorophyll: 35.5
```

Output:
```
Nitrogen: 85.5 mg/kg (Adequate) ✅
Phosphorus: 32.1 mg/kg (Adequate) ✅
Potassium: 220.3 mg/kg (Adequate) ✅

Recommendations:
- All nutrients are at optimal levels
- Continue current fertilization schedule
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 👨‍💼 Author

**Your Name**
- GitHub: [@Kambleap24](https://github.com/Kambleap24)
- LinkedIn: [Akash Kamble](https://linkedin.com/in/akashkamble30)
- Email: kambleap24.comp@coeptech.ac.in


## 🙏 Acknowledgments

- Sugarcane farming communities for domain knowledge
- ML model optimization techniques from research papers
- Open-source Flask, React, and scikit-learn communities

## 📞 Support

For issues, questions, or suggestions:
1. Open an [Issue](https://github.com/yourusername/sugarcane-nutrient-prediction/issues)
2. Provide:
   - Detailed description of the problem
   - Steps to reproduce
   - Error messages and logs
   - Your environment (OS, Python version, etc.)

## 🎓 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [scikit-learn Guide](https://scikit-learn.org/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)

---

**Made with ❤️ for sustainable agriculture**
