import urllib.request
import json
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from flask import current_app

from app import db



TOKEN = "cc922578a7a1c6065a2aa91bc62b02e41a99afdb"
ROOT_URL = "https://api-ssl.bitly.com"
SHORTEN = "/v3/shorten?access_token={}&longUrl={}"

class User(db.Document):
    email = db.StringField()
    password_hash = db.StringField()
    confirmed = db.BooleanField()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def gen_comfirm_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({"confirm":self.email})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.email:
            return False
        self.confirmed = True
        self.save()
        return True


    def __repr__(self):
        return 'email:%s'%self.email

    def get_id(self):
        return self.email

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

class Table(db.Document):
    number = db.StringField()
    owner = db.ReferenceField(User)
    url = db.StringField()
    empty = True

class Requests(db.Document):
    tableid = db.ReferenceField(Table)
    table_number = db.StringField()
    time = db.DateTimeField()
    wait_minutes = db.DateTimeField()
    owner = db.ReferenceField(User)


class BitlyHelper:
    """docstring for BitlyHelper"""

    def shorten_url(self, longurl):
        try:
            url = ROOT_URL + SHORTEN.format(TOKEN, longurl)
            response = urllib.request.urlopen(url).read()
            jr = json.loads(response)
            return jr['data']['url']
        except Exception as e:
            raise e
