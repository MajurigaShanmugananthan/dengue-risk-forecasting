from flask import Blueprint, request, jsonify
from app.ml.predictor import predict_dengue_risk

routes = Blueprint("routes", __name__)

@routes.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400

    # Extract model choice
    model_type = data.pop("model", "rf")  # REMOVE model from features

    result = predict_dengue_risk(data, model_type)
    return jsonify(result)
