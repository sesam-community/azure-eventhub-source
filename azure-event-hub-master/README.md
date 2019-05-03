Receive messages from Azure Event Hub.

Clone or download this repositiory. Bulid and push your docker image and fill in cedentials from your Azure Event Hub. 
To read more about how this work see our [**Getting Started with Sesam**](https://github.com/sesam-community/wiki/wiki/Getting-started) page.

Sample system in Sesam Portal:
```json
{
  "_id": "<system- name>",
  "type": "system:microservice",
  "connect_timeout": 600,
  "docker": {
     "cpu_quota": 100,
    "environment": {
    ###FILL INN YOUR EVENT HUB CREDENTIALS###
      "ADDRESS": "$ENV(eventhub-address)",
      "CONSUMER_GROUP": "$ENV(eventhub-consumer-group)",
      "KEY": "$SECRET(apikey)",
      "USER": "$ENV(eventhub-usr)"
    },
    "image": "<dockerhub_username>/<repoistory>:<tag>",
     "memory": 512,
    "port": 5000
  },
  "verify_ssl": true
}
```
The secrets and environment variables are stored in **Datahub** --> **Variables**-- in Sesam Node. 

Sample input pipe:
```json
{
  "_id": "<pipe-name>",
  "type": "pipe",
  "source": {
    "type": "json",
    "system": "<source system name>",
    "is_chronological": true,
    "is_since_comparable": true,
    "supports_since": true,
    "url": "/"
  },
  "transform": {
    "type": "dtl",
    "rules": {
      "default": [
        ["copy", "*"],
        ["add", "_id",
          ["string", "_S._updated"]
        ]
      ]
    }
  },
  "pump": {
    "cron_expression": "0 * * * ?"
  },
  "compaction": {
    "sink": true,
    "keep_versions": 0,
    "time_threshold_hours": 24,
    "time_threshold_hours_pump": 720
  }
}
```


