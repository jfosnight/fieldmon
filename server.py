from gevent import monkey; monkey.patch_all()

from time import sleep
from bottle import route, run, template, debug, static_file, request, redirect, abort, Bottle
import sqlite3
import tempfile
import time

from gcf import gcf_degrees

import dronekit

try:
    import picamera
except:
    pass

app = Bottle()

#droneAddress = "/dev/ttyACM0"
droneAddress = "tcp:127.0.0.1:5760"

targetAlt = 10

nodeList = {}
## Example List
#nodeList[1] = {'uploaded': False, 'lat': 37.7203396, 'lon': -97.2715991}
#nodeList[2] = {'uploaded': False, 'lat': 37.7201564, 'lon': -97.271533}
#nodeList[3] = {'uploaded': False, 'lat': 37.720754, 'lon': -97.270692}

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
def node_id_post(num):
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


@app.route('/node/<num>/delete')
def node_id_delete(num):
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("DELETE FROM node WHERE id = ?", tuple(num))

    conn.commit()

    return redirect("/node/")

## Sensor Data
@app.route('/node/<num>/data', method='GET')
def node_data(num):
    return template('data_upload.tpl')


## Sensor Delete Data
@app.route('/node/<num>/data/delete', method='GET')
def node_data_delete(num):
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("DELETE FROM sensor_data WHERE node_id = ?", tuple(num))

    conn.commit()

    return node_id(num)

@app.route('/node/<num>/data', method='POST')
def node_data_post(num):
    global nodeList

    temp_file = tempfile.TemporaryFile()

    if request.files.data:
        request.files.data.save(temp_file)
    else:
        temp_file.write(request.body.read())


    temp_file.seek(0)
    print temp_file.read(200)

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

    if int(num) in nodeList:
        nodeList[int(num)]['uploaded'] = True
        print "Node Uploaded"
    return html



## Pages for images
@app.route('/image')
@app.route('/image/')
def images():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
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

        sleep(1)

        camera.capture('./images/' + filename)
        camera.close()

        if vehicle:
            lat = vehicle.location.global_frame.lat
            lng = vehicle.location.global_frame.lon
            alt = round(vehicle.location.global_frame.alt, 2)
            heading = vehicle.heading
        else:
            lat = None
            lng = None
            alt = None
            heading = None

        c.execute("INSERT INTO image (file_name, lat, lng, alt, heading) VALUES (?, ?, ?, ?, ?)", (filename, lat, lng, alt, heading))

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
global controlStatus

controlStatus = ""

import threading
def drone_flight():
    global controlStatus, nodeList
    if not vehicle:
        controlStatus = "Disconnected"
        return "drone not connected"

    get_node_list()

    controlStatus = "Arming"
    ## Arm Vehcile
    vehicle.mode = dronekit.VehicleMode("GUIDED")
    while vehicle.mode != "GUIDED":
        sleep(0.1)

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
    vehicle.simple_takeoff( targetAlt )

    controlStatus = "Waiting to reach altitude"
    ## Wait for it to reach Altitude
    while (vehicle.location.local_frame.down or 0) * -1 < targetAlt * 0.95:
        sleep(0.1)


    ## Fly to waypoints
    for node in nodeList:
        if vehicle.mode.name != "GUIDED":
            controlStatus = "Not in guided mode"
            return "Not in guided mode"

        print "Node %d" %(node)

        if nodeList[node]['uploaded'] == False:
            loc = dronekit.LocationGlobalRelative(nodeList[node]['lat'], nodeList[node]['lon'], targetAlt)
            vehicle.simple_goto(loc)

            ## Used for timer to prevent waiting too long.
            watchDog = False
            cameraTimer = time.time()
            cameraEnable = 5
            while True:
                if vehicle.mode.name != "GUIDED":
                    controlStatus = "Not in guided mode"
                    return

                if nodeList[node]['uploaded'] == True:
                    break

                distance = gcf_degrees(nodeList[node]['lat'], nodeList[node]['lon'], vehicle.location.global_frame.lat, vehicle.location.global_frame.lon)
                if distance < 5 and watchDog == False:
                    watchDog = True
                    watchDogStart = time.time()
                    #  Only take one more picture.
                    cameraEnable -= 1

                if watchDog:
                    elapsedTime = time.time() - watchDogStart
                    if elapsedTime > 90:
                        break
                    controlStatus = "Waiting for data from node %d.  Elapsed Time: %.2f" % (node, elapsedTime)
                else:
                    controlStatus = "Flying to node %d.  Distance: %.2f m" % (node, distance)

                if time.time() - cameraTimer > 2 and cameraEnable > 0:
                    print "Take Picture"
                    if cameraEnable != 5:
                        cameraEnable -= 1
                    cameraTimer = time.time()

                sleep(0.1)


            # watchDogStart = time.time()
            # while nodeList[node]['uploaded'] == False and time.time() - watchDogStart < 90  and vehicle.mode.name == "GUIDED":
            #     distance = distanceToNode = gcf_degrees(nodeList[node]['lat'], nodeList[node]['lon'], vehicle.location.global_frame.lat, vehicle.location.global_frame.lon)
            #     controlStatus = "Flying to node %d.  Distance: %.2f m" % (node, distance)
            #     sleep(0.1)

    if vehicle.mode.name != "GUIDED":
        controlStatus = "Not in guided mode."
        return "Error"

    controlStatus = "Returning Home"
    vehicle.mode = dronekit.VehicleMode("RTL")

    while vehicle.system_status.state == "ACTIVE":
        sleep(0.1)

    controlStatus = "Mission Complete"
    return "Done"



