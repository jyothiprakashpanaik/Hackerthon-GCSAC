from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

# Configrations
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://admin:admin@127.0.0.1/tracker"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
db1 = SQLAlchemy(app)


class Data(db.Model):
	sno = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(100))
	name = db.Column(db.String(100))
	topic = db.Column(db.String(100))
	deadline = db.Column(db.DateTime)
	nextclass = db.Column(db.DateTime)

	def __init__(self,code,name,topic,deadline,nextclass):
		self.code = code
		self.name = name
		self.topic = topic
		self.deadline = deadline
		self.nextclass = nextclass






@app.route("/")
def home() :
	all_data = Data.query.all()
	return render_template("index.html",assignments = all_data)



@app.route('/insert', methods = ['POST'])
def insert():

	if request.method == "POST":
		code = request.form["code"]
		name = request.form["name"]
		topic = request.form["topic"]
		deadline = request.form["deadline"]
		nextclass = request.form["nextclass"]

		my_data = Data(code, name, topic, deadline, nextclass)
		db.session.add(my_data)
		db.session.commit()

		flash("Assignment Add Successfully")

		return redirect(url_for('home'))


@app.route("/update" , methods=["GET","POST"])
def update():

	if request.method == "POST":
		my_data = Data.query.get(request.form.get('sno'))
		my_data.code = request.form["code"]
		my_data.name = request.form["name"]
		my_data.topic = request.form["topic"]
		my_data.deadline = request.form["deadline"]
		my_data.nextclass = request.form["nextclass"]

		db.session.commit()
		flash("Assignment Updated Successfully")

		return redirect(url_for('home'))


@app.route("/help" , methods=["GET","POST"])
def help():

	if request.method == "POST":
		my_data = Data.query.get(request.form.get('sno'))
		# my_data.code = request.form["code"]
		# my_data.name = request.form["name"]
		# my_data.topic = request.form["topic"]
		# my_data.deadline = request.form["deadline"]
		# my_data.nextclass = request.form["nextclass"]

		# db.session.commit()
		flash("Your Dought Sent Successfully")

		return redirect(url_for('home'))

@app.route('/delete/<sno>/', methods = ['GET', 'POST'])
def delete(sno):
	my_data = Data.query.get(sno)
	db.session.delete(my_data)
	db.session.commit()
	flash("Assignment Deleted Successfully")

	return redirect(url_for("home"))



@app.route('/done/<sno>/', methods = ['GET', 'POST'])
def done(sno):
	my_data = Data.query.get(sno)
	db.session.delete(my_data)
	db.session.commit()
	flash("Assignment is Completed Successfully")

	return redirect(url_for("home"))




if __name__ == "__main__":
	app.run(debug=True)