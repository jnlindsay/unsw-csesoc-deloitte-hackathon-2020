from datetime import datetime
from application import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    # 0 for not 1 yes
    def __repe__(self):
        return '<Covid New Cases%r>' % self.id


class Covid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    num_cases = db.Column(db.Integer, default=0, nullable=False)
    #location = db.Column(db.String(200), nullable=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    # 0 for not 1 yes
    def __repe__(self):
        return '<id %r>' % self.id


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    Covid = db.relationship('Covid', backref='country', lazy=True)
    def __repe__(self):
        return '<country_id %r>' % self.id

