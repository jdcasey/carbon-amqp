# This file is part of Carbon-AMQP.
#
# Carbon-AMQP is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Carbon-AMQP is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Carbon-AMQP.  If not, see <https://www.gnu.org/licenses/>.

from ruamel.yaml import YAML
import getpass
import subprocess
import os
import sys

CONFIG_PATH = '/etc/carbon-amqp.yml'

AMQP_URL = 'amqp-url'
AMQP_QUEUE = 'amqp-queue'
CARBON_SERVER='carbon-server'
CARBON_PORT='carbon-port'

DEFAULT_AMQP_QUEUE = 'carbon'

class Config(object):
    def __init__(self, data):
        """Create a configuration instance suitable for use with the Carbon-AMQP relay (and associated commands).

        NOTE: This could be created from an external YAML (or dict) source, and doesn't have to be read from the 
        CONFIG_PATH (/etc/carbon-amqp.yml by default).
        """
        self.amqp_url = data.get(AMQP_URL)
        self.amqp_queue = data.get(AMQP_QUEUE) or DEFAULT_AMQP_QUEUE
        self.carbon_server = data.get(CARBON_SERVER)
        self.carbon_port = data.get(CARBON_PORT)

def serialized_sample():
    """Serialize a sample configuration to STDOUT"""
    return YAML().dump({
        AMQP_URL: 'amqp://<someuser>:<somepass>@wombat.rmq.cloudamqp.com/<instance-token>'
        CARBON_SERVER: '127.0.0.1',
        CARBON_PORT: 2023
    }, sys.stdout)

def load(config_file=None):
    """Load a Carbon-AMQP relay configuration from a YAML file (by default, use /etc/carbon-amqp.yml)"""
    config_path = config_file or CONFIG_PATH
    data = {}

    with open(config_path) as f:
        data = YAML().load(f)

    return Config(data)


