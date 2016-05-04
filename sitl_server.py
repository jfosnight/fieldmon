print "Start simulator (SITL)"
from dronekit_sitl import SITL
import time

#sitl = SITL('/home/pi/ardupilot/ArduCopter/ArduCopter.elf')
sitl = SITL()
sitl.download('copter', '3.3', verbose=True)
sitl_args = ['-I0', '--model', 'quad', '--home=37.720305,-97.270831,428,353']
sitl.launch(sitl_args, await_ready=True, restart=True)

while True:
    time.sleep(0.1)
