<!--- master only -->
> ![warning](images/warning.png) This document applies to the HEAD of the calico-mesos-deployments source tree.
>
> View the calico-mesos-deployments documentation for the latest release [here](https://github.com/projectcalico/calico-mesos-deployments/blob/0.26.0%2B1/README.md).
<!--- else
> You are viewing the calico-mesos-deployments documentation for release **release**.
<!--- end of master only -->

# Mesos Cluster Preparation: etcd & zookeeper
This guide will launch etcd and zookeeper as docker containers bound to their host's networking namespace. While most Mesos deployments will run these services on specific, dedicated machines chosen to maximize availability, we suggest following this guide on whichever machine is running your Mesos Master process, for simplicity.

## Prerequisites: Docker
Docker must be installed on this hostyou will need Docker installed on every Master and Agent in your cluster.
[Follow Docker's Centos installation guide](https://docs.docker.com/engine/installation/centos/) for information on how to get Docker installed.

## 1. Launch ZooKeeper
Mesos uses ZooKeeper to elect and keep track of the leading master in the cluster.

```
sudo docker pull jplock/zookeeper:3.4.5
sudo docker run --detach --name zookeeper -p 2181:2181 jplock/zookeeper:3.4.5
```

#### Configure Firewall for ZooKeeper
ZooKeeper uses tcp over port 2181, so you'll need to open this port on your firewall.

| Service Name | Port/protocol     |
|--------------|-------------------|
| ZooKeeper    | 2181/tcp          |

Example `firewalld` config

```
sudo firewall-cmd --zone=public --add-port=2181/tcp --permanent
sudo systemctl restart firewalld
```
## 2. Launch etcd
Calico uses etcd as its data store and communication mechanism among Calico components.

etcd needs your fully qualified domain name to start correctly.

```
sudo docker pull quay.io/coreos/etcd:v2.2.0
export FQDN=`hostname -f`
sudo mkdir -p /var/etcd
sudo FQDN=`hostname -f` docker run --detach --name etcd --net host -v /var/etcd:/data quay.io/coreos/etcd:v2.2.0 \
     --advertise-client-urls "http://${FQDN}:2379,http://${FQDN}:4001" \
     --listen-client-urls "http://0.0.0.0:2379,http://0.0.0.0:4001" \
     --data-dir /data
```
If you have SELinux policy enforced, you must perform the following step:

```
sudo chcon -Rt svirt_sandbox_file_t /var/etcd
```

#### Configure Firewall for etcd
Etcd uses tcp over ports 2379 and 4001. You'll need to open the relevent ports on your firewall:

| Service Name | Port/protocol     |
|--------------|-------------------|
| etcd         | 4001/tcp          |

Example `firewalld` config

```
sudo firewall-cmd --zone=public --add-port=4001/tcp --permanent
sudo systemctl restart firewalld
```

## Next steps
See [Our Guide on Using Calico-Mesos](UsingCalicoMesos.md) for info on how to test your cluster and start launching tasks networked with Calico.

[![Analytics](https://calico-ga-beacon.appspot.com/UA-52125893-3/calico-containers/docs/mesos/MesosClusterPreparation.md?pixel)](https://github.com/igrigorik/ga-beacon)
