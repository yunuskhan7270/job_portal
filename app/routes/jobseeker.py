from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..models import Job, Application
from .. import db

jobseeker_bp = Blueprint('jobseeker', __name__, url_prefix='/jobseeker')

@jobseeker_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'jobseeker':
        return "Access Denied", 403
    jobs = Job.query.all()
    applied_jobs = [a.job_id for a in Application.query.filter_by(seeker_id=current_user.id).all()]
    return render_template('jobseeker_dashboard.html', jobs=jobs, applied_jobs=applied_jobs)

@jobseeker_bp.route('/apply/<int:job_id>')
@login_required
def apply(job_id):
    if current_user.role != 'jobseeker':
        return "Access Denied", 403
    existing = Application.query.filter_by(job_id=job_id, seeker_id=current_user.id).first()
    if not existing:
        db.session.add(Application(job_id=job_id, seeker_id=current_user.id))
        db.session.commit()
    return redirect(url_for('jobseeker.dashboard'))
