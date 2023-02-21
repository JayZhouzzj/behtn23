from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///htn.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    email = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'name': self.first_name + " " + self.last_name,
            'company': self.company.name,
            'email': self.email,
            'phone': self.phone,
            'skills': [{
                **userskill.skill.to_dict(), 
                'rating': userskill.rating
            } for userskill in self.skills]
        }

    def __repr__(self):
        return '<User %r>' % self.id

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {'skill': self.name}

    def __repr__(self):
        return '<Skill %r>' % self.id

class UserSkill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, 
        db.ForeignKey('user.id'), nullable=False)
    skill_id = db.Column(db.Integer, 
        db.ForeignKey('skill.id'), nullable=False)
    rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, 
        default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('skills', lazy=False))
    skill = db.relationship('Skill', backref=db.backref('users', lazy=False))

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    people = db.relationship(User, lazy=True,
        backref=db.backref('company', lazy=False))

    def __repr__(self):
        return '<Company %r>' % self.id

@app.route("/")
def hello_world():
    return "<p>Connected!</p>"

@app.route("/users", methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route("/users/<int:user_id>", methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route("/users/<string:email>")
def get_user_by_email(email):
    user = User.query.filter_by(email=email).first_or_404()
    return jsonify(user.to_dict())
