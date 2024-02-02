from flask import Flask, render_template, redirect, url_for, session, request
import tweepy
import secrets


secret_key = secrets.token_hex(16)  

app = Flask(__name__)
app.secret_key = secret_key


CONSUMER_KEY = 'your_consumer_key'
CONSUMER_SECRET = 'your_consumer_secret'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, callback='oob')  # Set the callback value to 'oob'
    redirect_url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    return redirect(redirect_url)

@app.route('/callback')
def callback():
    verifier = request.args.get('oauth_verifier')
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    token = session['request_token']
    del session['request_token']

    auth.request_token = token
    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print('Error! Failed to get access token.')

    session['access_token'] = auth.access_token
    session['access_token_secret'] = auth.access_token_secret

    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'access_token' not in session or 'access_token_secret' not in session:
        return redirect(url_for('login'))

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(session['access_token'], session['access_token_secret'])
    api = tweepy.API(auth)

    user = api.me()
    tweets = api.user_timeline(count=10)

    return render_template('dashboard.html', user=user, tweets=tweets)

if __name__ == '__main__':
    app.run(debug=True)
