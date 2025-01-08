# Server

#### Compile & Install Intiface-Engine
##### Download Rust
```
export USERNAME=local_user
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
mkdir -p /home/$USERNAME/intiface-engine
cd /usr/src
git clone https://github.com/intiface/intiface-engine
sudo cp -R /usr/src/intiface-engine/target/release/* /home/$USERNAME/intiface-engine/
```

##### Getting Buttplug for generating a Device-Config
###### Requirements
 - NodeJS
```
sudo apt-get install -y nodejs npm
```

###### Generate device-config .json
```
export TARGET_DIR=/home/$USERNAME/intiface-engine
cd /usr/src
git clone https://github.com/buttplugio/buttplug
cd buttplug/buttplug-device-config
npm i
npm run build:v3
sudo mkdir -p $TARGET_DIR
cp <config>.json $TARGET_DIR/
```


###### Setup systemd-service
```
root      #   cp ./system/systemd/intiface-engine.service /etc/systemd/system/
root      #   systemctl daemon-reload
root      #   systemctl --enable --now intiface-engine.service
```

###### Start Intiface manually
```
$USERNAME #   cd /home/$USERNAME/intiface-engine
$USERNAME #   ./intiface-engine --websocket-port 12334 --use-lovense-dongle-hid --websocket-use-all-interfaces --log debug --use-device-websocket-server --device-websocket-server-port 12344 --device-config-file buttplug-device-config-v3.json
```

