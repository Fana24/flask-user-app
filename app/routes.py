from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import User
from app.forms import RegistrationForm, UpdateForm

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """Home page displaying welcome message."""
    return render_template('index.html', title='Home')


@main.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration - display form and process submissions."""
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(
    username=form.username.data,
    email=form.email.data,
    first_name=form.first_name.data,
    last_name=form.last_name.data,
    age=form.age.data if form.age.data else None,
    bio=form.bio.data if form.bio.data else None
)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash(f'Account created successfully for {user.username}!', 'success')
            return redirect(url_for('main.profile', user_id=user.id))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
    
    return render_template('register.html', title='Register', form=form)


@main.route('/users')
def users():
    """Display all registered users."""
    all_users = User.query.order_by(User.created_at.desc()).all()
    return render_template('users.html', title='All Users', users=all_users)


@main.route('/profile/<int:user_id>')
def profile(user_id):
    """Display a specific user's profile."""
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', title=f"{user.username}'s Profile", user=user)


@main.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update(user_id):
    """Handle profile updates - display form with current data and process changes."""
    user = User.query.get_or_404(user_id)
    form = UpdateForm()
    
    if form.validate_on_submit():
        # Check if username changed and if new one is taken
        if form.username.data != user.username:
            existing = User.query.filter_by(username=form.username.data).first()
            if existing:
                flash('This username is already taken.', 'danger')
                return render_template('update.html', title='Update Profile', form=form, user=user)
        
        # Check if email changed and if new one is taken
        if form.email.data != user.email:
            existing = User.query.filter_by(email=form.email.data).first()
            if existing:
                flash('This email is already registered.', 'danger')
                return render_template('update.html', title='Update Profile', form=form, user=user)
        
        user.username = form.username.data
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.age = form.age.data if form.age.data else None
        user.bio = form.bio.data if form.bio.data else None
        
        try:
            db.session.commit()
            flash('Your profile has been updated!', 'success')
            return redirect(url_for('main.profile', user_id=user.id))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}', 'danger')
    
    # Pre-fill form with current user data for GET requests
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.age.data = user.age
        form.bio.data = user.bio
    
    return render_template('update.html', title='Update Profile', form=form, user=user)


@main.route('/delete/<int:user_id>', methods=['POST'])
def delete(user_id):
    """Delete a user from the database."""
    user = User.query.get_or_404(user_id)
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f'User {user.username} has been deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {str(e)}', 'danger')
    
    return redirect(url_for('main.users'))