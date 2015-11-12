# Calico Without Docker
Project Calico releases are primarily distributed as docker containers for quick, easy, and consistant deployment. However, it is possible to run the core calico components on bare metal, removing the dependency on docker.

This guide will walk through running Calico Directly on a centos7 host, without Docker.

# WARNING: Dockerless Calico is Experimental!
Some `calicoctl` commands rely on a running `calico-node` container, and may not function properly when calico is run on baremetal. Please raise any encountered issues on [calico-docker](calico-docker) and message us on [calico-slack](https://calicousers-slackin.herokuapp.com/).

## Install Dependencies
1. Make changes to SELinux and QEMU config to allow VM interfaces with type='ethernet' ([this libvirt Wiki page](http://wiki.libvirt.org/page/Guest_won%27t_start_-_warning:_could_not_open_/dev/net/tun_%28%27generic_ethernet%27_interface%29) explains why these changes are required):
    ```
    setenforce permissive
    ```

2. Edit `/etc/selinux/config` and change the `SELINUX=` line to the following:
    ```
    SELINUX=permissive
    ```

## Installing Calico
Add the project-calico repository.
```
cat > /etc/yum.repos.d/calico.repo <<EOF
[calico]
name=Calico Repository
baseurl=http://binaries.projectcalico.org/rpm_stable/
enabled=1
skip_if_unavailable=0
gpgcheck=1
gpgkey=http://binaries.projectcalico.org/rpm/key
priority=97
EOF

```
Install the dockerless-calico rpm:
```
wget https://github.com/projectcalico/releases/v0.10.1/calico-docker.rpm
yum install ./calico-docker.rpm
```

## Configure Calico-Dockerless
Add the following line to `/etc/calico/calico-environment`:

    ETCD_AUTHORITY

## Start Calico-Dockerless

    systemctl start calico-dockerless
