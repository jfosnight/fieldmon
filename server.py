from gevent import monkey; monkey.patch_all()

from time import sleep
from bottle import route, run, template, debug, static_file, request, redirect, abort, Bottle
import sqlite3
import tempfile

import dronekit

try:
    import picamera
except:
    pass

app = Bottle()

@app.route('/stream')
def stream():
    for x in range(0,50):
        yield str(float(x)/10) + "<br>"
        sleep(0.1)
    yield '<br>END<br>'


# Setup for Static Bower Files to be served.
@app.route('/bower/<file_path:re:.+>')
def bower(file_path):
    return static_file(file_path, "./bower_components")

# Server Index Page
@app.route('/')
def index():
    return static_file("index.html", ".")

# Pages for Nodes
@app.route('/node')
@app.route('/node/')
def node():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM node")
    rows = c.fetchall()

    return template('nodes.tpl', nodes=rows)

@app.route('/node/new', method='GET')
def node_new():
    return template('node_new.tpl')

@app.route('/node/new', method='POST')
def node_create():

    name = request.forms.get('name')
    lat = request.forms.get('lat')
    lng = request.forms.get('lng')

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("INSERT INTO node (name, lat, lng) VALUES (?,?,?)", (name, lat, lng, ))
    conn.commit()

    redirect("/node/")


@app.route('/node/<num>', method='POST')
def node_id(num):
    name = request.forms.get('name')
    lat = request.forms.get('lat')
    lng = request.forms.get('lng')

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("UPDATE node SET name=?, lat=?, lng=? WHERE id=?", (name, lat, lng, num,))
    conn.commit()

    redirect("/node/" + str(num))



@app.route('/node/<num>')
def node_id(num):
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM node WHERE id = ?", (num, ))
    row = c.fetchone()

    c.execute("SELECT * FROM sensor_data WHERE node_id = ?", tuple(num))
    sensor_data = c.fetchall()

    return template('node.tpl', node=row, sensor_data=sensor_data)



## Sensor Data
@app.route('/node/<num>/data', method='GET')
def node_data(num):
    return template('data_upload.tpl')

@app.route('/node/<num>/data', method='POST')
def node_data_post(num):
    global droneContinue

    temp_file = tempfile.TemporaryFile()

    if request.files.data:
        request.files.data.save(temp_file)
    else:
        temp_file.write(request.body.read())

    temp_file.seek(0)
    html = "<table>"
    data = []
    for line in temp_file.readlines():
        line = line.strip()
        values = line.split(",")
        if len(data) == 0:
            values.append("node_id")
        else:
            values.append(num)
        data.append(tuple(values))

        html += "<tr>"
        for v in values:
            html += "<td>" + v + "</td>"
        html += "</tr>"

    html += "</table>"

    header = data.pop(0)
    placeholder = "("
    i = 0
    while(i < len(header) - 1):
        placeholder += "?,"
        i += 1
    placeholder += "?)"

    sqlText = "INSERT INTO sensor_data " + str(header) + " VALUES " + str(placeholder)

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.executemany(sqlText, data)
    conn.commit()

    if dronePause:
        droneContinue = True
    return html



## Pages for images
@app.route('/image')
@app.route('/image/')
def images():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("SELECT * FROM image ORDER BY timestamp ASC")
    rows = c.fetchall()

    return template('images.tpl', images=rows)


