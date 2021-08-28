from flask import Flask, session, redirect, url_for, request
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/debug', methods=['GET', 'POST'])
def debug():
    if request.method == 'POST':
        print('SESSION:', session)
    print('REQUEST:', request)
    return 'Check console'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
