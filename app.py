## getting an error when trynna log in, it says the table is not created. might be something wrong with the link, the original link directly from heroku does not work. 

from flask import Flask, render_template, session, redirect, url_for, request
from psycopg2 import Error
from sqlalchemy import create_engine, Column, Integer, String, Float
try:
    from sqlalchemy.dialects.postgresql import ARRAY
    print("Import successful!")
except ImportError as e:
    print(f"Import failed: {e}")
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
app = Flask(__name__)
app.secret_key = 'usa-project'  # Add a secret key for session management
engine = create_engine('postgresql+psycopg2://u7feclortrbds4:pc99371329189ecc6173f01b8ccd6bfe4e2fcd50723ccfa773a5b7396af0d20e1@c1i13pt05ja4ag.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d97m4fsiubgdkl', echo=True)
Base = declarative_base()
Session_maker = sessionmaker(bind=engine)
#engine = create_engine('postgresql+psycopg2://user:password@localhost/dbname')
# Creating tables
class users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement="auto")
    name = Column(String)
    email = Column(String)

class locations(Base):
    __tablename__ = "locations"
    user_id = Column(Integer, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)

class friends(Base):
    __tablename__ = "friends"
    user_id = Column(Integer, primary_key=True)
    friends = Column(ARRAY(Integer))

@app.route('/', methods=["POST", "GET"])
def main():
    if request.method == "POST":
        session_instance = Session_maker()
        email = str(request.form["email"])
        try:
            found_user = session_instance.query(users).filter_by(email=email).all()
            session_instance.close()
            if len(found_user) == 0:
                return redirect(url_for("signup", message="plssignup"))
            else:
                session["email"] = email
                return redirect(url_for("home", message="login successful"))
        except (Exception, Error) as error:
            print("Error while trying to log a user in", error)
            session_instance.close()
            return render_template("login.html", message=error)
    else:
        return render_template("login.html", message="plslogin")

@app.route('/home', methods=["POST", "GET"])
def home():
    if "email" in session:
        email = session["email"]
        session_instance = Session_maker()
        try:
            records = session_instance.query(friends).filter_by(email=email).all()
            session_instance.close()
            return render_template("index.html", message="loggedin")
        except (Exception, Error) as error:
            print("Error while trying to load the home page", error)
            session_instance.close()
            return render_template("index.html", message=error)
    else:
        return redirect(url_for("main", message="loginrequired"))

@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        session_instance = Session_maker()
        email = str(request.form["email"])
        name = str(request.form["name"])
        try:
            found_user = session_instance.query(users).filter_by(email=email).all()
            if len(found_user) == 0:
                user = users(name=name, email=email)
                session_instance.add(user)
                session_instance.commit()
                session_instance.close()
                return redirect(url_for("main", message="accountcreated"))
            else:
                session["email"] = email
                session_instance.close()
                return redirect(url_for("main", message="userexists"))
        except (Exception, Error) as error:
            print("Error while trying to sign up a user", error)
            session_instance.close()
            return render_template("signup.html", message=error)
    else:
        return render_template("signup.html", message="welcometosignup")

if __name__ == "__main__":
    # Ensure tables are created
    try:
        Base.metadata.create_all(engine)
        print("Tables created successfully.")
    except Exception as e:
        print("Error creating tables:", e)
    app.run(debug=True)
