from flask import Flask, render_template, redirect, url_for, request
from graphiql_request import get_profiles

# importing the already made the application object
from models import app, get_all_drugs

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

if __name__ == '__main__':
    app.run(debug=True)
