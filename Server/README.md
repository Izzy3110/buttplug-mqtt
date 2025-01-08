# Server

#### Compile & Install Intiface-Engine


##### -> as root
###### Install dependencies via apt-get
```
~$ apt install libdbus-1-dev pkg-config libudev-dev -y
```
###### Create user
```
~$ useradd -m -s /bin/bash intiface
~$ usermod -a -G sudo intiface
```
###### Login as user
```
~$ su -l intiface
```

##### -> as $USERNAME
```
~$ export USERNAME=intiface
```
###### Download & Setup cargo (Rust)
```
~$ curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
~$ . "$HOME/.cargo/env"
```

###### Get intiface-engine source from github
```
~$ mkdir $HOME/src
~$ cd $HOME/src
~/src$ git clone https://github.com/intiface/intiface-engine
~/src$ cd intiface-engine
```

###### build intiface-engine release
```
~/src/intiface-engine$ cargo build --release
~/src/intiface-engine$ cp -R ./target/release/* $HOME/intiface-engine/
```

###### Getting buttplug source for generating a Device-Config


##### Requirements
 - NodeJS
```
sudo apt-get install -y nodejs npm
```

###### Generate device-config .json
```
~$ export TARGET_DIR=~/intiface-engine
~$ cd ~/src
~/src$ git clone https://github.com/buttplugio/buttplug
~/src$ cd buttplug 
~/src/buttplug$ cd buttplug/buttplug-device-config
~/src/buttplug/buttplug/buttplug-device-config$ npm i
~/src/buttplug/buttplug/buttplug-device-config$ npm audit fix --force
~/src/buttplug/buttplug/buttplug-device-config$ npm run build:v3
cp ~/src/buttplug/buttplug/buttplug-device-config/build-config/buttplug-device-config-v3.json $TARGET_DIR/
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

