from flask import Flask, render_template, url_for, redirect
from authlib.integrations.flask_client import OAuth
import json
app = Flask(__name__)

oauth = OAuth(app)

app.config['SECRET_KEY'] = "THIS SHOULD BE SECRET"
app.config['GITHUB_CLIENT_ID'] = "77f241282b1eb592b77a"
app.config['GITHUB_CLIENT_SECRET'] = "20ec16101e39c4a07cba437266b5f917f9f6ea97"


github = oauth.register (
  name = 'github',
    client_id = app.config["GITHUB_CLIENT_ID"],
    client_secret = app.config["GITHUB_CLIENT_SECRET"],
    access_token_url = 'https://github.com/login/oauth/access_token',
    access_token_params = None,
    authorize_url = 'https://github.com/login/oauth/authorize',
    authorize_params = None,
    api_base_url = 'https://api.github.com/',
    client_kwargs = {'scope': 'user:email'},
)


# Default route
@app.route('/')
def index():
  return render_template('index.html')


# Github login route
@app.route('/login/github')
def github_login():
    github = oauth.create_client('github')
    redirect_uri = url_for('github_authorize', _external=True)
    return github.authorize_redirect(redirect_uri)


# Github authorize route
@app.route('/login/github/authorize')
def github_authorize():
    github = oauth.create_client('github')
    token = github.authorize_access_token()
    resp = github.get('user').json()
    print("Type of: ",type(resp))
    print(f"\n{resp}\n")
    return render_template('data.html', title="page", data=resp)

if __name__ == '__main__':
  app.run(debug=True)
