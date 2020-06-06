## Duster - Particulate Matter Concentration analyzer
## Code shifted to bitbucket:
## https://bitbucket.org/kszewc/duster/src/master/

Driver and simple web app application for Raspberry PI and Grove hm3301 sensor.
This is a first version  - tested only on Raspberry PI 4.

### Requrements

The library needs Python3 with pip and pigpiod.
Both available in Raspbian.

### Installation

The library is composed of three component: the hm3301 driver, simple sampler, and simple Flask based web app.
The preferred way of running is to call `sampler.py` and `webapp.py` separately. 
By default the data is stored in the sqlite3 database.
The application parameters can be changed in `config.py`.

Before installing, install required python modules:
> pip install -r requrements.txt

The prefered way is to use virtualenv.

#### Connecting Raspberry Pi and hm3301.

The connection of Raspberry PI with hm3301 is straightforward, the I2C bus is used.
The driver assumes that SDA at pin 2, SCL at 3, I2C address is 0x40.
These values can be changed in `config.py`.

#### Running sampler.py

Before running `sampler.py`, the pigpiod client need to be run:
> sudo pigpiod

Then, sampler can be run using simply:
> python sampler.py

However, preferred way is to use it in background using nohup or create systemd service.

#### Running webapp.py

The web application can be run just by calling:
> python webapp.py

It serves the application by default Flask server in port 8080.

However, the Flask server is designed for developing and testing purposes so it is better not to use in production environment.

The preferred way is to use Gunicorn:
> gunicorn -b your_ip:your_port webapp:app

Similarly to sampler, it is better to use nohup or systemd service to run this app in backround.

### Acknowladgements

The project is served under MIT license.

For plotting, the Chart.js library is used (MIT License): https://www.chartjs.org/

The driver has been inspired by https://github.com/switchdoclabs/SDL_Pi_HM3301 project. 
Please also look at their great article here: https://www.switchdoc.com/2020/02/tutorial-air-quality-on-the-raspberry-pi-with-the-hm3301/

