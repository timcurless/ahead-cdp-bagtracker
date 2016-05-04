from flask import Blueprint, render_template

index = Blueprint('index', __name__)


@index.route('/')
def home():
    return render_template('index.html')


@index.route('/status')
def status():
    return render_template('status.html')


@index.route('/manage')
def manage():
    return render_template('manage.html')
