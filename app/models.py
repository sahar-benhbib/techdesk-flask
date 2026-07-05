from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='employe')  # 'employe' ou 'agent'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    categorie = db.Column(db.String(50))  # ex: "Matériel", "Logiciel", "Accès"
    priorite = db.Column(db.String(20), default='normale')  # basse / normale / haute
    statut = db.Column(db.String(20), default='ouvert')  # ouvert / en_cours / resolu
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    createur = db.relationship('User', backref='tickets')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contenu = db.Column(db.Text, nullable=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    ticket = db.relationship('Ticket', backref='comments')
    auteur = db.relationship('User')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))