from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models import Job, User

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return "Access Denied", 403
    jobs = Job.query.count()
    employers = User.query.filter_by(role='employer').count()
    seekers = User.query.filter_by(role='jobseeker').count()
    return render_template('admin_dashboard.html', jobs=jobs, employers=employers, seekers=seekers)
