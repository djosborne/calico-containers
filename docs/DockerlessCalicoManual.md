# Dockerless Calico - Manual Installation
Project Calico releases are primarily distributed as docker containers for quick, easy, and consistant deployment. However, it is possible to run the core calico components on bare metal, removing the dependency on docker.

This guide will walk through how to manually create services and configurations to run Calico on Centos7 without Docker.

# WARNING: Dockerless Calico is Experimental!
Some `calicoctl` commands rely on a running `calico-node` container, and may not function properly when calico is run on baremetal. Please raise any encountered issues on [calico-docker](calico-docker) and message us on [calico-slack](https://calicousers-slackin.herokuapp.com/).

## Install Dependencies
1. Make changes to SELinux and QEMU config to allow VM interfaces with type='ethernet' ([this libvirt Wiki page][libvirt-wiki] explains why these changes are required):
    ```
    setenforce permissive
    ```
    
2. Edit `/etc/selinux/config` and change the `SELINUX=` line to the following:
    ```
    SELINUX=permissive
    ```

## Install calico-felix
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

Calico relies on a few epel packages. Ensure you have the EPEL repos: `$ yum install -y epel-release`

Then install calico-felix: `$ yum install -y calico-felix`

Until calico-felix 0.3.0 is released, you'll have to manually install a few runtime deps: `yum install -y posix-spawn  python-gevent python-eventlet python-etcd`


## Install
Install Binaries
```
# calicoctl
$ curl -L https://github.com/projectcalico/calico-docker/releases/download/v0.12.0/calicoctl -o /usr/local/bin/calicoctl
$ chmod +x /usr/local/bin/calicoctl

# bird
$ curl -L https://github.com/projectcalico/calico-bird/releases/download/v0.1.0/bird -o /usr/local/bin/bird
$ chmod +x /usr/local/bin/bird

# confd
$ curl -L https://github.com/projectcalico/confd/releases/download/v0.10.0-scale/confd.static -o /usr/local/bin/confd
$ chmod +x /usr/local/bin/confd
```

Install systemd services
```
$ git clone https://github.com/project-calico/calico-docker.git
$ cp -R calico-docker/calico_node/common/confd/ /etc/calico/
$ cp calico-docker/calico_node/rpm/files/calico-dockerless*.service /usr/lib/systemd/
$ systemctl enable /usr/lib/systemd/calico-dockerless*.service
```

calico-confd requires a binary available in $PATH which can restart calico-confd:
```
$ cp calico-docker/calico_node/rpm/restart-calico-confd /usr/local/bin
$ chmod +x /usr/local/bin/restart-calico-confd
```

Create calico environment file at `/etc/calico/calico-environment`:
```
ETCD_AUTHORITY=<EtcdIP:Port>
IP=<LocalIP>
```

We'll need to also create a felix.cfg file. Copy the sample:

    $ cp /etc/calico/felix.cfg.example /etc/calico/felix.cfg
    
Then uncomment and edit `EtcdAddr`.




# Start 'er up
```
systemctl start calico-dockerless
```
[libvert-wiki][http://wiki.libvirt.org/page/Guest_won%27t_start_-_warning:_could_not_open_/dev/net/tun_%28%27generic_ethernet%27_interface%29]
