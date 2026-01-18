export default function Results({ data }) {
  if (!data) {
    return null;
  }

  if (!data.success) {
    return (
      <div className="results-container">
        <div className="error-box">
          <h3>❌ Error</h3>
          <p>{data.error || 'Prediction failed'}</p>
        </div>
      </div>
    );
  }

  const { predictions, status, confidence } = data;

  const NutrientCard = ({ name, value, st, conf }) => {
    const statusClass = st.toLowerCase();
    return (
      <div className={`nutrient-card ${statusClass}`}>
        <h3>{name}</h3>
        <div className="value">{value.toFixed(2)} mg/kg</div>
        <div className="status">{st}</div>
        <div className="confidence">
          Confidence: {(conf * 100).toFixed(0)}%
        </div>
      </div>
    );
  };

  return (
    <div className="results-container">
      <h2>✅ Results</h2>

      <div className="nutrients-grid">
        <NutrientCard
          name="Nitrogen"
          value={predictions.nitrogen}
          st={status.nitrogen}
          conf={confidence.nitrogen}
        />
        <NutrientCard
          name="Phosphorus"
          value={predictions.phosphorus}
          st={status.phosphorus}
          conf={confidence.phosphorus}
        />
        <NutrientCard
          name="Potassium"
          value={predictions.potassium}
          st={status.potassium}
          conf={confidence.potassium}
        />
      </div>

      <div className="metadata">
        <small>
          Prediction ID: {data.prediction_id} | 
          Time: {new Date(data.timestamp).toLocaleString()}
        </small>
      </div>
    </div>
  );
}
