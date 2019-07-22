from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField


class AddForm(FlaskForm):

    name = StringField('Name of Puppy: ')
    submit = SubmitField('Add Puppy')


class DelForm(FlaskForm):

    id = IntegerField("id number of Puppy to Remove")
    submit = SubmitField('Remove Puppy')


class AddOwner(FlaskForm):

    name = StringField('Name of Owner: ')
    pup_id = IntegerField("id number of Puppy to Add Owner:")
    submit = SubmitField('Add Owner:')
