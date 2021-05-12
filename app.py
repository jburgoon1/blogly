"""Blogly application."""

from flask import Flask, redirect, render_template,request
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/blogly'
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

@app.route('/user/<int:user_id>/edit', methods = ['POST'])
def update_user(user_id):
    user_id.first_name = request.form['first']
    user_id.last_name = request.form['last']
    user_id.image_url = request.form['img']
    db.session.add(user_id.first_name, user_id.last_name, user_id.image_url)
    db.session.commit()
    return redirect('/user/<int:user_id>')


@app.route("/user/<int:user_id>/edit", methods = ['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    User.query.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/new-post')
def show_new_form():
    return render_template('post_form.html')

@app.route('/user/<int:user_id>/new-post', methods=['POST'])
def submit_post(user_id):
    title = request.form['title']
    content = request.form['content']
    user= user_id
    post = Post(title = title, content = content, user_id = user)
    db.session.add(post)
    db.session.commit()
    return redirect('/user/<int:user_id>', post= post)

@app.route('/user/<int:user_id>/<int:post_id>')
def show_post(user_id,post_id):
    user = user_id
    post = post_id
    return render_template('posts.html', user = user, post = post)

@app.route('/user/<int:user_id>/posts/edit')
def show_edit_form(user_id, post_id):
    post = post_id
    user = user_id
    return render_template('post_edit.html', post = post, user= user)

@app.route('/user/<int:user_id>/posts/edit', methods = ['POST'])
def edit_post(user_id, post_id):
    post_id.title = request.form['title']
    post_id.content = request.form['content']
    new_post = [post_id.title, post_id.content]
    db.session.add(new_post)
    db.session.commit()
    return redirect('/user/<int:user_id>/<int:post_id>')
@app.route('/user/<int:user_id>/<int:post_id>/delete')
def delete_post(user_id,post_id):
    db.query.delete(post_id)
    db.session.commit()
    return redirect('/user/<int:user_id>')




