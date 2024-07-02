from flask import Flask, render_template, session, redirect, url_for, request


app = Flask(__name__)
app.secret_key = "rufreern"



@app.route('/', methods=["POST", "GET"])
def main():
    return render_template("login.html")    




if __name__ == "__main__":
    app.run()


#git and connecting to github stuff 
#https://docs.github.com/en/get-started/importing-your-projects-to-github/importing-source-code-to-github/adding-locally-hosted-code-to-github

