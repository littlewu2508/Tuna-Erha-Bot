import configparser

config_file = 'config.ini'
# config_file = 'config-dev.ini'

config = configparser.RawConfigParser()
config.read(config_file)


def update_config():
    with open(config_file, 'w') as configFile:
        config.write(configFile)
