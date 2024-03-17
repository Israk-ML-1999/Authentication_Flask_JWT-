from flask import Flask, request, jsonify, make_response, \
    render_template, session
from datetime import datetime, timedelta
from functools import wraps
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f9dfba4c14e74cb7a8b2da8ad2d40588'


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('token')
        print(token)
        if not token:
            return jsonify({'Alert!': 'token is missing'}), 401
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
        except:
            return jsonify({'Alert!': 'Invalid token'}), 403

        return func(*args, **kwargs)
    return decorated


# Home
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return 'Logged in currently'


@app.route('/public')
def public():
    return 'For Public'


@app.route('/authenticated')
@token_required
def authenticated():
    return 'JWT is verified. Welcome to dashboard'


# Login
@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == '123456':
        session['logged_in'] = True
        token = jwt.encode({
            'user': request.form['username'],
            'expiration': str(datetime.utcnow() + timedelta(seconds=120))

        }, app.config['SECRET_KEY'], algorithm='HS256')
        # return jsonify({'token': jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')})
        return jsonify({'token': token})

    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm:"Authentication Failed"'})


if __name__ == "__main__":
    app.run(debug=True)
