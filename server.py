from flask import Flask, render_template, session, redirect, request
from database import Database

db = Database()

app=Flask(__name__)
app.secret_key = "CHANGE_THIS_LATER_PLEASE_"

###################################################
def is_logged_in():
    try:
        status = session['logged_in']
        return status
    except KeyError:
        session['logged_in'] = False

###################################################
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

###################################################
@app.route('/login', methods=['POST'])
def log_in():
    if is_logged_in():
        return redirect('/')

    if request.method == 'POST':
        form = request.form
        if 'username' not in form or "password" not in form:
            return redirect('/')

        username=form['username']
        password=form['password']

        if (db.valid_login(username, password)):
            session['logged_in']=True
            session['username']=username

        else:
            return "login failed lmao"
    return redirect('/')

###################################################
@app.route('/')
def home_page():
    if not is_logged_in():
        return render_template("home.html", logged_in=False)
    return render_template("home.html", logged_in=True, user=session['username'])

###################################################
@app.route('/register', methods=['POST', 'GET'])
def register():
    msg="Sign Up!"
    if request.method=='POST':
        form = request.form
        print("Registration:", form)
        if 'username' in form and "password" in form:
            if (db.create_user(form['username'], form['password'])):
                return redirect('/')
            msg="Username taken!"
    return render_template("register.html", header=msg)

###################################################
@app.route('/tweet', methods=['GET'])
def tweet():
    print (request.method)
    if request.method == "GET":
        args = request.args
        print("TWEETING")
        if 'tweet' in args and is_logged_in():
            db.create_tweet(session['username'], args['tweet'])
    return redirect('/')

###################################################
@app.route('/search', methods=["GET"])
def search():
    if request.method == "GET":
        srch = request.args['search']
        r = db.get_users_as_search(srch)
        return render_template("userlist.html", title="Search results", result=r)
    return "ERROR 500: INTERNAL SERVER OOPSIE"

###################################################
@app.route('/follow/<user>')
def follow(user):
    if is_logged_in():
        db.create_follow(session['username'], user)
    return redirect('/')

###################################################
@app.route('/following')
def get_following():
    if is_logged_in():
        r=db.get_followees(session['username'])
        return render_template("userlist.html", title="Following", result=r)

###################################################
@app.route('/followers')
def get_followers():
    if is_logged_in():
        r=db.get_followers(session['username'])
        return render_template("userlist.html", title="Your Followers", result=r)

###################################################

@app.route('/tweets')
def my_tweets():
    tweets_list = db.get_tweets_from_user(session['username'])
    return render_template("tweetlist.html", title="Your Tweets", result=tweets_list)


if __name__ == '__main__':
   app.run(debug = True)
