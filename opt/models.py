from datetime import datetime
from flask_login import UserMixin
from opt import db, login_manager, app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer



@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)



    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"



class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    #foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


#to define the category of underlying/Instrument
class Instcategory(db.Model):
    __tablename__ = 'instcategory'
    id = db.Column(db.Integer, primary_key=True)
    catname=db.Column(db.String(20), nullable=False)
    catdesc=db.Column(db.String(20), nullable=False)
    
    
    #relationships
    instname= db.relationship('Instrument', backref='category', lazy=True)
    
    def __repr__(self):
        return f"Instcategory('{self.cname}')"



class Instrument(db.Model):
    __tablename__ = 'instrument'
    id = db.Column(db.Integer, primary_key=True)
     #underyling name/description
    type_inst=db.Column(db.String(20), nullable=False)
    desc_inst=db.Column(db.String(20), nullable=False)
    sym_inst=db.Column(db.String(8), nullable=False)

    #relationships
    opt_list=db.relationship('Options', backref='underlying', lazy=True)
    #foreign keys
    catid = db.Column(db.Integer, db.ForeignKey('instcategory.id'), nullable=False)
   
    
    def __repr__(self):
        return f"Instrument('{self.type_inst}')"

class Options(db.Model):
    __tablename__ = 'options'
    id = db.Column(db.Integer, primary_key=True)
     #underyling name/description
    ul_name=db.Column(db.String(20), nullable=False)
    #underlying symbol
    ul_symbol=db.Column(db.String(4), nullable=False)
       #underlying symbol
    ul_price=db.Column(db.String(4), nullable=False)
    #date of calculation
    date_calc=db.Column(db.DateTime, default=datetime.utcnow) 
    #strike price
    opt_strike=db.Column(db.String(4), nullable=False)
    #symbol of option
    opt_sym=db.Column(db.String(8), default=datetime.utcnow)
    # expiry date of option
    exp_date=db.Column(db.DateTime, default=datetime.utcnow) 
    #date of estimated value. for instance in 10 days
    date_val=db.Column(db.DateTime, default=datetime.utcnow) 

    #Foreign Keys
    inst_id = db.Column(db.Integer, db.ForeignKey('instrument.id'), nullable=False)

    def __repr__(self):
        return f"Options('{self.opt_sym}','{self.opt_strike}', '{self.exp_date}')"

