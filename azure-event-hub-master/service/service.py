import json
from flask import Flask, request, Response
from azure.eventhub import EventHubClient, Offset
from ast import literal_eval
import logging
import cherrypy
import os
from uamqp import types, errors


app = Flask(__name__)
logger = logging.getLogger('service')
logging.basicConfig(level=logging.ERROR)

# Access tokens for event hub namespace, from Azure portal for namespace
address = os.environ.get('address')
user = os.environ.get('user')
key = os.environ.get('key')
consumergroup = os.environ.get('consumergroup')
partition = os.environ.get('partition')

if not address:
    logger.error("No event hub address supplied")


@app.route('/', methods=['GET'])
def get():
    logger.info("start of the function get()")
    if request.args.get('since') is None:
        sequenceid = "-1"
    else:
        sequenceid = int(request.args.get('since'))

    client = EventHubClient(address, debug=False, username=user, password=key)
    client.clients.clear()
    receiver = client.add_receiver(consumergroup, partition, prefetch=5000, offset=Offset(sequenceid), keep_alive=72000)
    client.run()

    def generate():
        try:
            batched_events = receiver.receive(max_batch_size=100,timeout=3000)
            index = 0
            yield '['
            while batched_events:
                for event_data in batched_events:
                    if index > 0:
                        yield ','
                    last_sn = event_data.sequence_number
                    data = str(event_data.message)
                    output_entity = literal_eval(data)
                    output_entity.update({"_updated": last_sn})
                    yield json.dumps(output_entity)
                    index = index + 1
                batched_events = receiver.receive(max_batch_size=100,timeout=3000)
            yield ']'
        except (errors.TokenExpired, errors.AuthenticationException):
            logger.error("Receiver disconnected due to token error.")
            receiver.close(exception=None)
        except (errors.LinkDetach, errors.ConnectionClose):
            logger.error("Receiver detached.")
            receiver.close(exception=None)
        except Exception as e:
            logger.error("Unexpected error occurred (%r). Shutting down.", e)
            receiver.close(exception=None)

    return Response(generate(), mimetype='application/json')


if __name__ == '__main__':
    cherrypy.tree.graft(app, '/')

    # Set the configuration of the web server to production mode
    cherrypy.config.update({
        'environment': 'production',
        'engine.autoreload_on': False,
        'log.screen': True,
        'server.socket_port': 5000,
        'server.socket_host': '0.0.0.0'
    })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()
