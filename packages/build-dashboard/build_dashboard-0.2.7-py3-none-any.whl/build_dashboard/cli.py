from os import environ, path
from argparse import ArgumentParser
from getpass import getpass
import asyncio
import logging
import toml
from build_dashboard.model import BuildbotModel, BuildbotClient
from build_dashboard.screen import draw_screen
from build_dashboard import logger


def main():
    parser = ArgumentParser(prog='build_dashboard', description='A buildbot client')
    parser.add_argument('--unix', help='Unix domain socket to connect through', type=str)
    parser.add_argument('--username', help='Username for basic auth', type=str)
    parser.add_argument('--config', help='Config file to use', type=str)
    parser.add_argument('--protocol', help='Connection protocol (Default: http)', type=str)
    parser.add_argument('--host', help='Buildbot master hostname', type=str)
    parser.add_argument('--log', help='Writes logs to file for debugging', type=str)
    parser.add_argument('--update-interval', help='Update interval', type=str)
    args = parser.parse_args()
    
    config_file = None
    if args.config:
        config_file = args.config
    elif environ.get('HOME') != None:
        config_file = environ.get('HOME') + '/.buildbotrc'

    config = {}

    if (config_file is not None and
            path.exists(config_file)):
        with open(config_file) as f:
            config.update(toml.load(f))

    for key in vars(args):
        value = getattr(args, key)
        if value != None:
            config[key] = value
    
    if args.username is not None and 'password' not in config:
        config['password'] = getpass()
    
    if 'log' in config:
        handler = logging.FileHandler(config['log'])
        formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    else:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.ERROR)

    client = BuildbotClient(
            path=config.get('unix', None), 
            protocol=config.get('protocol', 'http'),
            host=config.get('host', 'localhost'),
            username=config.get('username', None),
            password=config.get('password', None)
    )
    
    model = BuildbotModel(client)
    
    loop = asyncio.get_event_loop()
    draw_screen(model, loop, config.get('update-interval', 5))
