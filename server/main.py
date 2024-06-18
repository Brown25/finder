from __init__ import create_app, db, login_manager, bcrypt  # Ensure bcrypt is imported from __init__.py
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import User, Package
from forms import LoginForm, RegisterForm  # Assuming you have these forms defined in forms.py
from datetime import datetime

app = create_app()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    error = None
    #package_info = None
    if request.method == "POST":
        tracking_number = request.form.get("tracking_number")
        package = Package.query.filter_by(tracking_number=tracking_number).first()
        if package: 
            #package_info = package.get_info()
        else:
            error = "Invalid tracking number."
    
    current_time = datetime.now().strftime("%A %b %d, %Y, %H:%M:%S")
    return render_template("home.html", error=error, package_info=package_info, current_time=current_time)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Incorrect username or password', 'danger')
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if not existing_user:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Account created successfully!', 'success')
            return redirect(url_for('index'))
        flash('Username already exists', 'danger')
    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
