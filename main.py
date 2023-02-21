from flask import Flask, jsonify, request
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
    email = db.Column(db.String(255), unique=True, nullable=False)
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

@app.route("/users/<int:user_id>", methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    if 'name' in request.json:
        user.first_name = request.json['name'].split()[0]
        user.last_name = request.json['name'].split()[1]
    if 'email' in request.json:
        user.email = request.json['email']
    if 'phone' in request.json:
        user.phone = request.json['phone']

    if 'company' in request.json:
        old_company = user.company
        new_company = Company.query \
            .filter_by(name=request.json['company']).first()
        if new_company is None:
            new_company = Company(name=request.json['company'])
            db.session.add(new_company)
        user.company = new_company

    if 'skills' in request.json:
        for old_user_skill in UserSkill.query.filter_by(user_id=user.id).all():
            db.session.delete(old_user_skill)

        for user_skill_data in request.json['skills']:
            skill_name = user_skill_data['skill']
            skill_rating = user_skill_data['rating']
            skill = Skill.query.filter_by(name=skill_name).first()

            if skill is None:
                skill = Skill(name=skill_name)
                db.session.add(skill)

            user_skill = UserSkill(
                user=user, skill=skill, rating=skill_rating)
    db.session.commit()
    return jsonify(user.to_dict())

@app.route("/users/<string:email>", methods=['PUT'])
def update_user_by_email(email):
    user = User.query.filter_by(email=email).first_or_404()
    return update_user(user.id)
