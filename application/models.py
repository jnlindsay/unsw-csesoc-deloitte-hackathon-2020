from datetime import datetime
from application import db

class Covid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(200), nullable=False)
    # 0 for not 1 yes
    def __repe__(self):
        return '<Covid New Cases%r>' % self.id

class Flu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(200), nullable=False)
    # 0 for not 1 yes
    def __repe__(self):
        return '<Flu New Cases%r>' % self.id


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
