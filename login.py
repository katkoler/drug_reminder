from flask import Flask, render_template, redirect, url_for, request
from graphiql_request import get_profiles

# importing the already made the application object
from models import app, get_all_drugs, add_text_message

# use decorators to link the function to a url
@app.route('/')
def home():
    drugs = get_all_drugs()
    return render_template('index.html', drugs=drugs)  # return a string

# start the server with the 'run()' method

@app.route("/about")
def about():
    profiles = get_profiles()
    return render_template("about.html", members=profiles, enumerate=enumerate)

@app.route("/sign-up")
def sign_up():
    return render_template("signupform.html")

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route("/subscribe", methods=["POST"])
def subscribe():
    add_text_message(request.values)
    print("OK!!!")
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)
