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

import pika
import time

class Connection(object):
    def __init__(self, config):
        self.config = config

        params = pika.URLParameters(self.config.amqp_url)
        self.conn = pika.BlockingConnection(params)
        self.chan = self.conn.channel()

    def stop(self):
        self.chan.stop_consuming()
        self.conn.close()

    def listen(self, callback):
        self.chan.queue_declare(queue=self.config.amqp_queue)
        self.chan.basic_consume(self.config.amqp_queue, callback, auto_ack=True)
        self.chan.start_consuming()

    def send(self, body):
        self.chan.basic_publish(exchange='', routing_key=self.config.amqp_queue, body=body)

class Sender(object):
    def __init__(self, config):
        """Construct a new AMQP message sender using the given configuration dict to specify a URL and queue.
        """
        self.config = config
        self.amqp = Connection(config)

    def send_metrics(self, metrics):
        """Serialize the given metrics dict (assumed to be key:value pairs without timestamps) to triplets in a 
        multi-line message, using a timestamp generated in this method. Once the message is formatted, send it to 
        the configured Slack channel.
        """
        now = int(time.time())

        lines = []
        for k in metrics.keys():
            v = metrics[k]
            lines.append(f"{k} {v} {now}")

        self.send("\n".join(lines))

    def send(self, message):
        """Send a simple string message to the configured AMQP queue."""
        return self.amqp.send(message)
