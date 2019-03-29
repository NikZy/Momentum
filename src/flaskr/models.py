
from flask import url_for
from flaskr import db, auth
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


#make_searchable() # for search

#class Job_applicant_query(BaseQuery, SearchQueryMixin):
    #pass

def set_password(self, password):
    self.password_hash = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(self.password_hash, password)

#Model class of Uploads_Tbl
class UploadFiles(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    fileName = db.Column(db.String(100))
    createdon = db.Column(db.DateTime)

    def __init__(self, fileName, createdon):
        self.fileName = fileName
        self.createdon = createdon

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(50))
    frontpage_post = db.relationship('Frontpage_post', backref='AdminUser', lazy=True)
    def generate_data():
        admin = AdminUser(username="SuperAdmin", email="admin@admin.no")
        set_password(admin, "admin")
        db.session.add(admin)

        try:
            db.session.commit()
            print("ADDED AdminUSer")
        except:
            db.session.rollback()

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Job_applicant(db.Model):
    __tablename__ = 'Job_applicant'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False, default="")
    last_name=db.Column(db.String(120), nullable=False, default="")
    birth_date=db.Column(db.Date)
    email = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))
    CV=db.Column(db.String(500))
    former_jobs=db.Column(db.String(200))
    profile_picture = db.Column(db.String(30), default="profile_man.jpg")

    tags = db.relationship('Tag', secondary='tag_map', backref=db.backref('Job_applicant', lazy='dynamic'))
    location=db.Column(db.String(100))
    markerText=db.Column(db.String(100))

    def generate_data():
        job_applicant1=Job_applicant(first_name="Hanniballer",last_name="aldri", birth_date=datetime.datetime.now(), email="guns@gemale.com",CV="alt", former_jobs="morendin", profile_picture="MrGuns.jpeg",  location="høyskoleringen 3", markerText="P15")
        set_password(job_applicant1, "passord123")
        job_applicant1.tags.append(Tag.query.first())
        job_applicant2=Job_applicant(first_name="Harald",last_name="Ødegård", birth_date=datetime.datetime.now(), email="fast@sf.no",CV="Hanniballes kunnskap < Meg", former_jobs="Sjefen til Asgeir", profile_picture="Halvor.png",  location="Trondheim", markerText="Eier alt her")
        set_password(job_applicant2, "123")
        job_applicant2.tags.append(Tag.query.first())
        db.session.add(job_applicant2)
        try:
            db.session.commit()
            print("ADDED JOB APPLICANTS")
        except:
            db.session.rollback()

    def __repr__(self):
        return '<User {}>'.format(self.email)
    def __str__(self):
        return '<User {}>'.format(self.email)

class Startup(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(120), nullable=False, default="")
    email=db.Column(db.String(50), nullable=False, default="")
    startup_date=db.Column(db.Date)
    description=db.Column(db.String(300))
    password_hash = db.Column(db.String(128))
    location = db.Column(db.String(100))
    markerText = db.Column(db.String(100))
    tags = db.relationship('Tag', secondary='tag_map', backref=db.backref('startup', lazy='dynamic'))
    job_positions = db.relationship('Job_position', backref='publishded_by', lazy=True)

    profile_picture = db.Column(db.String(30), default="profile_man.jpg")


    def generate_data():
        import datetime
        db.session.add(dummydataStartUp("Mesla", "melon_dusk", "Vi lager biler som kjører på møkk", "San Fransisco", 1, "Mesla.png"))
        db.session.add(dummydataStartUp("Den Kebabnorske Bank", "bankfloss", "Whallah, vi låner deg floos brur", "Oslo", 3, "KebabnorskBank.png"))
        db.session.add(dummydataStartUp("MoTube", "motube", "Forum for kuvideoer", "San Fransisco", 1, "MoTube.png"))
        db.session.add(dummydataStartUp("KanAkademi", "notkhan", "Free education 4 stupid people", "San Fransisco", 15, "KanAkademi.png"))
        db.session.add(dummydataStartUp("AiDiabitus", "diabetus", "Vi lager en AI som sier at du er feit og holder på å få diabetes", "San Fransisco", 6, "AiDiabitus.png"))
        db.session.add(dummydataStartUp("IkkeA", "billigmobler", "Billig møbler om har alt for vanskelige instrukser", "stockholm", 8, "IkkeA.png"))
        try:
            db.session.commit()
            print("ADDED STARTUPS")
        except:
            db.session.rollback()


    def _repr_(self):
        return '<user{}>'.format(self.email)
    def __str__(self):
        return "Startup: {}".format(self.email)

