from flask import Flask, render_template, session, redirect, url_for, request
from psycopg2 import Error
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, Boolean, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
 
app = Flask(__name__)
app.secret_key = "CSIA"

engine = create_engine('postgresql://u7feclortrbds4:pc99371329189ecc6173f01b8ccd6bfe4e2fcd50723ccfa773a5b7396af0d20e1@c1i13pt05ja4ag.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d97m4fsiubgdkl', echo = True)

#engine = create_engine("sqlite:///db.sqlite3") this is for testing databse
Base = declarative_base()
Session_maker = sessionmaker(bind=engine)

#creating tables
class users(Base): 
    __tablename__ = "users" 
    user_id = Column(Integer, primary_key = True, autoincrement="auto")
    name = Column(String)
    email = Column(String)


class locations(Base):
   __tablename__ = "locations" 
   user_id = Column(Integer, primary_key = True)
   latitude = Column(Float)
   longitude = Column(Float) 


class friends(Base): 
    __tablename__ = "friends"
    user_id = Column(Integer, primary_key = True)
    friends = Column(Array)


@app.route('/', methods=["POST", "GET"])
def main():
    if request.method == "POST": 
        Session = Session_maker()
        email = str(request.form["email"])
        try: 
            found_user = Session.query(users).filter_by(email=email).all()
            if len(found_user) == 0: 
                return redirect(url_for("signup", no_user="true"))
            else: 
                session["email"] = email
                return redirect(url_for("home"))
        except (Exception, Error) as error:
                print("Error while trying to log a user in", error)
                Session.close()
                return render_template("login.html", error=error)    
    else:
        return render_template("login.html")

@app.route('/home', methods=["POST", "GET"])
def home():
    if "email" in session:
        email = session["email"]
        Session = Session_maker()
        try:
            array = []
            records = Session.query(friends).filter_by(email=email).all()
            Session.close()
            return render_template("index.html", array=array)
        except (Exception, Error) as error:
                print("Error while trying to load the home page", error)
                Session.close()
                return render_template("index.html", array=["ERROR HAS OCCURED"])
    else: 
        return redirect(url_for("main", loginrequired="true"))


@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST": 
        Session = Session_maker()
        email = str(request.form["email"])
        name = str(request.form["name"])
        try: 
            found_user = Session.query(users).filter_by(email=email).all()
            if len(found_user) == 0: 
                user=users(name=name, email=email)
                session.add(task)
                session.commit()
                session.close()
                return redirect(url_for("main"))
            else: 
                session["email"] = email
                return redirect(url_for("main"), userexists="true")
        except (Exception, Error) as error:
                print("Error while trying to log a user in", error)
                Session.close()
                return render_template("signup.html", error=error)    
    else:
        return render_template("signup.html")

# git add . && git commit -m "message"
# git push -u usa master

if __name__ == "__main__":
    app.run()