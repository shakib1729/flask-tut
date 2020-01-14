from app import app   # 'app' director is a package, import from app __init__

from flask import render_template

@app.route('/admin/dashboard')
def admin_dashboard():
	return render_template('admin/dashboard.html')

@app.route('/admin/profile')
def admin_profile():
	return render_template('admin/profile.html')
