from datetime import datetime, time

from flask import Flask, Response, redirect, url_for, request, render_template

app = Flask(__name__)


# @app.route('/hello/<int:id>/')
# def hello_world(**kwargs):
#     return f"Hello <b>{'Quang' if kwargs.get('id', False) == 1 else 'Nhung'}</b>"
# app.add_url_rule('/hello', 'hello', hello_world)

@app.route('/')
def index():
    port = {}
    port.update({
        'date_now': datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    })

    return render_template('index.html', **port)


@app.route('/time_feed')
def time_feed():
    def generate():
        yield datetime.now().strftime("%m/%d/%Y %H:%M:%S")  # return also will work

    return Response(generate(), mimetype='text')


@app.route('/success/<name>', methods=['POST', 'GET'])
def success(name):
    return f"Login success. Welcome {name}!"


@app.route('/login', methods=['POST', 'GET'])
def login():
    user = 'N/A'
    if request.method == 'POST':
        user = request.form['nm']
    else:
        user = request.args.get('rm')
    return redirect(url_for('success', name=user))


@app.route('/guest/<name>')
def guest(name):
    return f"Hello {name}"


@app.route('/hello/<name>')
def hello(name):
    if name == 'admin':
        return redirect(url_for('admin', name))
    return redirect(url_for('guest', name))


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