@app.route('/image/take')
def take_image():

    json_response = {}
    try:

        conn = sqlite3.connect("data.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute("SELECT * FROM image ORDER BY timestamp DESC LIMIT 1")
        row = c.fetchone()

        if row is None:
            filename = "image0000.jpg"
        else:
            filename = "image" + str(row[0] + 1).zfill(4) + ".jpg"

        camera = picamera.PiCamera()

        sleep(1.5)

        camera.capture('./images/' + filename)
        camera.close()


        c.execute("INSERT INTO image (file_name) VALUES (?)", (filename, ))

        c.execute("SELECT * FROM image WHERE id = ?", (c.lastrowid, ))
        body = {}
        row = c.fetchone()
        print row

        conn.commit()

        for key in row.keys():
            body[key] = row[key]

        json_response['status'] = "success"
        json_response['body'] = body

        conn.close()
    except Exception as e:
        json_response['status'] = "error"
        json_response['body'] = e.args
    return json_response


@app.route('/image/<filename>')
def image(filename):
    return static_file(filename, "./images")


global vehicle
global controlThread
global controlStatus
global dronePause
global droneContinue


controlStatus = ""

import threading
def drone_flight():
    global controlStatus, droneContinue, dronePause
    if not vehicle:
        controlStatus = "Disconnected"
        return "drone not connected"

    flight_path = get_flight_path()

    controlStatus = "Arming"
    ## Arm Vehcile
    vehicle.mode = dronekit.VehicleMode("GUIDED")
    vehicle.airspeed = 5
    if not vehicle.armed:
        vehicle.armed = True
        while not vehicle.armed:
            sleep(0.1)

    if vehicle.mode.name != "GUIDED":
        controlStatus = "Not in guided mode."
        return "Error"

    controlStatus = "Takeoff"
    ## Takeoff to 20 meters
    vehicle.simple_takeoff(20)

    controlStatus = "Waiting to reach altitude"
    ## Wait for it to reach Altitude
    while (vehicle.location.local_frame.down or 0) * -1 < 20 * 0.95:
        sleep(0.1)


    ## Fly to waypoint
    #controlStatus = "Flying to Waypoint"
    #a_location = dronekit.LocationGlobalRelative(-35.36300, 149.166022, 30)
    #vehicle.simple_goto(a_location)

    #while vehicle.location.global_frame.lat > -35.362990  and vehicle.location.global_frame.lon < 149.16600:
    #   sleep(0.1)

    # dronePause = True
    # droneContinue = False

    controlStatus = "Waiting for Upload"
    sleep(5)
    # while not droneContinue:
    #     sleep(0.1)
    # droneContinue = False

    controlStatus = "Returning Home"
    vehicle.mode = dronekit.VehicleMode("RTL")

    while vehicle.system_status.state == "ACTIVE":
        sleep(0.1)

    controlStatus = "Mission Complete"
    return "Done"



def get_flight_path():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM node")
    rows = c.fetchall()

    flight_path = []
    for row in rows:
        flight_path.append({"lat" : row['lat'], "lng" : row['lng']})

    return flight_path


vehicle = None
@app.route('/drone/connect')
def drone_connect():
    global vehicle
    if not vehicle:
        vehicle = dronekit.connect("tcp:127.0.0.1:5760", wait_ready=True)
        return "Connected to Drone"
    else:
        return "Already Connected"


@app.route('/drone/disconnect')
def drone_disconnect():
    global vehicle
    if vehicle:
        vehicle.close()
        vehicle = None
        return "Drone is Disconnected"
    else:
        return "Drone was already disconnected"


@app.route('/drone')
@app.route('/drone/')
def drone_status():
    return template("drone.tpl")


@app.route("/drone/takeoff")
def drone_takeoff():
    if not vehicle:
        return "Drone Not Connected"


    vehicle.armed = True
    # Set mode to guided - this is optional as the goto method will change the mode if needed.
    vehicle.mode = dronekit.VehicleMode("GUIDED")

    vehicle.airspeed = 5

    while not vehicle.armed:
        sleep(0.1)

    vehicle.simple_takeoff(20)

    # Set the target location in global-relative frame
    #a_location = dronekit.LocationGlobalRelative(-35.35000, 149.166022, 30)
    #vehicle.simple_goto(a_location)
    return "Taking Off"


@app.route("/drone/move")
def drone_move():
    if not vehicle:
        return "Drone Not Connected"

    # Set mode to guided - this is optional as the goto method will change the mode if needed.
    vehicle.mode = dronekit.VehicleMode("GUIDED")

    #vehicle.airspeed = 5

    if not vehicle.armed:
        vehicle.armed = True
        while not vehicle.armed:
            sleep(0.1)


    # Set the target location in global-relative frame
    a_location = dronekit.LocationGlobalRelative(-35.36200, 149.166022, 30)
    vehicle.simple_goto(a_location)
    return "Flight Path Set"


@app.route("/drone/rtl")
def drone_rtl():
    vehicle.mode = dronekit.VehicleMode("RTL")
    return "Returning Home"

@app.route("/drone/mission")
def drone_mission():
    threading.Thread(target=drone_flight, name='drone').start()
    return "Mission Started"

@app.route('/drone/status')
def drone_status():
    return template("drone_status.tpl")

@app.route("/ws/drone/status")
def ws_drone_status():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            if vehicle:
                status = ""
                status += "Location: %s <br>" % vehicle.location.global_frame
                status += "Local Location: %s <br>" % vehicle.location.local_frame
                status += "Down: %f<br>" % (vehicle.location.local_frame.down or 0)
                #status += "Altitude: %s <br>" % vehicle.location.global_frame.alt
                status += " GPS: %s <br>" % vehicle.gps_0
                status += " Battery: %s <br>" % vehicle.battery
                status += " Last Heartbeat: %s <br>" % vehicle.last_heartbeat
                status += " Is Armable?: %s <br>" % vehicle.is_armable
                status += " Armed: %s <br>" % vehicle.armed
                status += " System status: <b>%s</b> <br>" % vehicle.system_status.state
                status += " Mode: %s <br>" % vehicle.mode.name
                status += "<br>"
                status += "Mission Status: %s<br>" % controlStatus

                wsock.send(status)
                sleep(0.25)
            else:
                wsock.close()
                return

        except WebSocketError:
            break

@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    print "Websocket Initialized"
    print wsock

    i = 0
    while True:
        try:
            if wsock.closed:
                print "Socket Closed"
                return

            wsock.send(str(i))
            sleep(1)
            i += 1

        except WebSocketError:
            print "Connection Closed Unexpectedly"
            break

@app.route('/socket')
def index_2():
    return template("websocket.tpl")


debug(True)

from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
server = WSGIServer(("0.0.0.0", 80), app,
                    handler_class=WebSocketHandler)
server.serve_forever()

## Startup Server
#debug(True)
#run(host='0.0.0.0', port=80, reloader=True, server='gevent') #server='bjoern',
