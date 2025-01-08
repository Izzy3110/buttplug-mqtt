# App
## &raquo; Python & OS

#### Tested with Python 
- 3.12.4
- 3.11.2

#### Tested with Debian 
```
Debian GNU/Linux (bookworm)
6.1.0-27-amd64
```

## &raquo; Hardware
##### Lovense USB-Dongle
#### - udev rules
```
cp ./system/udev/50-localusb.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && udevadm trigger

sudo usermod -aG plugdev $USERNAME
```
## &raquo; Installation steps
#### Setup virtual environment
```
python -m venv venv
source ./venv/bin/activate
```

#### Install Python packages
```
pip install -r requirements
```

#### Start Program
```
python ./main.py
```