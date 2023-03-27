"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
# db.create_all()


@app.route('/')
def redirect_users():
    """redirect to users page"""
    return redirect('/users')


@app.route('/users')
def users_page():
    """Shows home page"""
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/new')
def user_form():
    """New user form"""
    return render_template('add.html')


@app.route('/users/new', methods=["POST"])
def create_user():
    """Submit form to add user"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name,
                    image_url=image_url or None)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Show details about single user"""
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)


@app.route('/users/<int:user_id>/edit')
def user_edit(user_id):
    """Show edit user page"""
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    """Submit form to edit user data"""
    user = User.query.get_or_404(user_id)
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user"""
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect('/users')


# Have a cancel button that returns to the detail page for a user, and a save button that updates the user.

# POST /users/[user-id]/edit
# Process the edit form, returning the user to the /users page.
# POST /users/[user-id]/delete
# Delete the user.
