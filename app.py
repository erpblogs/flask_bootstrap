import os
from datetime import datetime, time

from flask import Flask, Response, redirect, url_for, request, render_template, session, abort, flash
from werkzeug import secure_filename

app = Flask(__name__)
app.secret_key = 'Any random Text'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS


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
    # if session.get('user_name', False) and session.get('password', False):
    #     return redirect(url_for('index'))
    if request.method == 'POST':
        if request.form['user_name'] == 'admin' and request.form['password'] == '1':
            session.update({'user_name': request.form['user_name'], 'password': request.form['password']})
            flash('You were successfully logged in')
            return redirect(url_for('index'))
        # else:
        #     return abort(401)
        else:
            error = 'Invalid username or password. Please try again!'
            flash(error, category='error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.get('user_name', False) and session.pop('user_name')
    session.get('password', False) and session.pop('password')
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


@app.route('/upload', methods=['GET', 'POST'])
def uploader():
    return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        name = request.form['name']
        files = request.files.getlist('file')
        i = 0
        for file in files:
            i += 1
            if file.filename == '':
                flash('No file selected for uploading')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                if name:
                    filename = ".".join([name + str(i), filename.split('.')[-1]])

                file.save(os.path.join(f"{ROOT_DIR}\\store", filename))

            else:
                flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
                return redirect(request.url)
        flash('File successfully uploaded')
        return 'file uploaded successfully'


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)
