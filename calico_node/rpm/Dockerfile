# NOTE: When building with this dockerfile, use /calico_node as
# the docker path so "common" files and "docker_dist" files can be accessed.
# e.g: docker build -f calico_node/rpm/Dockerfile calico_node

FROM centos:7
ENV CALICO_DOCKER_VERSION v0.10.0

# Install dependencies
RUN yum install -y epel-release wget rpm-build

RUN mkdir -p /root/rpmbuild/SOURCES/bin

# Add calicoctl
RUN wget https://github.com/projectcalico/calico-docker/releases/download/${CALICO_DOCKER_VERSION}/calicoctl -O /root/rpmbuild/SOURCES/calicoctl
RUN curl -L https://github.com/projectcalico/confd/releases/download/v0.10.0-scale/confd.static -o /root/rpmbuild/SOURCES/confd
RUN curl -L https://github.com/projectcalico/calico-bird/releases/download/v0.1.0/bird -o /root/rpmbuild/SOURCES/bird

# Add systemd files
COPY common/ /root/rpmbuild/SOURCES/
COPY rpm/files/ /root/rpmbuild/SOURCES/
RUN rm /root/rpmbuild/SOURCES/confd-files/templates/README.md
RUN mv /root/rpmbuild/SOURCES/confd-files /tmp/

RUN tar -C /tmp -cvf /root/rpmbuild/SOURCES/calico-dockerless-confd-templates.tar.gz confd-files

# Build RPM
ADD ./rpm/calico-dockerless.spec /root/calico-dockerless.spec
