from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Ticket, Comment

main = Blueprint('main', __name__)
@main.route('/')
@login_required
def home():
    if current_user.role == 'agent':
        tickets = Ticket.query.order_by(Ticket.date_creation.desc()).all()
    else:
        tickets = Ticket.query.filter_by(user_id=current_user.id).order_by(Ticket.date_creation.desc()).all()

    return render_template('home.html', tickets=tickets)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            return render_template('login.html', erreur="Identifiants incorrects")

    return render_template('login.html')


@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/ticket/nouveau', methods=['GET', 'POST'])
@login_required
def nouveau_ticket():
    if request.method == 'POST':
        titre = request.form['titre']
        description = request.form['description']
        categorie = request.form['categorie']
        priorite = request.form['priorite']

        ticket = Ticket(
            titre=titre,
            description=description,
            categorie=categorie,
            priorite=priorite,
            user_id=current_user.id  )
        db.session.add(ticket)
        db.session.commit()

        return redirect(url_for('main.home'))

    return render_template('nouveau_ticket.html')

@main.route('/ticket/<int:id>', methods=['GET', 'POST'])
@login_required
def detail_ticket(id):
    ticket = Ticket.query.get(id)

    if request.method == 'POST':
        contenu = request.form['contenu']

        commentaire = Comment(
            contenu=contenu,
            ticket_id=ticket.id,
            user_id=current_user.id
        )
        db.session.add(commentaire)
        db.session.commit()

        return redirect(url_for('main.detail_ticket', id=ticket.id))

    return render_template('detail_ticket.html', ticket=ticket)

@main.route('/ticket/<int:id>/statut', methods=['POST'])
@login_required
def changer_statut(id):
    if current_user.role != 'agent':
        return "Accès refusé : réservé aux agents IT", 403

    ticket = Ticket.query.get(id)
    ticket.statut = request.form['statut']
    db.session.commit()

    return redirect(url_for('main.detail_ticket', id=ticket.id))