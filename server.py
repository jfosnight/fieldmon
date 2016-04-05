from gevent import monkey; monkey.patch_all()

from time import sleep
from bottle import route, run, template, debug, static_file
import sqlite3
import picamera

@route('/stream')
def stream():
    for x in range(0,50):
        yield str(float(x)/10) + "<br>"
        sleep(0.1)
    yield '<br>END<br>'


# Setup for Static Bower Files to be served.
@route('/bower/<file_path:re:.+>')
def bower(file_path):
    return static_file(file_path, "./bower_components")

# Server Index Page
@route('/')
def index():
    return static_file("index.html", ".")


@route('/node')
@route('/node/')
def node():
    return "Node Home Page"

@route('/node/<num>')
def node_id(num):
    return "Node: " + str(num)

@route('/image')
@route('/image/')
def images():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("SELECT * FROM image ORDER BY timestamp ASC")
    rows = c.fetchall()

    return template('images.tpl', images=rows)
    

@route('/image/take')
def take_image():
    yield "Taking Picture<br><br>"

    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("SELECT * FROM image ORDER BY timestamp DESC LIMIT 1")
    row = c.fetchone()

    camera = picamera.PiCamera()
    filename = "image" + str(row[0] + 1).zfill(4) + ".jpg"

    camera.awb_mode = 'off'
    camera.awb_gains = (1.0,0.5)
    
    camera.capture('./images/' + filename)
    camera.close()

    
    c.execute("INSERT INTO image (file_name) VALUES (?)", (filename, ))
    conn.commit()
    conn.close()
    yield "Done"

@route('/image/<filename>')
def image(filename):
    return static_file(filename, "./images")

debug(True)
run(host='0.0.0.0', port=80, reloader=True, server='gevent') #server='bjoern', 
