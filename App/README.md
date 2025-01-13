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
## &raquo; Installation steps

#### Install Python Virtual Environment (as root)
```
~$ apt install python-is-python3 python3-venv -y
```

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
