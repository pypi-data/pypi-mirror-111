import requests
import yaml
from termcolor import colored

from common_structure_microservices.exception import GenericMicroserviceError


class Profiles:
    file_config = yaml.load(open('profile.yaml'), Loader=yaml.FullLoader)['django']
    APP_NAME = file_config['application']['name']
    PROFILE = file_config['profiles']['active']
    ENVIRONMENTS = f'{APP_NAME}-{PROFILE}.yml'
    URI = file_config['cloud']['config']['uri'] + ENVIRONMENTS
    APPLICATION = file_config['application']
    CONFIG = {}
    env = {}

    def get_env(self):
        try:
            r = requests.get(self.URI, allow_redirects=True)
            open(self.ENVIRONMENTS, 'wb').write(r.content)
            self.env = yaml.load(open(self.ENVIRONMENTS), Loader=yaml.FullLoader)['django']
            self.CONFIG = self.env['cloud']['config']
            print(colored('ARCHIVO DE CONFIGURACIONES -> ' + self.ENVIRONMENTS, 'green'))
        except Exception as e:
            raise GenericMicroserviceError(status=500, detail=f'ERROR CONFIG ENV: {e}')

    def get_operating_system(self):
        return self.env['cloud']['config'].get('OPERATING_SYSTEM')
