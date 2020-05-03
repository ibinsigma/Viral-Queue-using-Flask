from flask import Blueprint, render_template, redirect, url_for, request, flash , session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User, UserEntry
from . import db
from email.message import EmailMessage
import smtplib

'''
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
app = Flask(__name__)
admin = Admin(app,name='Control Panel')
'''

auth = Blueprint('auth', __name__)

#admin = Admin(auth,name='Control Panel')


@auth.route('/referred/<code>')
def referred(code) :
    session['referrer'] = code
    return redirect(url_for('auth.signup'))


@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()
    msg = "Your referral link is http://localhost:5000/referred/" + str(email)
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    referrer = session.get('referrer', None)


    userentrycheck = UserEntry.query.filter_by(email=email).first()
    if userentrycheck and userentrycheck.referrer:
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))

    elif referrer :
        print(referrer)
        update_referrer = UserEntry.query.filter_by(email=referrer).first()
        update_referrer.entries += 1

        new_user_entry1 = UserEntry(email=email,referrer=referrer,entries=1)
        db.session.add(new_user_entry1)
        db.session.commit()
    else :
        new_user_entry = UserEntry(email=email,referrer='NULL',entries=1)
        db.session.add(new_user_entry)
        db.session.commit()


    login_user(user, remember=remember)


    # ----------------------------------- Email sending -------------------------------------------------


    msg = EmailMessage()
    msg['Subject'] = 'Link is http://localhost:5000/referred/' + str(email)
    msg['From'] = 'testqversity@gmail.com'
    msg['To'] = email

    msg.set_content('Your referral link is http://localhost:5000/referred/<your-email-address>')

    msg.add_alternative("""\
        <!DOCTYPE html>
        <html>
        <body>
        <h1 style="color:Blue;"><b>Link is in the subject</h1>
        <h2> SHARE YOUR LINK !! </h2>
        <a href="https://www.facebook.com" target="_blank">FACEBOOK</a><br><br>
        <a href="https://www.twitter.com" target="_blank">TWITTER</a>
        </body>
        </html>
        """, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp :
        '''
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        

        

        subject = 'Referral Link'
        body = 'Your referral link is http://localhost:5000/referred/' + str(email)

        msg = f'Subject: {subject}\n\n{body}'

        smtp.sendmail('testqversity@gmail.com', email, msg)
        '''
        smtp.login('testqversity@gmail.com', 'stronger1#')
        smtp.send_message(msg)



    #--------------------------------------------------------------------------------------------------------
    return redirect(url_for('main.profile'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Email address already exists.')
        return redirect(url_for('auth.login'))

    new_user = User(email=email, firstname=firstname, lastname=lastname, password=generate_password_hash(password, method='sha256'))
    #new_user1 = UserEntry( email=email, entries=1)

    db.session.add(new_user)
    #db.session.add(new_user1)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