def get_node_list():
    global nodeList
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM node")
    rows = c.fetchall()

    #flight_path = []
    nodeList = {}
    for row in rows:
        nodeList[int(row['id'])] = {'uploaded': False, 'lat' : float(row['lat']), "lon" : float(row['lng'])}
        #flight_path.append({"lat" : row['lat'], "lng" : row['lng']})


vehicle = None
@app.route('/drone/connect')
def drone_connect():
    global vehicle
    if not vehicle:
        try:
    	    vehicle = dronekit.connect(droneAddress, wait_ready=True)
            return "Connected to Drone"
        except Exception as e:
            return "Unable to Connect.  %s" %e
    else:
        return "Already Connected"


@app.route('/drone/disconnect')
def drone_disconnect():
    global vehicle
    if vehicle:
        vehicle.close()
        vehicle = None
        return "Disconnected"
    else:
        return "Disconnected"


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
                status += "Lat: %s, Long: %s, Alt: %s<br>" %(vehicle.location.global_frame.lat, vehicle.location.global_frame.lon, vehicle.location.global_frame.alt)
                #status += "Location: %s <br>" % vehicle.location.global_frame
                status += "Relative Pos: north: %.2f m, east: %.2f m, height: <b>%.2f m</b><br>" % (vehicle.location.local_frame.north or 0, vehicle.location.local_frame.east or 0, (vehicle.location.local_frame.down or 0) * -1)
                status += "Heading: %s" % vehicle.heading
                #status += "Local Location: %s <br>" % vehicle.location.local_frame
                #status += "Down: %f<br>" % (vehicle.location.local_frame.down or 0)
                #status += "Altitude: %s <br>" % vehicle.location.global_frame.alt
                status += " GPS: %s <br>" % vehicle.gps_0
                #status += " Battery: %s <br>" % vehicle.battery
                status += " Last Heartbeat: %s <br><br>" % vehicle.last_heartbeat
                status += " Is Armable?: "
                if vehicle.is_armable:
                    status += "<div class='uk-badge uk-badge-success'>True</div>"
                else:
                    status += "<div class='uk-badge uk-badge-danger'>False</div>"
                status += "<br>"
                #status += " Is Armable?: %s <br>" % vehicle.is_armable
                status += "Armed: "
                if vehicle.armed:
                    status += "<div class='uk-badge uk-badge-success'>True</div>"
                else:
                    status += "<div class='uk-badge uk-badge-warning'>False</div>"
                status += "<br>"
                #status += " Armed: %s <br>" % vehicle.armed
                status += " Status: <b>%s</b> <br>" % vehicle.system_status.state
                status += " Mode: <b>%s</b> <br>" % vehicle.mode.name
                status += "<br>"
                status += "Mission Status: <b>%s</b><br>" % controlStatus

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

print "Server Started"

## Startup Server
#debug(True)
#run(host='0.0.0.0', port=80, reloader=True, server='gevent') #server='bjoern',
