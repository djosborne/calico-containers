<!--- master only -->
> ![warning](images/warning.png) This document applies to the HEAD of the calico-mesos-deployments source tree.
>
> View the calico-mesos-deployments documentation for the latest release [here](https://github.com/projectcalico/calico-mesos-deployments/blob/0.27.0%2B2/README.md).
<!--- else
> You are viewing the calico-mesos-deployments documentation for release **release**.
<!--- end of master only -->

# Manually Install Calico and Mesos on Agent
This guide explains how to add calico networking to a Mesos slave. Specifically, we will add the calico plugin to perform networking for the unified containerizer.
- For information on the Docker Containerizer, see [Docker Containerizer Guide](#)


## Prerequisites
### Mesos-Slave with Mesos and Netmodules installed
- This guide will focus on only the calico components of a calico-mesos-slave. You must have a slave with net-modules activated. See the [Add Netmodules to Mesos Guide](#)

### Docker
Calico's core services are run in a docker container, so we'll need Docker installed on every Agent in the cluster.
[Follow Docker's Centos installation guide](https://docs.docker.com/engine/installation/centos/) for information on how to get Docker installed.

### Running etcd instance
[prerequisites guide](prerequisites)

## 1. Install Calico-Mesos Components
The following scripts will add the necessary calico components. 
```
mkdir /calico

# the calico_mesos plugin binary
curl -O /calico/calico_mesos https://github.com/projectcalico/calico-mesos/releases/download/v0.1.5/calico_mesos
chmod +x /calico/calico_mesos

# modules.json
curl -O /calico/modules.json https://raw.githubusercontent.com/projectcalico/calico-mesos-deployments/master/packages/sources/modules.json 

# activate modules in mesos-slave
echo file:///calico/modules.json > /etc/mesos/mesos-slave/modules

# set ETCD_AUTHORITY for the mesos slave process, by replacing 
# [etcd-ip:port] with the location of your etcd server
echo ETCD_AUTHORITY=[etcd-ip:port] >> /etc/mesos-slave/environment
```

# 2. Run Calico Node
The last Calico component required for Calico networking in Mesos is `calico-node`, a Docker image containing Calico's core routing processes.
 
`calico-node` can easily be launched via `calicoctl`, Calico's command line tool. When doing so, we must point `calicoctl` to our running instance of etcd, by setting the `ECTD_AUTHORITY` environment variable.

> Follow our [Mesos Cluster Preparation guide](MesosClusterPreparation.md#Install) if you do not already have an instance of etcd running to walk through installing etcd with Docker.

```
curl -O https://github.com/projectcalico/calico-containers/releases/download/v0.9.0/calicoctl
chmod +x calicoctl
sudo ETCD_AUTHORITY=<IP of host with etcd>:4001 ./calicoctl node
```

## Next steps
See [Our Guide on Using Calico-Mesos](UsingCalicoMesos.md) for info on how to test your cluster and start launching tasks networked with Calico.

[![Analytics](https://calico-ga-beacon.appspot.com/UA-52125893-3/calico-containers/docs/mesos/ManualInstallCalicoMesos.md?pixel)](https://github.com/igrigorik/ga-beacon)
