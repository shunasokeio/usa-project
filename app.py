from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)

@app.route('/', methods=["POST", "GET"])
def main():
    return render_template("index.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    return render_template("login.html")

@app.route('/signup', methods=["POST", "GET"])
def signup():
    return render_template("signup.html")

# git add . && git commit -m "message"
# git push -u usa master

if __name__ == "__main__":
    app.run()