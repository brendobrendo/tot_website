from flask_app import app, bcrypt
from flask_app.models.model_magazines import Magazine
from flask_app.models import model_users
from flask import redirect, render_template, request, session

@app.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    magazines = Magazine.get_all()
    user = model_users.User.get_one({"id": session['user_id']})
    return render_template("show_magazines.html", magazines=magazines, user=user)

@app.route("/magazine/new")
def new_magazine():
    if 'user_id' not in session:
        return redirect('/')
    user = model_users.User.get_one({'id':session['user_id']})
    return render_template("new_magazine.html", user=user)

@app.route("/create/magazine", methods=["POST"])
def create_sighting():
    magazine_data = {**request.form, 'user_id': session['user_id']}
    is_valid = Magazine.validate_magazine_update(request.form)
    if not is_valid:
        return redirect('/magazine/new')
    Magazine.save(magazine_data)
    return redirect("/dashboard")

@app.route("/show/<int:id>") #make sure id is the sighting id
def view_magazine(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {"id": id}
    magazine = Magazine.get_one(data)
    user = model_users.User.get_one({'id':session['user_id']})
    return render_template("show_magazine.html", magazine=magazine, user=user)

@app.route("/edit/<int:id>") #make sure id is the sighting id
def edit_post(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {"id": id}
    sighting = Sighting.get_one(data)
    if sighting.user_id != session['user_id']:
        return redirect("/dashboard")
    user = model_user.User.get_one({'id':session['user_id']})
    session['sighting_id'] = id
    return render_template("edit_sighting.html", sighting=sighting, user=user)

"""
@app.route("/update", methods=["POST"])
def update():
    update_data = {**request.form}
    update_data['id'] = session['sighting_id']
    print(update_data)
    Sighting.update_one(update_data)
    del session['sighting_id']
    return redirect("/dashboard")
"""

@app.route("/delete/<int:id>")
def delete(id):
    data = {"id": id}
    Magazine.delete_one(data)
    return redirect("/users/account")
