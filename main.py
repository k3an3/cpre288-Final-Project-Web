from flask import Flask, render_template, request, jsonify
from models import db, Result, Object, Robot
import sys

sys.path.append('PyRobot')
from command import *
from status import *
from receiver import DebugReceiver, FifoReceiver
from sender import DebugSender

app = Flask(__name__)
global myreceiver
global mysender

@app.route('/', methods=['POST', 'GET'])
def control_center():
  if request.method == 'POST':
    if not ser.isOpen():
      error = "The serial connection is not established"
  return render_template('control_center.html', **locals())

@app.route('/api/getstatus')
def get_status():
    statuses = []
    myreceiver.receive() #Poll for data on serial port or FIFO
    while myreceiver.isNewStatusAvailable():
        s = myreceiver.getStatus()
        statuses.append({
                         'type' : type(s).__name__,
                         'id' : s.command.command_id,
                         'actual' : s.distance_actually_moved,
                         'reason' : s.abort_reason,
                         })
    return jsonify(statuses=statuses if statuses else None)

#TODO: Parameters and stuff
@app.route('/api/moveforward', methods=['POST'])
def move_foward():
    if request.method == 'POST':
        mysender.sendCommand(MoveForwardCommand())
    return ''

#@app.before_request
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
  mysender = DebugSender()
  myreceiver = FifoReceiver(mysender, "receivefifo")
  app.debug = True
  app.run()
