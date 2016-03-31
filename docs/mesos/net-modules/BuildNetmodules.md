# Install Net-modules
These instructions cover how to manually compile net-modules on top of the official Mesos release.

1. Install official Mesos
    ```
    rpm -Uvh http://repos.mesosphere.com/el/7/noarch/RPMS/mesosphere-el-repo-7-1.noarch.rpm
    yum -y install mesos-0.28.0
    ```

2. Install Dependencies
    ```
    yum groupinstall -y "Development Tools"
    yum install -y \
       git \
      python-devel \
          libcurl-devel \
          python-setuptools \
          python-pip \
          python-wheel 
    ```
        
3. Get 3rd party dependency source files. Since Mesos doesn't ship with them, we'll grab them from github.
    ```
    # GLOG - glog's header files are produced during preprocessing:
    curl -O https://github.com/apache/mesos/blob/0.28.0/3rdparty/libprocess/3rdparty/glog-0.3.3.tar.gz
    curl -O https://raw.githubusercontent.com/apache/mesos/0.28.0/3rdparty/libprocess/3rdparty/glog-0.3.3.patch
    tar -xvf glog-0.3.3.tar.gz
    cd glog-0.3.3
    git apply ../glog-0.3.3.patch
    ./configure
    cd -
    
    # BOOST
    curl -O https://github.com/apache/mesos/blob/0.28.0/3rdparty/libprocess/3rdparty/boost-1.53.0.tar.gz
    tar -xvf boost-1.53.0.tar.gz
    
    # PROTOBUF
    curl -O https://github.com/apache/mesos/blob/0.28.0/3rdparty/libprocess/3rdparty/protobuf-2.5.0.tar.gz
    tar -xvf protobuf-2.5.0.tar.gz
    ```

4. Download netmodules
    ```
    curl -O -L https://github.com/mesosphere/net-modules/archive/master.tar.gz
    ```

5. Build netmodules
    ```
    export CPPFLAGS='-I~/protobuf/protobuf-2.5.0/src/ -I~/glog/glog-0.3.3/src/ -I~/boost/boost-1.53.0/'
    ./bootstrap
    ./configure --prefix=/usr --with-mesos=/
    make
    sudo make install
    ```
