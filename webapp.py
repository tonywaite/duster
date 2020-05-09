import datetime
from flask import Flask, render_template
import threading
import sqlalchemy as db
from hm3301 import Hm3301
from sampler import Sampler
from hm3301dummy import Hm3301Dummy
from config import Config

app = Flask(__name__)
app.config.from_object("config.Config")
engine = db.create_engine(Config.DATABASE)


def parse_data(dataset):
    labels = [str(element['date']).split('.')[0] for element in dataset]
    data = {'pm1 factory': [element['pm1 factory'] for element in dataset],
            'pm2.5 factory': [element['pm2.5 factory'] for element in dataset],
            'pm10 factory': [element['pm10 factory'] for element in dataset],
            'pm1 atmospheric': [element['pm1 atmospheric'] for element in dataset],
            'pm2.5 atmospheric': [element['pm2.5 atmospheric'] for element in dataset],
            'pm10 atmospheric': [element['pm10 atmospheric'] for element in dataset]
            }
    return labels, data


def query_data(hours=0, minutes=0):
    connection = engine.connect()
    metadata = db.MetaData()
    concentration = db.Table('concentration', metadata, autoload=True, autoload_with=engine)
    query = db.select([concentration])
    query = query.where(concentration.c.date > datetime.datetime.now() - datetime.timedelta(hours=hours, minutes=minutes))
    result_proxy = connection.execute(query)
    dataset = result_proxy.fetchall()
    return parse_data(dataset)


@app.route('/')
def main():
    labels, data = query_data(hours=24)
    return render_template('summary.html', timerange="24 hours", data=data, labels=labels)


@app.route('/hours=<int:hours>')
def last_hours(hours):
    labels, data = query_data(hours=hours)
    return render_template('summary.html', timerange="%s hours" % hours, data=data, labels=labels)


@app.route('/minutes=<int:minutes>')
def last_minutes(minutes):
    labels, data = query_data(minutes=minutes)
    return render_template('summary.html', timerange="%s minutes" % minutes, data=data, labels=labels)


if __name__ == '__main__':

    if not Config.SAMPLING_DUMMY:
        import pigpio
        hm3301 = Hm3301(pigpio.pi(), sda=Config.PI_SDA, scl=Config.PI_SCL, i2c_address=Config.PI_I2C_ADDRESS)
    else:
        hm3301 = Hm3301Dummy(None)

    if not Config.SAMPLING_STANDALONE:
        thread = threading.Thread(target=Sampler(hm3301).collect, args=(), daemon=True)
        thread.start()

    app.run(debug=Config.DEBUG, port=Config.PORT)
