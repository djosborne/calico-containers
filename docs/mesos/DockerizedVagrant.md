<!--- master only -->
> ![warning](../images/warning.png) This document applies to the HEAD of the calico-containers source tree.
>
> View the calico-containers documentation for the latest release [here](https://github.com/projectcalico/calico-containers/blob/v0.14.0/README.md).
<!--- else
> You are viewing the calico-containers documentation for release **release**.
<!--- end of master only -->

# Deploying a Vagrant Dockerized Mesos Cluster with Calico

In these instructions, we will create two Centos virtual machines (a master and an agent) that run all cluster services as [Docker][docker] containers.  This speeds deployment and will prevent pesky issues like incompatible dependencies.

If you would prefer to run the commands manually to better understand what is being run in the script,
check out the [Manual Dockerized Deployment guide](DockerizedDeployment.md).

On the Master machine, the script installs containers for:

 * Zookeeper
 * etcd
 * Mesos Master
 * Marathon (Mesos framework)

On the Agent machine, we will install containers for:

 * Mesos Agent
 * Calico

## Preparing Host Machine

To run these instructions, you will need a host machine with:

 * [VirtualBox][virtualbox] to host the Mesos master and slave virtual machines
 * [Vagrant][vagrant] to run the script that provisions the Virtual Machines
 * 4+ GB memory
 * 2+ CPU
 * 80 GB available storage space (40 GB per machine)


## Deploy Mesos Cluster with Vagrant

The vagrant script will create the two Centos virtual machines, install docker and calico on the machines, pull the required docker images from DockerHub, and start the images.

To get the vagrant script, you must clone the [`calico-mesos repository`][calico-mesos] onto your host.

```
# HTTPS
git clone https://github.com/projectcalico/calico-mesos.git

# SSH
git clone git@github.com:projectcalico/calico-mesos.git 
```

Change directories into the `calico-mesos` repository on your machine, then run `vagrant up` to execute the `Vagrantfile` in this directory:

```
cd calico-mesos
vagrant up
```

That's it!  Note that the script may take up to 30 minutes to complete, so don't be alarmed if it 
seems to be taking its time.

## Vagrant Install Results

Once the vagrant install is finished, you will have two machines running Docker with the following setup:

### Master

 * **OS**: `Centos`
 * **Hostname**: `calico-01`
 * **IP**: `172.18.8.101`
 * **Docker Containers**:
	 * `mesos-master` - `calico/mesos-calico` 
	 * `etcd` - `quay.io/coreos/etcd`
	 * `zookeeper` - `jplock/zookeeper`
	 * `marathon` - `mesosphere/marathon`

### Agent

 * **OS**: `Centos`
 * **Hostname**: `calico-02`
 * **IP**: `172.18.8.102`
 * **Docker Containers**:
	 * `mesos-agent` - `calico/mesos-calico`
	 * `calico-node` - `calico/node`

You can log into each machine by running:
```
vagrant ssh <HOSTNAME>
```

## Next steps

### Use Frameworks 

At this point, you're Mesos Cluster is configured and you can start using frameworks.

You can run the following command on either instance to use a Calico framework that runs tests on the cluster:
```
docker run calico/calico-mesos-framework 172.18.8.101:5050
```

### More Agents

You can modify the script to use multiple agents. To do this, modify the `num_instances` variable
in the `Vagrantfile` to be greater than `2`.  The first instance created is the master instance, every 
additional instance will be an agent instance.

Every agent instance will take similar form to the agent instance above:

 * **OS**: `Centos`
 * **Hostname**: `calico-0X`
 * **IP**: `172.18.8.10X`
 * **Docker Containers**:
	 * `mesos-agent` - `calico/mesos-calico`
	 * `calico-node` - `calico/node`

where `X` is the instance number.
 
Each agent instance will require additional storage and memory resources.


[calico]: http://projectcalico.org
[mesos]: https://mesos.apache.org/
[calico-mesos]: https://github.com/projectcalico/calico-mesos
[net-modules]: https://github.com/mesosphere/net-modules
[docker]: https://www.docker.com/
[virtualbox]: https://www.virtualbox.org/
[vagrant]: https://www.vagrantup.com/
[![Analytics](https://ga-beacon.appspot.com/UA-52125893-3/calico-containers/docs/mesos/DockerizedDeployment.md?pixel)](https://github.com/igrigorik/ga-beacon)
