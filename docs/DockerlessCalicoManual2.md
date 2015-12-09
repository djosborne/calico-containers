1. Add calico repos
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
2. Calico relies on a few epel packages. Ensure you have the EPEL repos: `yum install -y epel-release`

##  Calicoctl
```
$ wget https://github.com/projectcalico/calico-docker/releases/download/v0.12.0/calicoctl
$ chmod +x calicoctl
```

## confd
Install: `$ curl -L https://github.com/projectcalico/confd/releases/download/v0.10.0-scale/confd.static -o /usr/bin/confd`

```
$ git clone https://github.com/project-calico/calico-docker.git
$ cp -R calico-docker/calico_node/common/confd/ /etc/calico/
$ cp calico-docker/calico_node/rpm/files/*.service /usr/lib/system/
```

Create calico environment file at `/etc/calico/calico-environment`:
```
FELIX_ETCDADDR=<EtcdIP:Port>
ETCD_AUTHORITY=$FELIX_ETCDADDR
```

## Bird
1. `curl -L https://github.com/projectcalico/calico-bird/releases/download/v0.1.0/bird -o /usr/bin/bird`
2. `bird -s /run/bird.ctl -c /etc/calico/`

## Felix
3. `yum install -y calico-felix`
4. Until 0.3.0 is released, you'll have to manually install a few runtime deps: `yum install -y posix-spawn  python-gevent python-eventlet`
5. 

## Start er up
`systemctl start calico-dockerless`

