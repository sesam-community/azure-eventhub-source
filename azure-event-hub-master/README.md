Receive messages from Azure Event Hub.

Clone or download this repositiory. Bulid and push your docker image and fill in cedentials from your Azure Event Hub. 
To read more about how this work see our [**Getting Started with Sesam**](https://github.com/sesam-community/wiki/wiki/Getting-started) page.

Sample system in Sesam Portal:
```json
{
  "_id": "eventhub-system",
  "type": "system:microservice",
  "docker": {
    "environment": {
    ###FILL INN YOUR EVENT HUB CREDENTIALS###
      "ADDRESS": "$ENV(eventhub-address)",
      "CONSUMER_GROUP": "$ENV(eventhub-consumer-group)",
      "KEY": "$SECRET(apikey)",
      "USER": "$ENV(eventhub-usr)"
    },
    "image": "<dockerhub_username>/<repoistory>:<tag>",
    "port": 5000
  },
  "verify_ssl": true
}
```
The secrets and evnironment variables are stored in **Datahub** in **Settings** in Sesam Node. 


Sample input pipe:
```json
{
  "_id": "input-pipe",
  "type": "pipe",
  "source": {
    "type": "json",
    "system": "eventhub-system",
    "is_chronological": true,
    "supports_since": true,
    "url": "/"
  },
  "transform": {
    "type": "dtl",
    "rules": {
      "default": [
        ["add", "_id", "_S.entityId"],
        ["copy", "*"],
        ["add", "rdf:type",
          ["ni", "input", "pipe"]
        ]
      ]
    }
  }
}
```

Sesam require that all entities has a "_id". To add this property ```["add", "_id", "_S.entityId"]```. The "_S" referes to the the source. 
