FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    openssh-server \
    rsync \
    wget \
    curl \
    procps \
    python3 \
    python3-pip \
    && apt-get clean

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

ENV HDFS_NAMENODE_USER=root
ENV HDFS_DATANODE_USER=root
ENV HDFS_SECONDARYNAMENODE_USER=root

RUN wget https://archive.apache.org/dist/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz \
    && tar -xzf hadoop-3.3.6.tar.gz -C /opt \
    && mv /opt/hadoop-3.3.6 $HADOOP_HOME \
    && rm hadoop-3.3.6.tar.gz

RUN echo "export JAVA_HOME=$JAVA_HOME" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

RUN mkdir -p /var/run/sshd /root/.ssh \
    && sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config \
    && sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config

RUN echo '<configuration><property><name>fs.defaultFS</name><value>hdfs://localhost:9000</value></property></configuration>' \
    > $HADOOP_HOME/etc/hadoop/core-site.xml

RUN echo '<configuration><property><name>dfs.replication</name><value>1</value></property><property><name>dfs.namenode.name.dir</name><value>file:///tmp/hadoop-root/dfs/name</value></property><property><name>dfs.datanode.data.dir</name><value>file:///tmp/hadoop-root/dfs/data</value></property></configuration>' \
    > $HADOOP_HOME/etc/hadoop/hdfs-site.xml

EXPOSE 9000 9870 22

CMD ["/bin/bash", "-c", "service ssh start && if [ ! -f /root/.ssh/id_rsa ]; then ssh-keygen -t rsa -P '' -f /root/.ssh/id_rsa; fi && cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys && sort -u /root/.ssh/authorized_keys -o /root/.ssh/authorized_keys && chmod 600 /root/.ssh/authorized_keys && ssh-keyscan -H localhost >> /root/.ssh/known_hosts 2>/dev/null || true; if [ ! -d /tmp/hadoop-root/dfs/name/current ]; then hdfs namenode -format -nonInteractive; fi; start-dfs.sh; tail -f /dev/null"]
