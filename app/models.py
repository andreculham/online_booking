from sqlalchemy import ForeignKey, text
from app import db
from datetime import datetime

class Aplikasi(db.Model):
    __tablename__ = 'aplikasi'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), index=True, nullable=False)
    def __repr__(self):
        return self.name

class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key = True)
    no_ref = db.Column(db.String(60))
    aplikasi_id = db.Column(db.Integer, db.ForeignKey('aplikasi.id'), nullable = True)
    aplikasi = db.relationship('Aplikasi')
    kamar = db.Column(db.String(60))
    nasabah = db.Column(db.String(60))
    check_in_date = db.Column(db.Date)
    check_out_date = db.Column(db.Date)
    status = db.Column(db.String(60))
    penghasilan = db.Column(db.Integer)
    pengeluaran = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.now(), server_default=text("CURRENT_TIMESTAMP"))
