from app import db

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(64), index=True, unique=True)
    role = db.Column(db.String(64), index=True)
    company = db.Column(db.String(64), index=True)
    division = db.Column(db.String(64), index=True)
    location = db.Column(db.String(64), index=True)
    phone_number = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True)
    link_vcf = db.Column(db.String(64), index=True)


    def __repr__(self):
        return '<User {}>'.format(self.username)