class Job_position(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    description=db.Column(db.String(400))
    deadline=db.Column(db.DATETIME)
    title=db.Column(db.String(32), nullable=False)
    contact_mail=db.Column(db.String(32))
    tags = db.relationship('Tag', secondary='tag_map', backref=db.backref('job_positions', lazy='dynamic'))
    startup = db.Column(db.Integer, db.ForeignKey(Startup.id), nullable=False)

    profile_picture = db.Column(db.String(30), default="profile_man.jpg")

    def generate_data():
        job_position1=Job_position(description="kjip",deadline=auth.to_datetimefield("2019-03-15"),title="Vi trenger en MaskinMøkk designer",startup=1, contact_mail= "kontakt_oss@melon_dusk.no")
        job_position1.tags.append(Tag.query.filter_by(id=1).one())
        job_position1.profile_picture="Mesla.png"
        taggers=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        job_position2=Job_position(description="dette er din jobb, bare føl på den", deadline=auth.to_datetimefield("1227-08-27"),title="u the person", startup=2, contact_mail="sjengis.khjen@murdi.commm")
        job_position2.tags=(Tag.query.filter(Tag.id.in_(taggers[0:15:2])).all())
        job_position2.profile_picture="KebabnorskBank.png"

        job_position3 = dummydataJobPosition("best","spør noen andre", "mhm@krak","2019-03-15",3)
        job_position3.tags=Tag.query.filter(Tag.id.in_(taggers[1:5])).all()
        job_position3.profile_picture="MoTube.png"

        job_position4 = dummydataJobPosition("mindre bra","ikke vet jeg da hehe", "enseriøs@mann.yass","2019-03-15", 3)
        job_position4.tags=Tag.query.filter(Tag.id.in_(taggers[15:-5])).all()
        job_position4.profile_picture="MoTube.png"
        

        job_position5 = dummydataJobPosition("senior douche", "ikke min jobb", "svarer.aldri@birken.no", "2019-03-15", 6)
        job_position5.tags = Tag.query.filter(Tag.id.in_(taggers[7:14:2])).all()
        job_position5.profile_picture="IkkeA.png"

        job_position6 = dummydataJobPosition("minor bug", "4evaeva", "det.slutter@aldri.se", "2019-03-15", 5)
        job_position6.tags = Tag.query.filter(Tag.id.in_(taggers[::3])).all()
        job_position6.profile_picture="AiDiabitus.png"

        job_position7 = dummydataJobPosition("juicepresser", "grind det shitten der", "cevita.ce@vita.no", "2019-03-15", 4)
        job_position7.tags = Tag.query.filter(Tag.id.in_(taggers[::4])).all()
        job_position7.profile_picture="KanAkademi.png"

        job_position8 = dummydataJobPosition("PT","Så lenge du er ripped går det fint", "mail?.jegharbare@msn.jeg","2019-03-15", 3)
        job_position8.tags=Tag.query.filter(Tag.id.in_(taggers[::15])).all()
        job_position8.profile_picture="MoTube.png"


        db.session.add(job_position2)
        db.session.add(job_position1)
        db.session.add(job_position3)
        db.session.add(job_position4)
        db.session.add(job_position5)
        db.session.add(job_position6)
        db.session.add(job_position7)

        try:
            db.session.commit()
            print("ADDED JOB_POSITIONS")
        except:
            db.session.rollback()

    def _repr_(self):
        return '<position {}>'.format(self.title)
    def __str__(self):
        return '<position {}>'.format(self.title)

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    tagname= db.Column(db.String(32))

    def generate_data():
        tag1 = Tag(tagname="IT")
        tag2 = Tag(tagname="Landbruk")
        tag3 = Tag(tagname="Økonomi og markedsføring")
        tag4 = Tag(tagname="Bygg og anlegg")
        tag5 = Tag(tagname="Off-shore")
        tag6 = Tag(tagname="Miljø")
        tag7 = Tag(tagname="Helse og sosial")
        tag8 = Tag(tagname="Design og arkitektur")
        tag9 = Tag(tagname="Elektro")
        tag10 = Tag(tagname="Hotell og reise")
        tag11 = Tag(tagname="Transport og Logistikk")
        tag12 = Tag(tagname="Musikk og kunst")
        tag13 = Tag(tagname="Sport og friluftsliv")
        tag14 = Tag(tagname="Non-profit")
        tag15 = Tag(tagname="Utdanning")
        tag16 = Tag(tagname="Journalistikk")
        db.session.add(tag1)
        db.session.add(tag2)
        db.session.add(tag3)
        db.session.add(tag4)
        db.session.add(tag5)
        db.session.add(tag6)
        db.session.add(tag7)
        db.session.add(tag8)
        db.session.add(tag9)
        db.session.add(tag10)
        db.session.add(tag11)
        db.session.add(tag12)
        db.session.add(tag13)
        db.session.add(tag14)
        db.session.add(tag15)
        db.session.add(tag16)

        try:
            db.session.commit()
            print("ADDED  TAGS")
        except:
            db.session.rollback()
    def _repr_(self):
        return '<Tag: {}>'.format(self.tagname)
    def __str__(self):
        return '<Tag: {}>'.format(self.tagname)



class Frontpage_post(db.Model):
    __tablename__ = 'frontpage_post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, default="")
    body_text=db.Column(db.String(300))
    author = db.Column(db.Integer, db.ForeignKey(AdminUser.id), nullable=False, default=1)
    made=db.Column(db.Date, default=datetime.datetime.now())
    image = db.Column(db.String(100), default="https://mdbootstrap.com/img/Photos/Others/images/10.jpg")

    # legge til img

    tags = db.relationship('Tag', secondary='tag_map', backref=db.backref('Frontpage_posts', lazy='dynamic'))

    def generate_data():
        post1 = Frontpage_post(title="Velkommen til Momentum!", body_text="Velkommen til Momentum, den nyeste nettsiden for startup-bedrifter og andre startup-interesserte! Lag en bruker som enten startup eller jobbsøker, og kom i kontakt med potensielle arbeidsgivere eller -takere. Som investor kan man søke seg frem til bedrifter eller sektorer man ønsker å investere i.", author=1, image="https://pilbox.themuse.com/image.jpg?url=https%3A%2F%2Fassets.themuse.com%2Fuploaded%2Fattachments%2F16096.jpg%3Fv%3De7619af4a2d0f77ea20a926ecc96ef3f15bec659f629e29195b8b1abbf5af147&bg=0fff&h=367&mode=fill&prog=1&w=750")
        post1.tags.append(Tag.query.first())

        post2 = Frontpage_post(title="Trondheim blir første by med 5G",body_text="Telenor lanserte i fjor høst Norges første 5G-pilot i Kongsberg. Siden den gang har det blitt annonsert en pilot til i Elverum og nå har selskapet bestemt hvor 5G-nettet skal skrus på først når det skal bygges ut som et ordinært mobilnett og ikke et testnett. Valget for hvor man først kan ta i bruk neste generasjons mobilnett falt på Trondheim. Fra og med i sommer begynner installasjonen av de første basestasjonene.",author=1, image="https://www.ntnu.no/documents/1265258993/1265296258/trondheim_eriksson_1200x400.jpg/85607465-6942-441a-9db7-6ce4696cd22e?t=1446629973278")
        post2.tags.append(Tag.query.filter_by(id=2).one())

        post5 = Frontpage_post(title="du er verdt det", body_text="det er på tide å stå opp, se seg selv i speilet og si 'gjør det heller i morgen, fordi du fortjener det'",author=1,image="https://i.imgur.com/duXNC.jpg" )
        post6 = Frontpage_post(title="tingen er å ha det", body_text="mange klager på å ikke ha ting, og det er da såklart et problem som kan påvirke hverdagen fra en tid til en annen når man minst tenker på det. gjerrr det bish", image="https://pbs.twimg.com/media/Cfe8Wo0WcAEv-1-.jpg")
        post3 = Frontpage_post(title="Bergens nye tech-fabrikk: Bygger startups i turbofart",body_text="Startup-fabrikken New ble grunnlagt av flere profilerte tech-personligheter i Bergen i fjor sommer. De siste månedene har New utviklet konsepter på løpende bånd. Blant annet en brennhet transport-startup. Vi har forsøkt å fjerne alt «hazzle» med å ha bil. Vi skal tilby hele bredden av transportmidler, basert på kundenes brukermønster, forteller Hans Kristian Aas, daglig leder av Imove.", author=1, image="https://www.travelmarket.dk/gfx/tm_2011/flight/big/21-BGO.jpg")
        post4 = Frontpage_post(title="Kahoot på børs før sommeren", body_text="I torsdagens investorpresentasjon varslet edtech-startupen at de kom til å bli notert på Merkur Market i løpet av andre kvartal. Vi velger å gå på børs for å ha muligheten til å hente kapital, for å kunne finansiere den ikke-organiske veksten, som tidvis vil ha et kapitalbehov. I forbindelse med børsnoteringen har vi ikke diskutert hvorvidt vi skal hente mer kapital, sier Furuseth i en artikkel i Finansavisen.",author=1, image="https://shifter.no/wp-content/uploads/2017/11/kahoot2.jpg")
        db.session.add(post1)
        db.session.add(post2)
        db.session.add(post3)
        db.session.add(post4)
        db.session.add(post5)
        db.session.add(post6)
        

        db.session.commit()
        try:
            print("ADDED FRONTPAGE_POSTS")
        except:
            print("ERROR ADDING TAGS")
            db.session.rollback()

    def _repr_(self):
        return '<{}>'.format(self.title)
    def __str__(self):
        return '<{}>'.format(self.title)



tag_map= db.Table(
    'tag_map',
    db.Column('tag_id', db.Integer, db.ForeignKey(Tag.id)),
    db.Column('frontpage_post_id', db.Integer, db.ForeignKey(Frontpage_post.id)),
    db.Column('job_applicant_id', db.Integer, db.ForeignKey(Job_applicant.id)),
    db.Column('startup_id', db.Integer, db.ForeignKey(Startup.id)),
    db.Column('job_position_id', db.Integer, db.ForeignKey(Job_position.id))

)
'''class Tags_map(db.Model):

    __tablename__= 'tags_map'
    id = db.Column(db.Integer, primary_key=True)

    frontpage_post_id = db.Column( db.Integer, db.ForeignKey(Frontpage_post.id))
    tags_id= db.Column( db.Integer, db.ForeignKey(Tag.id))

'''
import click
from flaskr import app
@app.cli.command()
def seed_db ():
    db.drop_all()
    db.create_all()
    Tag.generate_data()
    Frontpage_post.generate_data()
    AdminUser.generate_data()
    Startup.generate_data()
    Job_applicant.generate_data()
    Job_position.generate_data()
    print("populated databse")
@app.cli.command()
def drop_db():
    db.drop_all()
    print("Deleted the database")
@app.cli.command()
def create_db():
    db.create_all()
    print("Created db")





def dummydataStartUp(name, mail, description,location, tag, img):
    startup = Startup(name=name ,email=(name+"@startup.no"), startup_date=datetime.datetime.now(),description=description, location=location, markerText="Her er vi", profile_picture=img)
    startup.tags.append(Tag.query.filter_by(id=tag).one())
    set_password(startup, "test")
    return startup

def dummydataJobPosition(title, description, contact_mail, deadline, startup):
    job_position=Job_position(title=title,contact_mail=contact_mail,description=description,deadline=auth.to_datetimefield(deadline), startup=startup)
    return job_position
