# Buttplug MQTT Bridge (UNIX)
## Control Lovense-Toys via MQTT

### Description
This MQTT bridge application facilitates seamless communication between an MQTT broker and a Lovense toy. 
It processes specific JSON payloads to send commands via Bluetooth using a connected Lovense USB dongle, 
enabling remote control of the toy through standardized MQTT messaging.

### Components 
 - Docker   MQTT-Broker (mosquitto)
 - Server   Intiface-Engine
 - App      MQTT-Bridge

### Installation (UNIX)
 - Install docker.io and docker-compose
 - Start mosquitto
 - Start Server-Backend
 - Start MQTT-Bridge
