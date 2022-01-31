from flask_app import app, bcrypt
from flask_app.models.model_magazines import Magazine
from flask_app.models import model_users
from flask import redirect, render_template, request, session

@app.route("/users/account")
def account_page():
    if 'user_id' not in session:
        return redirect("/")
    user = model_users.User.get_user_magazines({"id": session['user_id']})
    print(user.magazines, "user magazines")
    return render_template("show_user.html", user=user)

@app.route("/users/update", methods=["POST"])
def update_user():
    update_data = {**request.form}
    update_data["id"] = session["user_id"]
    is_valid = model_users.User.validate_user_update(update_data)
    if not is_valid:
        return redirect("/users/account")
    model_users.User.update_one(update_data)
    return redirect("/users/account")
