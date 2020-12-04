""" Provides helper functions. """
import configparser
import os
import logging


def configure_logging():
    FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('pycaptive')
    logger.setLevel(logging.INFO)
    return logger


def search_and_load_ini():
    """
    Searches for pycaptive.ini and loads its content into a dictionary, with a
    more clean structure.

    Returns:
        bool (False): no file from paths tuple was detected
        dict : all pycaptive.ini configuration
    """
    config = configparser.ConfigParser()
    config.optionxform = str # Preserves case of .ini file
    paths = ('/etc/pycaptive/pycaptive.ini', 'app/pycaptive.ini', 'pycaptive.ini')
    for ini in paths:
        if os.path.isfile(ini):
            config.read(ini)
            break

    # Generating dict based on pycaptive.ini for loading into Flask app.config
    if config.sections():
        # Flatening dictionary for better .ini readability purposes
        config_flat = {k: v for dv in config.values() for k, v in dv.items()}
    else:
        return False

    return config_flat
