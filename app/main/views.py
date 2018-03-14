from . import main
from ..auth.forms import RegistrationForm, LoginForm
from .forms import CreateTableForm
from flask import render_template, request ,redirect, url_for
from flask_login import login_required,current_user
from config import Config
from ..models import Table, Requests,User, BitlyHelper
import datetime
import itertools

ADMIN_USER = User.objects(email='admin@admin.com')[0]

@main.route('/')
def home():
    registrationform = RegistrationForm()
    return render_template("home.html", loginform=LoginForm(), registrationform=registrationform)

@main.route("/account")
@login_required
def account():
    tables = Table.objects()
    return render_template("account.html", createtableform=CreateTableForm(), tables=tables)

@main.route("/create_table", methods=['POST'])
@login_required
def create_table():
    form = CreateTableForm(request.form)
    if form.validate():
        table = Table(number=form.tablenumber.data, owner=ADMIN_USER)
        table.save()
        url = BitlyHelper().shorten_url(Config.base_url + "newrequest/" + str(table.id))
        table.update(url=url)
        return redirect(url_for('main.account'))
    return render_template("account.html", createtableform=form, tables=Table.objects)


@main.route("/delete_table")
@login_required
def delete_table():
    table = Table.objects(id=request.args.get('tableid'))[0]
    table.delete()
    return redirect(url_for('main.account'))


@main.route("/dashboard")
@login_required
def dashboard():
    now = datetime.datetime.now()
    # owner = User.objects(email=current_user.get_id())[0]
    requests = Requests.objects(owner=ADMIN_USER)
    for req in requests:
        deltaseconds = (now - req['time']).seconds
        req['wait_minutes'] = "{}.{}".format((deltaseconds / 60), str(deltaseconds % 60).zfill(2))
    return render_template("dashboard.html", requests=requests)


@main.route("/newrequest")
@login_required
def new_request():
    table = Table.objects(id=request.args.get('tableid'))[0]
    table.update(empty=False)
    _request = Requests(tableid=table, table_number= table.number, time=datetime.datetime.now(), owner=ADMIN_USER)
    _request.save()

    return redirect(url_for('main.dashboard'))


@main.route('/resolve')
@login_required
def dashboard_resolve():
    request_id = request.args.get("request_id")
    request1 = Requests.objects(id=request_id)[0]

    request.delete()
    return redirect(url_for('main.dashboard'))


