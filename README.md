# fieldmon
Class Project to develop Field Monitoring Sensor Network

This project will develop an application to run on a companion computer (Raspberry Pi) attached to a UAV (quadcopter) for collecting data from a number of independent sensors distributed on the ground.


## Installation
### Install NodeJS

(From the website)

	curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
	sudo apt-get install -y nodejs

### Install Other Dependencies
	sudo npm install --global bower
	sudo pip install gevent bottle gevent-websocket
	sudo python init_new.py


## AP Setup
SSID: drone  
PW: dronecomm
IP: 192.168.42.1


## Resources
* [Making a Mavlink WiFi bridge using the Raspberry Pi](http://dev.ardupilot.com/wiki/making-a-mavlink-wifi-bridge-using-the-raspberry-pi/)
* [Installing Node JS - Ubuntu](https://nodejs.org/en/download/package-manager/)
* [Ingrafram (IR Photo Processing)](http://infragram.org/)
