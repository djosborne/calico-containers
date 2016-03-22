<!--- master only -->
> ![warning](images/warning.png) This document applies to the HEAD of the calico-mesos-deployments source tree.
>
> View the calico-mesos-deployments documentation for the latest release [here](https://github.com/projectcalico/calico-mesos-deployments/blob/0.26.0%2B1/README.md).
<!--- else
> You are viewing the calico-mesos-deployments documentation for release **release**.
<!--- end of master only -->

# RPM Install Calico-Mesos
This tutorial will walk through installing prebuilt RPMs containg Mesos, Netmodules, and Calico. At the completion of this guide, you will have a Mesos Slave ready to launch tasks with Calico networking.

>Note: These RPMs do not serve as an official calico or mesos installation option, and will not receive a supported upgrade story for the future. They merely serve as a more automatic alternative to performing the steps in the [Manually Installing Calico + Mesos + Netmodules](ManualInstallCalicoMesos.md) guide. 

This RPM installation includes and installs:
- mesos
- net-modules
- `calico_mesos` plugin binary
- `modules.json`, JSON file which points mesos to the location of `net-modules` and points `net-modules` to the `calico-mesos` plugin
- `calicoctl`, a command line tool for easily launching the calico-node service
- `calico.service`, a systemd service to ensure calico is always running

## Prerequisites
### Zookeeper, etcd, and Marathon
Follow the [Mesos Master and Cluster Preparation Guide](MesosClusterPreparation.md) for information on configuring these services.

### Mesos-Master
Calico to your Mesos Cluster doesn't require any modifications to the Mesos Master. Therefore you can follow Mesosphere's  [Mesos Install Guide](https://mesosphere.com/downloads/) using their official RPM to set up your Master.


## Getting Started
We will now install Mesos, Netmodules, and Calico on an Agent.

## 1. Download and Install the RPMs
Extra Packages for Enterprise Linux (EPEL) must be installed before installing Mesos + Net-Modules. You can download this package by calling:

```
sudo yum install -y epel-release
sudo yum update
```

Now, download and install the RPMs:
```
curl -O https://github.com/projectcalico/calico-mesos-deployments/releases/download/0.27.0%2B1/calico-mesos-rpms.tar
tar -xvf calico-mesos-rpms.tgz
sudo yum install -y calico-mesos-rpms/*.rpm
```

## 2. Start Calico
A systemd unit file has been provided to start the Calico processes needed by the calico_mesos plugin binary. When starting the calico-mesos service, the environment variable `ETCD_AUTHORITY` is used to point Calico to a running instance of etcd. This variable must be set in `/etc/default/mesos-slave`.  Similarly, the `MASTER` variable should point at your ZooKeeper's IP address and port. 

> If you do not have zookeeper and etcd running, follow the [Mesos Cluster Preparation guide](MesosClusterPreparation.md#install-zookeeper-and-etcd).

Open `/etc/default/mesos-slave` set the `ETCD_AUTHORITY` and `MASTER` 
variables to the correct values.  Your file should now look like this:
```
MASTER=zk://<ZOOKEEPER_IP>:2181/mesos
ETCD_AUTHORITY=<ETCD_IP>:4001
```

Now start the services:

```
sudo systemctl start calico-mesos.service
sudo systemctl start mesos-slave.service
```

Check that Calico and Mesos are both running:

```
sudo systemctl status calico-mesos.service
sudo systemctl status mesos-slave.service
```

## Next steps
See [Our Guide on Using Calico-Mesos](UsingCalicoMesos.md) for info on how to test your cluster and start launching tasks networked with Calico.


[calico-mesos]: https://github.com/projectcalico/calico-mesos/releases/latest

[![Analytics](https://calico-ga-beacon.appspot.com/UA-52125893-3/calico-containers/docs/mesos/RpmInstallCalicoMesos.md?pixel)](https://github.com/igrigorik/ga-beacon)
