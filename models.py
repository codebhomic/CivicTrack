from flask_sqlalchemy import SQLAlchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class IssueCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255))
    status = db.Column(db.String(50), default='Reported')
    category = db.Column(db.String(50))
    distance = db.Column(db.String(10))  # for display (e.g., '2.3 km')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url,
            'status': self.status,
            'category': self.category,
            'distance': self.distance
        }


class Flag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reason = db.Column(db.String(100), nullable=True)  # optional reason
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))


class StatusLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'), nullable=False)
    new_status = db.Column(db.String(30))  # Reported, In Progress, Resolved
    note = db.Column(db.String(255))  # optional admin note
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(20), default='citizen')  # 'citizen', 'admin', 'moderator'
    is_verified = db.Column(db.Boolean, default=False)
    is_banned = db.Column(db.Boolean, default=False)

    issues = db.relationship('Issue', backref='user', lazy=True)
    flags = db.relationship('Flag', backref='user', lazy=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now(datetime.timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)