import os
from forms import AddForm, DelForm, AddOwner
from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SECRET_KEY"] = "yes change it"

# SQL Database section

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'\
    + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)

# Models


class Puppy(db.Model):
    __tablename__ = 'puppies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    owner = db.relationship('Owner', backref='puppy', uselist=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        if self.owner:
            return f"#: {self.id} --Puppy Name: {self.name} --Owner: {self.owner.name}"
        else:
            return f"#: {self.id} --Puppy Name: {self.name}"


class Owner(db.Model):
    __tablename__ = 'owners'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    puppy_id = db.Column(db.Integer, db.ForeignKey('puppies.id'))

    def __init__(self, name, puppy_id):
        self.name = name
        self.puppy_id = puppy_id

    def __repr__(self):
        return f"Owner Name: {self.name}"

# view funtions


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add_pup():
    form = AddForm()

    if form.validate_on_submit():
        name = form.name.data
        new_pup = Puppy(name)
        db.session.add(new_pup)
        db.session.commit()
        flash(f"You just added a puppy {name.capitalize()}")
        return redirect(url_for('list_pup'))

    return render_template('add.html', form=form)


@app.route('/list')
def list_pup():
    puppies = Puppy.query.all()
    return render_template('list.html', puppies=puppies)


@app.route('/delete', methods=["GET", "POST"])
def del_pup():
    form = DelForm()
    if form.validate_on_submit():
        id = form.id.data
        pup = Puppy.query.get(id)
        db.session.delete(pup)
        db.session.commit()
        flash(f"You just deleted puppy: {pup.name.capitalize()}")

        return redirect(url_for('list_pup'))
    return render_template('delete.html', form=form)


@app.route('/addOwner', methods=['GET', 'POST'])
def add_owner():
    form = AddOwner()
    if form.validate_on_submit():
        pup_id = form.pup_id.data
        name = form.name.data
        new_owner = Owner(name, pup_id)
        db.session.add(new_owner)
        db.session.commit()
        pup_name = Puppy.query.get(pup_id)
        flash(f"You just added {name.capitalize()} as the owner of {pup_name.name}")
        return redirect(url_for('list_pup'))
    return render_template('addOwner.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
