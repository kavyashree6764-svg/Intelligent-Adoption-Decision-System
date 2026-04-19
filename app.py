from flask import Flask, request, jsonify
from flask_cors import CORS
from model import AdoptionDecisionModel

app = Flask(__name__)
CORS(app)

# Initialize model
model = AdoptionDecisionModel()


# -------- HOME ROUTE --------
@app.route('/')
def home():
    return "Adoption Decision API is Running 🚀"


# -------- PREDICT ROUTE --------
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # 🔹 Get original model result
        result = model.final_decision(data)

        # Extract values safely
        scores = result.get("scores", {})
        fraud_risk = result.get("fraud_risk", 0)
        final_score = result.get("final_score", 0)

        compatibility = scores.get("compatibility", 0)
        financial = scores.get("financial", 0)
        background = scores.get("background", 0)
        ml_confidence = scores.get("ml_confidence", 0)

        # -----------------------------------
        # 🔥 EXPLAINABILITY ENGINE
        # -----------------------------------
        contributions = {
            "compatibility": round(0.3 * compatibility, 2),
            "financial": round(0.25 * financial, 2),
            "background": round(0.2 * background, 2),
            "ml_confidence": round(0.25 * ml_confidence, 2),
            "fraud_penalty": round(-0.3 * fraud_risk, 2)
        }

        # Rank impact
        impact_ranking = sorted(contributions.items(), key=lambda x: x[1])

        # -----------------------------------
        # 🔥 DECISION TRACE
        # -----------------------------------
        trace = []

        if fraud_risk > 70:
            trace.append("High fraud risk triggered rejection")

        if financial < 50:
            trace.append("Low financial stability")

        if background < 50:
            trace.append("Background verification failed")

        if ml_confidence < 40:
            trace.append("Low parenting experience (ML confidence low)")

        if not trace:
            trace.append("All conditions satisfied within acceptable range")

        # -----------------------------------
        # 🔥 COUNTERFACTUAL ENGINE
        # -----------------------------------
        suggestions = []

        if financial < 70:
            suggestions.append("Increase income to improve financial score above 70")

        if fraud_risk > 40:
            suggestions.append("Reduce income mismatch to lower fraud risk below 40")

        if ml_confidence < 60:
            suggestions.append("Increase parenting experience to at least 3+ years")

        if background < 100:
            suggestions.append("Complete background verification")

        # -----------------------------------
        # 🔹 MERGE EVERYTHING
        # -----------------------------------
        result["contributions"] = contributions
        result["impact_ranking"] = impact_ranking
        result["decision_trace"] = trace
        result["counterfactual"] = suggestions

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)})


# -------- RUN SERVER --------
if __name__ == "__main__":
    app.run(debug=True)