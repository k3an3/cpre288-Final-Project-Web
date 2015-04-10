from flask import Flask, render_template, request
from utils import *

app = Flask(__name__)
global ser

@app.route('/', methods=['POST', 'GET'])
def control_center():
  if request.method == 'POST':
    pass
  return render_template('control_center.html', **locals())

if __name__ == '__main__':
  ser = serial_init()
  app.debug = True
  app.run()
