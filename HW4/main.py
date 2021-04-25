from flask import Flask,render_template,request,redirect,session,send_file

from flask_pymongo import PyMongo
app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/WADHW4" # database name: WADHW4, mangodb port 27017 by default run in localhost
mongo = PyMongo(app)



@app.route('/main')
def main():
    if request.cookies.get("name") is None:
        return redirect("")

    return render_template("main.html") #main page



@app.route('/',methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        user = mongo.db.users.find_one({"username": username})
        if user is None:
            msg = "This user does not exist"
        elif user["password"] != password:
            msg = "Incorrect password"
        else:
            resp = redirect("/main")
            resp.set_cookie("name", user["username"], max_age=540000)
            return resp
        return render_template('login.html', msg=msg)

    return render_template("login.html")    #login page


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('signup.html')   #sign up page
    user_name = request.form.get("user_name")

    password = request.form.get("password")
    password2 = request.form.get("password2")
    users = mongo.db.users.find_one({"username": user_name})

    if password!=password2:
        msg="Two password entries are inconsistent"

    elif user_name is None or user_name == "":
        msg = "Username can not be empty"

    elif users is not None:
        msg = "This user is already registered"
    else:
        mongo.db.users.insert_one(
            {"username":user_name, "password": password})
        return redirect("/")
    return render_template('signup.html', msg=msg)  #singup page


@app.route("/static/<path>/",methods=["GET"])
def image(path):
    return send_file("./static/images/"+path)


if __name__ == '__main__':
    app.run()
