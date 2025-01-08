# Server

#### Compile & Install Intiface-Engine
##### Download Rust
```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

##### Getting Buttplug for generating a Device-Config
###### Requirements
 - NodeJS
```
apt-get install -y nodejs npm
```

###### Generate device-config .json
```
git clone https://github.com/buttplugio/buttplug
cd buttplug/buttplug-device-config
npm i
npm run build:v3
```
