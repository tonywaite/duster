import time
import datetime
import pigpio


class Hm3301WrongResponseException(Exception):

    def __init__(self, message="Hm3301 wrong response."):
        self.message = message


class Hm3301(object):

    def __init__(self, pi, sda=2, scl=3, i2c_address=0x40):
        self.pi = pi
        self.sda = sda
        self.scl = scl
        self.i2c_address = i2c_address

        self.pi.set_pull_up_down(self.sda, pigpio.PUD_UP)
        self.pi.set_pull_up_down(self.scl, pigpio.PUD_UP)
        self.pi.bb_i2c_open(self.sda, self.scl, 20000)

        self.pi.bb_i2c_zip(self.sda, [4, self.i2c_address, 2, 7, 1, 0x80, 2, 7, 1, 0x88, 3, 0])
        time.sleep(1)

    def close(self):
        self.pi.bb_i2c_close(self.sda)
        self.pi.stop()

    @staticmethod
    def checksum(data):
        chksum = 0
        for i in range(28):
            chksum += data[i]
        chksum = chksum & 0xff
        return chksum == data[28]
   
    def get_data(self):
        (count, data) = self.pi.bb_i2c_zip(self.sda, [4, self.i2c_address, 2, 7, 1, 0x81, 3, 2, 6, 29, 3, 0])
        data = list(data)

        if self.checksum(data):
            concentration = {
                'date': datetime.datetime.now(),
                'pm1 factory': data[4] << 8 | data[5],
                'pm2.5 factory': data[6] << 8 | data[7],
                'pm10 factory': data[8] << 8 | data[9],
                'pm1 atmospheric': data[10] << 8 | data[11],
                'pm2.5 atmospheric': data[12] << 8 | data[13],
                'pm10 atmospheric': data[14] << 8 | data[15]
            }
            return concentration
        else:
            raise Hm3301WrongResponseException


if __name__ == '__main__':

    import pigpio
    hm3301 = Hm3301(pigpio.pi())

    try:
        while True:
            data = hm3301.get_data()
            print(data)

            time.sleep(5)
    except Hm3301WrongResponseException as ex:
        print(ex.message)
    finally:
        hm3301.close()
