# Blueprint dedicado a health check / status
from flask import Blueprint, jsonify

health_bp = Blueprint(
    "health",
    __name__,
    url_prefix="/",
)


@health_bp.route("/status/health")
@health_bp.route("/check/health")
def check_health():
    """Health check para monitoreo y load balancers. Devuelve JSON estándar."""
    return jsonify({"status": "ok", "message": "OK"}), 200
