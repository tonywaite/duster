
class Config(object):
    # General Flask
    DEBUG = False
    TESTING = False
    PORT = 8080

    # Database
    DATABASE = 'sqlite:///concentration.sqlite'  # Database engine and name

    # Data sampling
    SAMPLING_STANDALONE = True      # If true, standalone sampler needs to be launched
    SAMPLING_TIME = 120             # In seconds
    SAMPLING_DUMMY = False          # True to turn on randomly generated samples (testing purposes)

    # PI setup
    PI_SDA = 2                  # Sda id
    PI_SCL = 3                  # Scl id
    PI_I2C_ADDRESS = 0x40       # I2c address
