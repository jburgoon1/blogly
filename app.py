"""Blogly application."""

from flask import Flask, redirect, render_template,request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'bloglyapp'

connect_db(app)
# db.create_all()

@app.route("/")
def show_home():
   
    return render_template('home.html')

@app.route('/users')
def show_users():
     users = User.query.all()
     return render_template('users.html', users = users)

@app.route("/add_new")
def show_form():
    return render_template('new_user.html')

@app.route("/add_new", methods = ['POST'])
def make_new_user():
    first = request.form['first']
    last = request.form['last']
    img = request.form['img']

    new_user = User(first_name = first, last_name = last, image_url = img)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route("/user/<int:user_id>")
def show_details(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('detais.html', user = user)

@app.route('/user/<int:user_id>/edit')
def edit_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user = user)

# @app.route('/user/<int:user_id>/edit', methods = ['POST'])
# def update_user(user_id):


@app.route("/user/<int:user_id>/edit", methods = ['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    User.query.delete(user)
    db.session.commit()
    return redirect('/users')

