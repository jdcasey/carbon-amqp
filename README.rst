AMQP-to-Carbon Relay Library for Python
========================================

This library's main purpose is to relay metrics from a AMQP queue to a Carbon daemon, for inclusion in a Graphite database. It also contains commands (and classes) used to send and receive metric messages to Carbon.

Configuration
-------------

You can configure this library in two ways:

`/etc/carbon-amqp.yml` Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is what the "native" YAML configuration file looks like::

	amqp-url: "amqp://<someuser>:<somepass>@wombat.rmq.cloudamqp.com/<instance-token>" # URL from AMQP server
	amqp-queue: carbon
	carbon-server: 127.0.0.1
	carbon-port: 2023

Any command provided in this library will expect to load the above configuration, by default using the ``/etc/carbon-amqp.yml`` file (but you can also provide the configuration path using the ``--config | -c`` option).

Embedded in Your Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're using Carbon-AMQP as a library, you can also load the necessary configuration elements from any ``dict`` using::

	import carbon_amqp.config as conf
	config = conf.Config({
		conf.AMQP_URL: 'amqp://user:pass@server/instance-token',
		conf.AMQP_QUEUE: 'carbon',
		conf.CARBON_SERVER: '127.0.0.1',
		conf.CARBON_PORT: 2023
	})

This is the same as::

	import carbon_amqp.config as conf
	config = conf.Config({
		'amqp-url': 'amqp://user:pass@server/instance-token',
		'amqp-queue': 'carbon',
		'carbon-server': '127.0.0.1',
		'carbon-port': 2023
	})

As you can see, you could initialize this directly from strings in a script, or by reading command line arguments, or from almost anywhere. You could even read in another YAML file that looked something like this::

	my-app-id: 10
	my-username: buildchimp
	relay:
		amqp-url: "amqp://user:pass@server/instance-token"
		amqp-queue: carbon
		carbon-server: 127.0.0.1
		carbon-port: 2023

Then, use something like the following to initialize your relay::

	import carbon_slack.config as conf
	from carbon_slack.relay import Relay
	import yaml

	with open('/path/to/app.yml') as f:
		data = yaml.safe_load(f)

	relay = Relay(conf.Config(data['relay']))

Sending Manually
----------------

Carbon-AMQP also provides a library-based approach, for sending metrics programmatically::

	from carbon_amqp.amqp import Sender

	sender = Sender(config)
	sender.send_metrics({'test.metric', 1234})

Relaying to Carbon
------------------

Relaying is what Carbon-AMQP is designed to do. It uses AMQP as a message bus for sending metrics, which means neither the Graphite DB server nor any of the clients need to be exposed to the internet directly by opening holes in your firewalls. Both the client and the relay initiate connections to AMQP and interact on a channel using plaintext.

Metric messages in a AMQP channel each contain one or more lines of the format::

	metric.name value timestamp-in-seconds

This means you can send a group of metrics in a single message to save on protocol overhead. When the Relay client sees messages in this format, it parses them and sends them on to the Carbon daemon associated with your Graphite DB instance. Messages on the queue are auto-acknowledged.

Here's an example of the Relay in action::

	from carbon_amqp.relay import Relay

	relay = Relay(config)

	try:
	    relay.start()
	except KeyboardInterrupt:
		relay.stop()
