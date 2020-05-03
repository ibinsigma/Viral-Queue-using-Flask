from flask import Blueprint, render_template, request 
from flask_login import login_required, current_user
from sqlalchemy import desc
from .models import User,UserEntry
from . import db

#import smtplib


from datetime import datetime
main = Blueprint('main', __name__)



@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
	return render_template('profile.html', name=current_user.firstname)


@main.route('/leaderboard')
def leaderboard() :
	leaders = UserEntry.query.order_by(UserEntry.entries.desc()).limit(10).all()
	print(leaders)
	return render_template('leaderboard.html', leaders=leaders)
