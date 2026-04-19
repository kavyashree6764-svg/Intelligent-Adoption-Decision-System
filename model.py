import uuid

class AdoptionDecisionModel:

    def __init__(self):
        self.base_weights = {
            "compatibility": 0.35,
            "ml_confidence": 0.25,
            "financial": 0.20,
            "background": 0.20
        }

    # -------- Compatibility --------
    def calculate_compatibility(self, age_diff, preference_match):
        score = (1 - age_diff/50) * 50 + (preference_match * 50)
        return max(0, min(score, 100))

    # -------- Financial --------
    def financial_score(self, income):
        return 90 if income >= 50000 else 70 if income >= 30000 else 50 if income >= 20000 else 30

    # -------- Background --------
    def background_score(self, verified):
        return 90 if verified else 40

    # -------- Fraud Detection --------
    def fraud_detection(self, declared_income, actual_income):
        gap = abs(declared_income - actual_income)
        if gap > 20000:
            return 80
        elif gap > 10000:
            return 50
        return 20

    # -------- Fraud Category --------
    def fraud_category(self, fraud):
        if fraud >= 70:
            return "HIGH RISK"
        elif fraud >= 40:
            return "MEDIUM RISK"
        return "LOW RISK"

    # -------- ML Confidence --------
    def ml_prediction(self, experience):
        return min(100, experience * 20)

    # -------- 🔥 Fraud-Driven Adaptive System --------
    def adaptive_system(self, fraud):
        weights = self.base_weights.copy()

        # Dynamic Thresholds
        approve_threshold = 75
        review_threshold = 50

        # 🔥 Core Innovation: Fraud modifies entire system
        if fraud >= 70:
            weights["compatibility"] *= 0.3
            weights["ml_confidence"] *= 0.3
            weights["background"] *= 1.5

            approve_threshold = 85
            review_threshold = 60

        elif fraud >= 40:
            weights["compatibility"] *= 0.7
            approve_threshold = 80

        return weights, approve_threshold, review_threshold

    # -------- Final Decision --------
    def final_decision(self, data):

        compatibility = self.calculate_compatibility(
            data["age_diff"], data["preference_match"]
        )
        financial = self.financial_score(data["income"])
        background = self.background_score(data["verified"])
        fraud = self.fraud_detection(data["declared_income"], data["actual_income"])
        ml_conf = self.ml_prediction(data["experience"])

        weights, approve_th, review_th = self.adaptive_system(fraud)

        final_score = (
            weights["compatibility"] * compatibility +
            weights["ml_confidence"] * ml_conf +
            weights["financial"] * financial +
            weights["background"] * background
        )

        # -------- Impact Engine (RANKED) --------
        impacts = {
            "compatibility": round(weights["compatibility"] * compatibility, 2),
            "financial": round(weights["financial"] * financial, 2),
            "background": round(weights["background"] * background, 2),
            "ml_confidence": round(weights["ml_confidence"] * ml_conf, 2)
        }

        # Sort impacts (highest influence first)
        ranked_impacts = sorted(impacts.items(), key=lambda x: x[1], reverse=True)

        explanations = []
        for factor, impact in ranked_impacts:
            if impact > 0:
                explanations.append(f"{factor.capitalize()} contributed +{impact}")
            else:
                explanations.append(f"{factor.capitalize()} negatively impacted decision")

        # Add fraud explanation
        fraud_level = self.fraud_category(fraud)
        explanations.append(f"Fraud Risk: {fraud} ({fraud_level}) influenced system behavior")

        # -------- Decision Logic --------
        if fraud >= 85:
            decision = "AUTO-REJECTED (Critical Fraud)"
            reason = "System override due to extreme fraud risk"
        elif final_score > approve_th:
            decision = "APPROVED"
            reason = "Meets adaptive approval criteria"
        elif final_score > review_th:
            decision = "NEEDS REVIEW"
            reason = "Borderline case under adaptive thresholds"
        else:
            decision = "REJECTED"
            reason = "Below acceptable threshold"

        # -------- Traceable Audit --------
        trace_id = str(uuid.uuid4())

        audit = {
            "trace_id": trace_id,
            "inputs": data,
            "weights": weights,
            "thresholds": {
                "approve": approve_th,
                "review": review_th
            },
            "ranked_impacts": ranked_impacts,
            "fraud_category": fraud_level
        }

        return {
            "trace_id": trace_id,
            "scores": {
                "compatibility": compatibility,
                "financial": financial,
                "background": background,
                "ml_confidence": ml_conf
            },
            "fraud_risk": fraud,
            "fraud_category": fraud_level,
            "final_score": round(final_score, 2),
            "decision": decision,
            "reason": reason,
            "impact_ranking": ranked_impacts,
            "explanations": explanations,
            "audit_trail": audit
        }


# -------- TEST --------
if __name__ == "__main__":
    model = AdoptionDecisionModel()

    sample = {
        "age_diff": 10,
        "preference_match": 0.6,
        "income": 25000,
        "verified": False,
        "declared_income": 50000,
        "actual_income": 25000,
        "experience": 1
    }

    print(model.final_decision(sample))