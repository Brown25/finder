
#main.py
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime
from __init__ import create_app, db, login_manager, bcrypt
from models import User, Package
from forms import LoginForm, RegisterForm, CreateLabelForm
from tracking import Label
from package_generator import PackageNumberGenerator

# Create the Flask app instance
app = create_app()

@login_manager.user_loader
def load_user(user_id):
    """
    Load the user given their ID.

    Parameters:
        user_id (int): The ID of the user to load.

    Returns:
        User: The user object corresponding to the given ID.
    """
    return User.query.get(int(user_id))

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """
    Handle requests to the home page.

    If the request method is POST, attempts to find the package by tracking number.
    If found, displays the package information. Otherwise, displays an error message.

    Returns:
        Response: Renders the home template with package information or an error message.
    """
    error = None
    package_info = None

    if request.method == "POST":
        tracking_number = request.form.get("tracking_number")
        
        # Assuming `Package` is a model defined in `models.py` and `db` is your SQLAlchemy instance
        package = Package.query.filter_by(tracking_number=tracking_number).first()

        if package:
            package_info = package.get_info()
        else:
            error = "Invalid tracking number."
    
    current_time = datetime.now().strftime("%A %b %d, %Y, %H:%M:%S")
    return render_template("home.html", error=error, package_info=package_info, current_time=current_time)

@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle requests to the login page.

    If the form is submitted and valid, attempts to log the user in.
    If successful, redirects to the home page. Otherwise, displays an error message.

    Returns:
        Response: Renders the login template with the login form and any error messages.
    """
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
    """
    Log the user out and redirect to the home page.

    Returns:
        Response: Redirects to the home page.
    """
    logout_user()
    return redirect(url_for("index"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handle requests to the registration page.

    If the form is submitted and valid, attempts to register a new user.
    If successful, logs the user in and redirects to the home page. Otherwise, displays an error message.

    Returns:
        Response: Renders the registration template with the registration form and any error messages.
    """
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

@app.route('/create_label', methods=['GET', 'POST'])
@login_required
def create_label():
    """
    Handle requests to the create label page.

    If the form is submitted and valid, generates a new tracking number and creates a label.
    If successful, adds the new package to the database and redirects to the home page with a success message.

    Returns:
        Response: Renders the create label template with the create label form and any success/error messages.
    """
    form = CreateLabelForm()

    if form.validate_on_submit():
        package_number_generator = PackageNumberGenerator()
        tracking_number = package_number_generator.generate()

        sender = form.sender.data
        recipient = form.recipient.data
        address = form.address.data

        label = Label(tracking_number, sender, recipient, address)
        label_info = label.get_label_info()

        new_package = Package(
            tracking_number=tracking_number,
            sender=sender,
            recipient=recipient,
            address=address,
            creation_date=label_info["creation_date"]
        )
        db.session.add(new_package)
        db.session.commit()

        flash('Label created successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('create_label.html', form=form)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
