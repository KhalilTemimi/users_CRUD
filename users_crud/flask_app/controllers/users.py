from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.user import User

@app.route("/")
def index():
    # call the get all classmethod to get all friends
    users = User.get_all()
    print(users)
    return render_template("index.html", users = users)

@app.route("/user_form")
def add_user():
    return render_template('create.html')

@app.route('/create_user', methods=["POST"])
def create_user():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    data = {
        "fname": request.form["fname"],
        "lname" : request.form["lname"],
        "email" : request.form["email"]
    }
    # We pass the data dictionary into the save method from the Friend class.
    user = User.save(data)
    # Don't forget to redirect after saving to the database.
    return redirect('/show_last')

@app.route('/show_user/<int:user_id>')
def show_user(user_id):
    data={"id":user_id}
    return render_template('/read.html',user = User.show(data))

@app.route('/show_last')
def show_last():
    user = User.show_last_user()
    return render_template('/read.html',user = user)

@app.route('/edit_user/<int:user_id>')
def edit_user(user_id):
    data = {"id":user_id}
    return render_template('/edit.html',user = User.get_one(data))

@app.route("/user/update/<int:user_id>", methods=['post'])
def update_user(user_id):
    data = {
        **request.form,'id':user_id
    }
    User.edit(data)
    return redirect(f'/show_user/{user_id}')


@app.route('/delete_user/<int:user_id>')
def delete(user_id):
    data = {"id":user_id}
    User.delete(data)
    return redirect('/')