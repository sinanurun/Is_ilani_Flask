from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os

YUKLEME_KLASORU = 'static/yuklemeler'
UZANTILAR = set(['png', 'jpg', 'jpeg', 'gif','pdf'])

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yerel_is_rehberi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = YUKLEME_KLASORU
app.debug = True
db = SQLAlchemy(app)
dbsession = db.session()

class Yonetici(db.Model):

    yonetici_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    yonetici_adi_soyadi = db.Column(db.String(50), nullable=False)
    yonetici_tc = db.Column(db.String(11), unique=True, nullable=False)
    yonetici_sifre = db.Column(db.String(10), nullable=False)
    yonetici_email = db.Column(db.String(50))
    yonetici_tel = db.Column(db.String(12))
    yonetici_durum = db.Column(db.Integer, nullable=False)

class Isyeri(db.Model):
    isyeri_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    isyeri_adi = db.Column(db.String(50), nullable=False)
    isyeri_yonetici_adi_soyadi = db.Column(db.String(30), nullable=False)
    isyeri_tc = db.Column(db.String(11), unique=True, nullable=False)
    isyeri_sifre = db.Column(db.String(10), nullable=False)
    isyeri_email = db.Column(db.String(20))
    isyeri_tel = db.Column(db.String(15))
    isyeri_adres = db.Column(db.String(50))
    isyeri_durum = db.Column(db.Integer, nullable=False)
    isyeri_foto = db.Column(db.String(500), default="")
    yonetici_id = db.Column(db.Integer, db.ForeignKey('yonetici.yonetici_id'), nullable=False)
    yoneticiid = db.relationship('Yonetici', backref=db.backref('isveren_yonetici', lazy=True))

class Isci(db.Model):
    isci_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    isci_adi_soyadi = db.Column(db.String(30), unique=True, nullable=False)
    isci_tc = db.Column(db.String(11), unique=True, nullable=False)
    isci_sifre = db.Column(db.String(10), nullable=False)
    isci_cinsiyet = db.Column(db.Integer, nullable=False)
    isci_dogum_tarihi = db.Column(db.DateTime, nullable=False)
    isci_mezuniyet = db.Column(db.Integer, db.ForeignKey('mezun.mezun_id'), nullable=False)
    mezun = db.relationship('Mezun', backref=db.backref('mezuniyet_durumu', lazy=True))
    isci_askerlik = db.Column(db.Integer, db.ForeignKey('askerlik.askerlik_id'), nullable=False)
    askerlik = db.relationship('Askerlik', backref=db.backref('askerlik_durumu', lazy=True))
    isci_email = db.Column(db.String(50))
    isci_tel = db.Column(db.String(15))
    isci_adres = db.Column(db.String(150))
    isci_durum = db.Column(db.Integer, nullable=False)
    yonetici_id = db.Column(db.Integer, db.ForeignKey('yonetici.yonetici_id'), nullable=False)
    yoneticiid = db.relationship('Yonetici', backref=db.backref('isci_yonetici', lazy=True))
    isci_meslek_idler = db.Column(db.String(500), default="")
    isci_foto = db.Column(db.String(500), default="")
    isci_ozgecmis = db.Column(db.String(500), default="")


class Ilan(db.Model):
    ilan_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    ilan_baslik = db.Column(db.String(50))
    ilan_icerik = db.Column(db.String(500))
    isyeri_id = db.Column(db.Integer, db.ForeignKey('isyeri.isyeri_id'), nullable=False)
    isyeri = db.relationship('Isyeri', backref=db.backref('ilan_veren', lazy=True))
    yonetici_id = db.Column(db.Integer, db.ForeignKey('yonetici.yonetici_id'), nullable=False)
    yoneticiid = db.relationship('Yonetici', backref=db.backref('ilan_yonetici', lazy=True))
    ilan_tarihi = db.Column(db.DateTime, nullable=False, default=datetime.date(datetime.today()))
    basvuran_idler = db.Column(db.String(500),default="")
    meslek_idler = db.Column(db.String(500),default="")
    anahtarkelime_idler = db.Column(db.String(500),default="")
    ilan_durum = db.Column(db.Integer, nullable=False)


class Mezun(db.Model):
    mezun_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    mezun_adi = db.Column(db.String(50))

class Askerlik(db.Model):
    askerlik_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    askerlik_adi = db.Column(db.String(15))

class Meslek(db.Model):
    meslek_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    meslek_adi = db.Column(db.String(15))

class Anahtarkelime(db.Model):
    anahtarkelime_id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    anahtarkelime_adi = db.Column(db.String(30))


# veri tabanını oluşturmak için tabloyu oluşturmak için
db.create_all()