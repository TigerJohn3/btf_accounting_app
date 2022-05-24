# Where database models will be created
from time import timezone
from datetime import datetime
from sqlalchemy import Integer
from . import db # This is the equivalent of saying from website import db
                 # if this is done outside the directory
from flask_login import UserMixin

# Use Notes for now, but this will be changed to be an accounting db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=datetime.now()) # func.now gets current time
    # foreign key is the relationship between user and note
    # the second argument states we MUST pass a user id to this object
    # this is a one-to-many relationship -- one user, many notes
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Note - syntax will be different for many-to-one or many-to-many



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(100))
    # below code allows you to see all notes from each user
    notes = db.relationship('Note') # 'Note' is the note table above


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(150))
    type = db.Column(db.String(100))
    purchase_price = db.Column(db.Integer)
    usd_price = db.Column(db.Integer)
    purchase_type = db.Column(db.String(100))
    date_bought = db.Column(db.DateTime(timezone=True), default=datetime.now())
    currently_owned = db.Column(db.Boolean(), default=True)
    date_sold = db.Column(db.DateTime(timezone=True), default=None)
    sale_price = db.Column(db.Integer, default=None)
    usd_sale_price = db.Column(db.Integer, default=None)
    capital_gain = db.Column(db.Integer, default=None)




# Note from above - class name is LOWERCASE when using the foreign key
#    - first letter of class name is UPPERCASE when using relationship
