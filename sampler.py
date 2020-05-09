import time
import sqlalchemy as db
from hm3301 import Hm3301WrongResponseException, Hm3301
from config import Config
from hm3301dummy import Hm3301Dummy
import pigpio


class Sampler(object):

    def __init__(self, sensor):
        self.sensor = sensor

    def collect(self):
        engine = db.create_engine(Config.DATABASE)
        connection = engine.connect()
        metadata = db.MetaData()

        table = db.Table('concentration', metadata,
                         db.Column('date', db.DateTime()),
                         db.Column('pm1 factory', db.Integer()),
                         db.Column('pm2.5 factory', db.Integer()),
                         db.Column('pm10 factory', db.Integer()),
                         db.Column('pm1 atmospheric', db.Integer()),
                         db.Column('pm2.5 atmospheric', db.Integer()),
                         db.Column('pm10 atmospheric', db.Integer()))

        metadata.create_all(engine)

        while True:
            try:
                data = self.sensor.get_data()
                print(data)

                query = db.insert(table).values(data)
                result = connection.execute(query)
                time.sleep(Config.SAMPLING_TIME)
            except Hm3301WrongResponseException as ex:
                print(ex.message)
            #finally:
            #    self.sensor.close()


if __name__ == '__main__':

    if not Config.SAMPLING_DUMMY:
        pi = pigpio.pi()
        hm3301 = Hm3301(pi, sda=Config.PI_SDA, scl=Config.PI_SCL, i2c_address=Config.PI_I2C_ADDRESS)
    else:
        hm3301 = Hm3301Dummy(None)

    sampler = Sampler(hm3301)
    sampler.collect()
