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

import time
import socket
import pika
from carbon_amqp.amqp import Connection
from carbon_slack.carbon import PlaintextSender

class Relay(object):
    def __init__(self, config):
        """Initialize the Relay using a config dict.
        """
        self.amqp = Connection(config)
        self.sender = PlaintextSender(config)
        self.config = config

    def stop(self):
        """If a socket is open in the sender at the time when the user kills this script, try to close it 
        gracefully.
        """
        self.sender.close()
        self.amqp.close()

    def start(self):
        self.amqp.listen(relay)

    def relay(chan, method, properties, body):
        """Receive a messages from the AMQP channel and assume they are metrics triplets (key, value, tstamp).

        For each triplet we can parse, send a new metric data point over a socket that we open to the Carbon
        daemon for this purpose, using newline-delimited plaintext.
        """
        print("Sending stats...")
        metrics = []
        lines = [l.rstrip() for l in body.splitlines()]
        for line in lines:
            parts = line.split(' ')
            if len(parts) < 3:
                continue

            metrics.append("%s %s %s\n" % (parts[0], parts[1], parts[2]))

        if len(metrics) > 0:
            self.sender.send_metrics(metrics)

