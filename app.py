from datetime import datetime, time

from flask import Flask, Response, redirect, url_for, request, render_template, session

app = Flask(__name__)
app.secret_key = 'Any random Text'


# @app.route('/hello/<int:id>/')
# def hello_world(**kwargs):
#     return f"Hello <b>{'Quang' if kwargs.get('id', False) == 1 else 'Nhung'}</b>"
# app.add_url_rule('/hello', 'hello', hello_world)

@app.route('/')
def index():
    port = {}
    port.update({
        'date_now': datetime.now().strftime("%m/%d/%Y %H:%M:%S"),
    })
    user_name = session.get('user_name', False)
    if not user_name:
        return render_template('login.html')

    port.update({
        'user_name': user_name
    })

    return render_template('index.html', **port)


@app.route('/time_feed')
def time_feed():
    def generate():
        yield datetime.now().strftime("%m/%d/%Y %H:%M:%S")  # return also will work

    return Response(generate(), mimetype='text')


@app.route('/result', methods=['POST', 'GET'])
def result():
    user = 'N/A'
    if request.method == 'POST':
        user = request.form['nm']
    else:
        user = request.args.get('rm')
    port = {}
    port.update({
        'points': {'phy': 20, 'che': 60, 'maths': 70},
        'user': user
    })

    return render_template('result.html', **port)


@app.route('/login', methods=['POST', 'GET'])
def login():
    # check already login
    if request.method == 'POST':
        session.update({'user_name': request.form['user_name']})
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_name')
    return redirect(url_for('index'))


@app.route('/guest/<name>')
def guest(name):
    return f"Hello {name}"


@app.route('/hello/<name>')
def hello(name):
    if name == 'admin':
        return redirect(url_for('admin', name))
    return redirect(url_for('guest', name))

@app.route('/clock')
def clock():
    return render_template('clock.html')

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
