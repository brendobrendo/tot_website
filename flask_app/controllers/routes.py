from flask_app import app, bcrypt
from flask_app.models.model_users import User
from flask import redirect, render_template, request, session

@app.route("/")
def index():
    if 'user_id' in session:
        return redirect("/dashboard")
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    print(request.form, "THIS IS THE DATA BEING PASSED INT TO VALIDATE LOGIN")
    is_valid = User.validate_login(request.form)
    if not is_valid:
        return redirect("/")
    return redirect("/dashboard")

@app.route("/register", methods=["POST"])
def register():
    data = {**request.form}
    is_valid = User.validate_user(data)
    if not is_valid:
        return redirect("/")
    hashed_pw = bcrypt.generate_password_hash(data['password'])
    data['password'] = hashed_pw
    user = User.save(data)
    session['user_id'] = user
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    del session['user_id']
    return redirect("/")