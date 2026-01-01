from flask import Blueprint, request, jsonify
from app.ml.predictor import predict_dengue_risk

routes = Blueprint("routes", __name__)

@routes.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    result = predict_dengue_risk(data)
    return jsonify(result)
