# Dockerless Calico - Manual Installation
Project Calico releases are primarily distributed as docker containers for quick, easy, and consistant deployment. However, it is possible to run the core calico components on bare metal, removing the dependency on docker.

This guide will walk through how to manually create services and configurations to run Calico on Centos7 without Docker. **Note: This guide merely documents what the [dockerless-calico-rpm](#) will automatically do for you. We recommend following the [Dockerless Calico RPM Installation Guide] which will perform all of the following steps for you.**

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

## Configure Host
Configure this host for calico with calicoctl. Be sure to substitute ETCD_AUTHORITY with the address of your etcd cluster.
```
$ wget https://github.com/projectcalico/calico-docker/releases/download/v0.10.0/calicoctl
$ chmod +x ./calicoctl
$ ETCD_AUTHORITY=<etcd_ip> calicoctl node --runtime=none
```

## Bird
Each compute host will need to run bird which provides network routing on the host. Bird configurations must specify each host they are paired with in thier config. There are two ways to create this configuration:

- Automatically with confd (recommended): Confd can be configured to generate the etcd configuration by watching etcd for new host entries and reconfiguring bird appropriately.
- Manually: Generation of the bird config can be done manually, but must be also be updated manually each time a new host is added to the cluster.

### Option 1: Automatically with confd (recommended)
You'll need a number of files to get going. The easiest way to get them is to clone the calico-docker repo:

    git clone calico-docker.git
    
Move the confd files into place

    mkdir -p /etc/calico/
    cp -r calico_node/filestystem/confd /etc/calico/

Create an environment file for confd at `/etc/calico/calico-environment` with the following information:

    ETCD_AUTHORITY=<ip:port>
    IP=<local-ip>

Create a systemd service to launch confd at `/usr/lib/systemd/system/calico-dockerless-confd.service:

    [Unit]
    Description=confd for Dockerless Calico
    Requires=calico-dockerless.service
    Requires=calico-dockerless-bird.service
    After=calico-dockerless.service
    Before=calico-dockerless-bird.service
    
    [Service]
    ExecStartPre=/usr/bin/bash -c '/usr/bin/sed "s/HOSTNAME/$HOSTNAME/" /etc/calico/confd/templates/bird_aggr.toml.template > /etc/calico/confd/conf.d/bird_aggr.toml'
    ExecStartPre=/usr/bin/bash -c '/usr/bin/sed "s/HOSTNAME/$HOSTNAME/" /etc/calico/confd/templates/bird6_aggr.toml.template > /etc/calico/confd/conf.d/bird6_aggr.toml'
    ExecStartPre=/usr/bin/confd -confdir=/etc/calico/confd/ -onetime -node $ETCD_AUTHORITY
    ExecStart=/usr/bin/confd -confdir=/etc/calico/confd/ -interval=5 -watch -node $ETCD_AUTHORITY
    EnvironmentFile=/etc/calico/calico-environment
    
    [Install]
    WantedBy=multi-user.target

### Option 2: Manually with Static Configs

Create `/etc/bird.conf`. The following three steps detail a basic implementation of bird for use with Calico:

1. Variable Definitions. Change these to match your desired configuration:
    ```
    define router_id = 172.17.0.48;
    define default_pool = 192.168.0.0/16;
    define local_as = 64511;
    router id 172.17.0.48;
    ```
    
2. Core Routing Functionality. This uses the variables above to correctly configure bird for calico, and do not need to be modified to get up and running:
    ```
    filter calico_pools {
      if ( net ~ default_pool ) then {
        accept;
      }
      reject;
    }
    
    filter calico_ipip {
      accept;
    }
    
    # Configure synchronization between routing tables and kernel.
    protocol kernel {
      learn;             # Learn all alien routes from the kernel
      persist;           # Don't remove routes on bird shutdown
      scan time 2;       # Scan kernel routing table every 2 seconds
      import all;
      export filter calico_ipip; # Default is export none
      graceful restart;  # Turn on graceful restart to reduce potential flaps in
                         # routes when reloading BIRD configuration.  With a full
                         # automatic mesh, there is no way to prevent BGP from
                         # flapping since multiple nodes update their BGP
                         # configuration at the same time, GR is not guaranteed to
                         # work correctly in this scenario.
    }
    
    # Watch interface up/down events.
    protocol device {
      debug { states };
      scan time 2;    # Scan interfaces every 2 seconds
    }
    
    protocol direct {
      debug { states };
      interface -"cali*", "*"; # Exclude cali* but include everything else.
    }
    
    # Template for all BGP clients
    template bgp bgp_template {
      debug { states };
      description "Connection to BGP peer";
      local as local_as;
      multihop;
      gateway recursive; # This should be the default, but just in case.
      import all;        # Import all routes, since we don't know what the upstream
                         # topology is and therefore have to trust the ToR/RR.
      export filter calico_pools;  # Only want to export routes for workloads.
      next hop self;     # Disable next hop processing and always advertise our
                         # local address as nexthop
      source address router_id;  # The local address we use for the TCP connection
      add paths on;
      graceful restart;
    }
    ```
    
3. Lastly, you'll need to add an explicit BGP Peer connection to each other calico host you are setting up in your cluster:
    ```
    # Sample Static Peer: For peer /host/db0eec5a4c7a/ip_addr_v4
    protocol bgp Mesh_172_17_0_23 from bgp_template {
      neighbor 172.17.0.23 as local_as;
    }
    ```

## Install and Run Bird
With the configuration files in place, we can now start BIRD. Calico provides a patched release of Bird for use with Calico which includes tunnel support:

    curl -L https://github.com/projectcalico/calico-bird/releases/download/v0.1.0/bird -o /sbin/bird

Create a systemd service to launch bird at `/usr/lib/systemd/system/bird.service`:

    [Unit]
    Description=BIRD Internet Routing Daemon
    Wants=network.target
    After=network.target
    
    [Service]
    Type=forking
    ExecStart=/usr/sbin/bird -R -s /etc/calico/bird.ctl -d -c /etc/calico/confd/config/bird.cfg
    ExecReload=/bin/kill -HUP $MAINPID
    
    [Install]
    WantedBy=multi-user.target

Enable and run Bird:
```
systemctl enable /usr/lib/systemd/system/bird.service
systemctl start bird
```

## Installing Calico-Felix
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
Install the calico-felix package:
```
yum update
yum install -y calico-felix
systemctl start calico-felix
```

Create a felix.cfg:

    cp /etc/calico/felix.cfg.example /etc/calico/felix.cfg

Edit ETCD_IP in your new felix.cfg. Then start calico-felix:

    systemctl start calico-felix


[libvert-wiki][http://wiki.libvirt.org/page/Guest_won%27t_start_-_warning:_could_not_open_/dev/net/tun_%28%27generic_ethernet%27_interface%29]