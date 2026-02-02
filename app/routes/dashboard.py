"""Dashboard routes."""

from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
def index():
    """Render the main dashboard."""
    return render_template('dashboard.html')


@dashboard_bp.route('/health')
def health():
    """Health check endpoint for Cloud Run."""
    return {'status': 'healthy'}, 200
