<!--- master only -->
> ![warning](../images/warning.png) This document applies to the HEAD of the calico-containers source tree.
>
> View the calico-containers documentation for the latest release [here](https://github.com/projectcalico/calico-containers/blob/v0.17.0/README.md).
<!--- else
> You are viewing the calico-containers documentation for release **release**.
<!--- end of master only -->

# Mesos with Calico networking
Calico can be used as a network plugin for Mesos both for the Docker
Containerizer and the Unified Containerizer.

Calico with the Docker Containerizer uses a Calico network and IPAM 
driver that hooks directly into the Docker networking infrastructure.
Docker networks using the Calico plugin are created up-front, and Mesos 
can then be used to launch Docker containers using these networks.  Each
network is associated with a single Calico profile.  Fine grained policy
can be modified using the `calicoctl profile` commands.

Calico with the Unified Containerizer utilizes [net-modules](https://github.com/mesosphere/net-modules)
along with a [Calico-Mesos netmodules plugin](https://github.com/projectcalico/calico-mesos)
to provide Calico networking.  Networks are specified as net-groups when
launching a Mesos task.  A Calico profile is automatically created for 
each net-group (if it doesn't already exist), defaulting to allow 
communication between containers using the same net-group.  Fine grained
policy can be modified using the `calicoctl profile` commands.

The installation requirements to use Calico networking are different
depending on whether you are using the Docker Containerizer or the 
Unified Containerizer.  When setting up your cluster, follow the
appropriate guide based on your requirements.  Note that your Mesos
cluster may be configured to use both the Docker Containerizer and the
Unified Containerizer - in which case follow both sets of installation
instructions.

Calico is particularly suitable for large Mesos deployments on bare 
metal or private clouds, where the performance and complexity costs of 
overlay networks can become significant. It can also be used in public 
clouds.

To build a new Mesos cluster with Calico networking, try one of the
following guides:

Quick-start guides:
- [CentOS Vagrant](VagrantCentOS.md)
- [CoreOS on GCE](GCE.md)
- [CoreOS on AWS](AWS.md)

Installation guides:
- [CentOS RPM installation - Docker Containerizer](RPMInstallDocker.md)
- [CentOS RPM installation - Unified Containerizer](RPMInstallUnified.md)

If you have an existing Mesos cluster, follow the appropriate
installation guide omitting any steps installing existing software.
However, please ensure Mesos (and Marathon if you are using) are
installed at the appropriate minimum version, upgrading if necessary,

# Mesos with Calico policy
Calico can provide network policy for Mesos tasks for both Docker
Containerizer and Unified Containerizer.  Follow

This feature is currently in alpha and disabled by default.  The following guide explains how to enable and use Calico policy on Kubernetes. 
- [Kubernetes v1alpha1 Network Policy](NetworkPolicy.md)

Calico also supports network policy using annotaions.  This method is deprecated, and as such is not recommended.
- [Calico policy using Annotations](AnnotationPolicy.md) [Deprecated]

# Requirements
- The kube-proxy must be started in `iptables` proxy mode.

# Troubleshooting 
- [Troubleshooting](Troubleshooting.md)

[![Analytics](https://calico-ga-beacon.appspot.com/UA-52125893-3/calico-containers/docs/cni/kubernetes/README.md?pixel)](https://github.com/igrigorik/ga-beacon)
