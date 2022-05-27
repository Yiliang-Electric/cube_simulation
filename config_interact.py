import configparser
import cv2


def get_config_data(config_path):
    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8")
    # config = config[section]
    return config

def write_config_data(config, config_path):
    with open(config_path, 'w') as configfile:    # save
        config.write(configfile)

config_path = "config.cfg"
config = get_config_data(config_path)
config["program"]['bag_material'] = 'bag_material'
write_config_data(config, config_path)