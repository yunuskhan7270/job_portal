from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from ..models import Job
from ..forms import JobForm
from .. import db

employer_bp = Blueprint('employer', __name__, url_prefix='/employer')

@employer_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.role != 'employer':
        return "Access Denied", 403
    form = JobForm()
    if form.validate_on_submit():
        job = Job(title=form.title.data, description=form.description.data, employer_id=current_user.id)
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('employer.dashboard'))
    jobs = Job.query.filter_by(employer_id=current_user.id).all()
    return render_template('employer_dashboard.html', form=form, jobs=jobs)
