import os
from datetime import datetime
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath('__file__'))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "databases/paysys.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class User(db.Model):
    eid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pay_amount = db.Column(db.Integer, primary_key=True)
    joining_date = db.Column(db.Integer, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.name

db.create_all()

@app.route('/', methods=["GET", "POST"])
def home():
	users = None
	if request.form:
			try:
				eid = request.form["eid"]
				name = request.form["name"]
				mail = request.form["mail"]
				pay_amount = request.form["pay_amount"]
				joining_date = request.form["doj"]
				user = User(eid= eid , name= name , email= mail , pay_amount = pay_amount , joining_date = joining_date)
				db.session.add(user)
				db.session.commit()
			except Exception as e:
				print("Failed to add user")
				print(e)
	users = User.query.all()
	return render_template("index.html", users=users)

@app.route("/update", methods=["POST"])
def update():
	if request.form:
		try:
			oldid = request.form.get("old_eid")
			eid = request.form["update_eid"]
			name = request.form["update_name"]
			mail = request.form["update_mail"]
			pay_amount = request.form["update_pay_amount"]
			joining_date = request.form["update_doj"]
			user = User.query.filter_by(eid=oldid).first()
			user.eid = eid
			user.name = name
			user.email = mail
			user.pay_amount = pay_amount
			user.joining_date = joining_date
			db.session.commit()
			return redirect("/")
		except Exception as e:
			print("Failed to update user")
			print(e)
	return redirect("/")


@app.route("/delete", methods=["POST"])
def delete():
	user = None
	if request.form:
		try:
			eid = request.form["del_title"]
			user = User.query.filter_by(eid=eid).first()
			print(user)
			db.session.delete(user)
			db.session.commit()
			return redirect("/")
		except Exception as e:
			print("Failed to delete user")
			print(e)
	return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
