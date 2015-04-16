from flask import Flask, render_template, request, jsonify
import sys
import serial

sys.path.append('PyRobot')
from command import *
from status import *
from receiver import *
from sender import *

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
        print s.distance_actually_moved
        statuses.append({
                         'id' : s.command.command_id,
                         'result' : s.actualResultString(),
                         'code' : s.abort_reason,
                         'string' : s.abortReasonString(),
                         })
    return jsonify(statuses=statuses if statuses else None)

#TODO: Parameters and stuff
@app.route('/api/moveforward', methods=['POST'])
def move_foward():
    if request.method == 'POST':
        distance = num(request.data.split("=")[1])
        distance = distance if distance and distance > 0 and distance < 5000 else 200
        print distance
        mysender.sendCommand(MoveForwardCommand(distance))
    return ''

@app.route('/api/movereverse', methods=['POST'])
def move_reverse():
    if request.method == 'POST':
        distance = num(request.data.split("=")[1])
        distance = distance if distance and distance > 0 and distance < 5000 else 200
        print distance
        mysender.sendCommand(MoveReverseCommand(distance))
    return ''

@app.route('/api/rotateclockwise', methods=['POST'])
def rotate_clockwise():
    if request.method == 'POST':
        degrees = num(request.data.split("=")[1])
        degrees = degrees if degrees and degrees > 0 and degrees <= 360 else 90
        print degrees
        mysender.sendCommand(RotateClockwiseCommand(degrees))
    return ''

@app.route('/api/rotatecounterclockwise', methods=['POST'])
def rotate_counterclockwise():
    if request.method == 'POST':
        degrees = num(request.data.split("=")[1])
        degrees = degrees if degrees and degrees > 0 and degrees <= 360 else 90
        print degrees
        mysender.sendCommand(RotateCounterclockwiseCommand(degrees))
    return ''

@app.route('/api/sendscan', methods=['POST'])
def begin_scan():
    if request.method == 'POST':
        mysender.sendCommand(BeginScanCommand())
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

def num(s):
    try:
        return int(s)
    except ValueError:
        return None

app.jinja_env.globals['csrf_token'] = generate_csrf_token

if __name__ == '__main__':
  if 'debug' in sys.argv:
     mysender = DebugSender()
     myreceiver = FifoReceiver(mysender, 'tempfifo')
  else:
     ser = serial.Serial('/dev/rfcomm0', 38400, timeout=0, writeTimeout=0)
     mysender = PySerialSender(ser)
     myreceiver = PySerialReceiver(mysender, ser)
  app.debug = True
  app.run(host='0.0.0.0')
