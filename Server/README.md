# Server

#### Compile & Install Intiface-Engine


##### -> as root
###### Install dependencies via apt-get
```
apt install libdbus-1-dev pkg-config libudev-dev -y
```
###### Create user
```
useradd -m -s /bin/bash intiface
usermod -a -G sudo intiface
```
###### Login as user
```
su -l intiface
```

##### -> as User (intiface)
```
export USERNAME=intiface
```

## &raquo; Hardware
##### Lovense USB-Dongle
#### - udev rules
```
sudo cp ./system/udev/50-localusb.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
sudo usermod -aG plugdev $USERNAME
```

###### Download this repository
```
git clone https://github.com/Izzy3110/buttplug-mqtt
```


###### Download & Setup cargo (Rust)
```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
. "$HOME/.cargo/env"
```

###### Get intiface-engine source from github
```
mkdir $HOME/src $HOME/intiface-engine
cd $HOME/src
git clone https://github.com/intiface/intiface-engine
cd intiface-engine
```

###### build intiface-engine release
```
cargo build --release
cp -R ./target/release/* $HOME/intiface-engine/
```

###### Getting buttplug source for generating a Device-Config


##### Requirements
 - NodeJS
```
sudo apt-get install -y nodejs npm
```

###### Generate device-config .json
```
export TARGET_DIR=~/intiface-engine
cd ~/src
git clone https://github.com/buttplugio/buttplug
cd buttplug 
cd buttplug/buttplug-device-config
npm i
npm audit fix --force
npm run build:v3
cp ~/src/buttplug/buttplug/buttplug-device-config/build-config/buttplug-device-config-v3.json $TARGET_DIR/
```

##### -> as root
###### Setup systemd-service
```
cp /home/intiface/buttplug-mqtt/Server/system/systemd/intiface_engine.service /etc/systemd/system
systemctl daemon-reload
systemctl --enable --now intiface-engine.service
```

## Troubleshooting 
###### Start Intiface manually
```
su -l intiface
cd ~/intiface-engine
./intiface-engine --websocket-port 12334 --use-lovense-dongle-hid --websocket-use-all-interfaces --log debug --use-device-websocket-server --device-websocket-server-port 12344 --device-config-file buttplug-device-config-v3.json
```
