# ⚡ Quick Start Guide

Get the Sugarcane Nutrient Prediction System running in 5 minutes!

## Prerequisites

- **Python 3.8+** - Download from [python.org](https://www.python.org/downloads/)
- **Node.js 14+** - Download from [nodejs.org](https://nodejs.org/)
- **Git** - Download from [git-scm.com](https://git-scm.com/)

Verify installation:
```bash
python --version
node --version
npm --version
git --version
```

---

## 🚀 Backend Setup (5 minutes)

### 1. Navigate to Backend
```bash
cd backend
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Start Backend Server
```bash
python run.py
```

✅ **Backend ready!** You should see:
```
🚀 SUGARCANE NUTRIENT PREDICTION SYSTEM
✅ Successfully imported app module
✅✅✅ Flask application created successfully ✅✅✅
🌐 SERVER CONFIGURATION
🎯 Backend API: http://0.0.0.0:5000
🎯 API Base: http://localhost:5000/api
🚀 Starting Flask server...
```

**Keep this terminal open!**

---

## 🎨 Frontend Setup (5 minutes)

### 1. Open New Terminal Window

### 2. Navigate to Frontend
```bash
cd frontend
```

### 3. Install Dependencies
```bash
npm install
```

### 4. Start Development Server
```bash
npm run dev
```

✅ **Frontend ready!** You should see:
```
VITE v... ready in ... ms

➜  Local:   http://localhost:5173/
➜  press h to show help
```

---

## 🧪 Test the Application

### 1. Open Browser
Visit: `http://localhost:5173/`

### 2. Check Backend Connection
You should see **"Backend: Connected ✅"** (green indicator)

### 3. Make a Test Prediction
1. Enter NDVI value: `0.75`
2. Enter Chlorophyll value: `35.5`
3. Click **"Get Prediction"**
4. See nutrient prediction results!

---

## 📡 Test API Directly

### Option 1: Using Browser
```
http://localhost:5000/api/health
```

### Option 2: Using cURL
```bash
curl http://localhost:5000/api/health
```

### Option 3: Using PowerShell
```powershell
Invoke-WebRequest -Uri http://localhost:5000/api/health
```

### Option 4: Using Python
```python
import requests

# Health check
response = requests.get('http://localhost:5000/api/health')
print(response.json())

# Make prediction
response = requests.post(
    'http://localhost:5000/api/predict',
    json={'ndvi': 0.75, 'chlorophyll': 35.5}
)
print(response.json())
```

---

## 🗂️ Project Structure (Quick Overview)

```
sugarcane-nutrient-prediction/
├── backend/                    # 🐍 Python/Flask
│   ├── app/
│   │   ├── __init__.py        # Flask app factory
│   │   ├── models.py          # Database models
│   │   ├── ml_models.py       # ML model manager
│   │   └── routes.py          # API endpoints
│   ├── trained_models/        # ML models (pickle files)
│   ├── logs/                  # Application logs
│   ├── run.py                 # Start Flask here
│   └── requirements.txt        # Python dependencies
│
├── frontend/                   # ⚛️ React/Vite
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API communication
│   │   └── App.jsx            # Main component
│   ├── package.json           # NPM dependencies
│   └── index.html             # Entry HTML
│
└── README.md                  # Project documentation
```

---

## 📊 API Quick Reference

### Health Check
```bash
GET /api/health
```
Returns backend status

### Make Prediction
```bash
POST /api/predict
Content-Type: application/json

{
  "ndvi": 0.75,
  "chlorophyll": 35.5
}
```

### Get Prediction History
```bash
GET /api/history?limit=10&days=30
```

### Export Data
```bash
GET /api/export?format=csv&days=30
```

---

## 🛠️ Troubleshooting

### Backend won't start?
```bash
# Check if port 5000 is in use
# Windows
netstat -ano | findstr :5000

# Mac/Linux
lsof -i :5000

# Kill process if needed (Windows)
taskkill /PID <PID> /F
```

### Frontend won't connect to backend?
1. Make sure backend is running (`python run.py`)
2. Check browser console (F12) for CORS errors
3. Verify `VITE_API_URL` in frontend `.env` file

### Models not loading?
```bash
# Check if trained_models folder exists
ls backend/trained_models/

# Should contain:
# - nitrogen_model.pkl
# - phosphorus_model.pkl
# - potassium_model.pkl
# - scaler_features.pkl
```

### Database errors?
```bash
# Remove old database and restart
rm backend/predictions.db
python backend/run.py
```

---

## 📝 Common Commands

### Backend
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install/upgrade packages
pip install -r requirements.txt

# Check logs
tail -f logs/app.log  # Mac/Linux
Get-Content -Wait logs/app.log  # Windows
```

### Frontend
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Git
```bash
# Check status
git status

# Commit changes
git add .
git commit -m "Your message"

# Push to GitHub
git push origin main
```

---

## 🔧 Development Tips

### Hot Reload
- Frontend automatically reloads when you save files
- Backend auto-reloads (if debug mode enabled)

### Debug Mode
- Open browser DevTools: **F12**
- Check Console for errors
- Check Network tab for API calls

### Test Different Values
```
NDVI Range: 0.0 - 1.0
- 0.0-0.3: Low vegetation
- 0.3-0.6: Medium vegetation  
- 0.6-1.0: High vegetation

Chlorophyll Range: 0+ mg/m²
- 10-20: Low
- 20-40: Optimal
- 40+: High
```

---

## 📚 Next Steps

1. ✅ **Get it running** - You're here!
2. 📖 Read [README.md](README.md) for full project info
3. 📡 Check [API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) for API details
4. 🚀 Follow [GITHUB_SETUP_GUIDE.md](GITHUB_SETUP_GUIDE.md) to push to GitHub
5. 📝 Add to your resume
6. 🔄 Make improvements and commit

---

## ✨ What You Can Do Now

- ✅ Make predictions with different input values
- ✅ View prediction history
- ✅ Export data as JSON or CSV
- ✅ Check API response times
- ✅ Explore the codebase
- ✅ Modify ML thresholds in `app/ml_models.py`
- ✅ Customize the UI in React components
- ✅ Add more features and commit to GitHub

---

## 🎯 Performance Tips

### For Better Performance:
1. Keep Chrome/Firefox DevTools closed during testing
2. Use production build: `npm run build`
3. Close unnecessary applications
4. Restart backend if it becomes sluggish

### Check Response Times:
```bash
# In browser console
time(() => fetch('http://localhost:5000/api/predict', {...}))
```

---

## 📞 Need Help?

1. Check error logs: `backend/logs/app.log`
2. Open browser console: **F12 → Console**
3. Check GitHub Issues: [github.com/yourusername/sugarcane-nutrient-prediction/issues](https://github.com/yourusername/sugarcane-nutrient-prediction/issues)
4. Read full documentation: [README.md](README.md)

---

## 🎉 You're Ready!

Congratulations! Your application is running. Now:

1. Test it with different values
2. Explore the code
3. Push it to GitHub
4. Share with recruiters
5. Add it to your portfolio

**Happy Coding!** 🚀

---

Last Updated: January 18, 2024
