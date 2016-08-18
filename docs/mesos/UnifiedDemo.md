# Demo: Label Based Policy for Mesos

Our application uses a redis database.
Lets define a marathon application: `database.json`
```
{
  "id": "database",
  "container": {
    "type": "MESOS",
    "docker": {
      "image": "redis"
    }
  },
  "cpus": 0.2,
  "mem": 128,
  "instances": 1,
  "ipAddress": {
    "networkName": "calico-net-1",
    "labels": {
      "application": "database",
      "group": "production"
    },
    "discovery": {
      "ports": [{"number": 6379, "name": "http", "protocol": "tcp"}]
    }
  }
}
```

Lets launch it using Marathon
```
curl -X POST -H 'Content-Type: application/json' http://localhost:8080/v2/apps -d @database.json
```

Next, let's write our application: a Python flask app that uses redis as its database:
```
from flask import Flask
from redis import Redis
import os
import socket
app = Flask(__name__)
host = socket.gethostname()

@app.route('/')
def hello():
    try:
        redis = Redis(host='database.marathon.mesos', port=6379, socket_connect_timeout=1)
        redis.incr('hits')
    except:
        return "Failed to connect to redis"
    return 'Hello World! - I have been seen %s times. My Host name is %s' % (redis.get('hits') ,host)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
```

Let's wrap our app into a marathon application definition: `frontend.json`
```
{
  "id": "frontend",
  "container": {
    "type": "MESOS",
    "docker": {
      "image": "calico/hello-dcos:v0.1.0"
    }
  }
  "instances": 3,
  "cpus": 0.1,
  "mem": 128,
  "ipAddress": {
    "labels": {
      "application": "frontend",
      "group": "production"
    },
    "discovery": {
      "ports": [{"number": 80, "name": "http", "protocol": "tcp"}]
    }
  }
}
```

Then launch it using Marathon
```
curl -X POST -H 'Content-Type: application/json' http://localhost:8080/v2/apps -d @frontend.json
```

Let's check how Mesos DNS responds to queries for our frontend service
```
docker exec mesoscni_slave_1 nslookup frontend.marathon.mesos
```

...and now the backend
```
run docker exec mesoscni_slave_1 nslookup database.marathon.mesos
```


I can access the frontend:
```
docker exec mesoscni_client_1 curl  --connect-timeout 1 -s frontend.marathon.mesos
```

But I can also access redis"
```
docker exec mesoscni_client_1 docker run --rm redis:alpine redis-cli -h database.marathon.mesos -p 6379 SET hits 0
```

This is bad news, so lets add some policy

Let's define a policy that only allows redis to accept inbound connections from the frontend: `redis-policy.yaml`
```
version: v1
kind: policy
metadata:
  name: redis-policy
spec:
  order: 50
  selector: application == 'database'
  inbound_rules:
  - protocol: tcp
    src_selector: application == 'frontend'
    action: allow
  outbound_rules:
  - action: deny
```

Let's create this policy:
```
./calicoctl create --filename=./redis-policy.yaml
```

Our frontend policy will need to accept connections from anywhere, but only outbound connect to redis
```
version: v1
kind: policy
metadata:
  name: frontend-policy
spec:
  order: 50
  selector: application == 'frontend'
  inbound_rules:
  - protocol: tcp
    dst_ports: [80]
    action: allow
  outbound_rules:
  - protocol: tcp
    dst_selector: application == 'database'
    dst_ports: [6379]
    action: allow
```


```
./calicoctl create --filename=./frontend-policy.yaml
```

We can no longer access redis directly - only the frontend can
```
docker exec mesoscni_client_1 docker run --rm redis:alpine redis-cli -h database.marathon.mesos -p 6379 SET hits 0
```
