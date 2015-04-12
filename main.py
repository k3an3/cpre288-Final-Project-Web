from flask import Flask, render_template, request
from utils import *
from models import db, Result, Object, Robot

app = Flask(__name__)
global ser

@app.route('/', methods=['POST', 'GET'])
def control_center():
  db.connect()
  event = check_sensor_event()
  if request.method == 'POST':
    if not ser.isOpen():
      error = "The serial connection is not established"
  history_list = Result.select().order_by(Result.time.desc())
  db.close()
  return render_template('control_center.html', **locals())

@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = some_random_string()
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token

if __name__ == '__main__':
  ser = serial_init()
  app.debug = True
  app.run()
