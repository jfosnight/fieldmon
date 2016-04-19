from gevent import monkey; monkey.patch_all()

from time import sleep
from bottle import route, run, template, debug, static_file, request, redirect
import sqlite3
import tempfile
#import picamera

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

# Pages for Nodes
@route('/node')
@route('/node/')
def node():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM node")
    rows = c.fetchall()

    return template('nodes.tpl', nodes=rows)

@route('/node/new', method='GET')
def node_new():
    return template('node_new.tpl')

@route('/node/new', method='POST')
def node_create():

    name = request.forms.get('name')
    lat = request.forms.get('lat')
    lng = request.forms.get('lng')

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("INSERT INTO node (name, lat, lng) VALUES (?,?,?)", (name, lat, lng, ))
    conn.commit()

    redirect("/node/")


@route('/node/<num>', method='POST')
def node_id(num):
    name = request.forms.get('name')
    lat = request.forms.get('lat')
    lng = request.forms.get('lng')

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("UPDATE node SET name=?, lat=?, lng=? WHERE id=?", (name, lat, lng, num,))
    conn.commit()

    redirect("/node/" + str(num))



@route('/node/<num>')
def node_id(num):
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM node WHERE id = ?", (num, ))
    row = c.fetchone()

    c.execute("SELECT * FROM sensor_data WHERE node_id = ?", tuple(num))
    sensor_data = c.fetchall()

    print sensor_data

    return template('node.tpl', node=row, sensor_data=sensor_data)



## Sensor Data
@route('/node/<num>/data', method='GET')
def node_data(num):
    return template('data_upload.tpl')

@route('/node/<num>/data', method='POST')
def node_data_post(num):
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


    return html



## Pages for images
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


@route('/image/<filename>')
def image(filename):
    return static_file(filename, "./images")


## Startup Server
debug(True)
run(host='0.0.0.0', port=80, reloader=True, server='gevent') #server='bjoern',
