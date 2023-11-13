#!/bin/bash

# Define Hive version and installation directory
HIVE_VERSION=3.1.2
HIVE_HOME=$HADOOP_HOME/hive

echo "Downloading and installing Hive $HIVE_VERSION..."

# Download and extract Hive
wget https://downloads.apache.org/hive/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz -P /tmp
tar -xf /tmp/apache-hive-${HIVE_VERSION}-bin.tar.gz -C $HIVE_HOME --strip-components=1

echo "export HIVE_HOME=$HIVE_HOME" >> ~/.bashrc
echo 'export PATH=$PATH:$HIVE_HOME/bin' >> ~/.bashrc
source ~/.bashrc

echo "Hive downloaded and installed successfully."

# Copy Hive configuration files to /etc/hive/conf
echo "Copying Hive configuration files..."
sudo mkdir -p /etc/hive/conf
sudo cp $HIVE_HOME/conf/*.xml /etc/hive/conf
echo "Hive configuration files copied successfully."

# Create Hive warehouse directory in HDFS
echo "Creating Hive warehouse directory in HDFS..."
hdfs dfs -mkdir /user/$USER/warehouse
hdfs dfs -chmod g+w /user/$USER/warehouse
echo "Hive warehouse directory in HDFS created successfully."

# Start Derby metastore
echo "Starting Derby metastore..."
bash derby.sh
echo "Derby metastore started successfully."

# Configure Hive metastore in hive-site.xml
echo "Configuring Hive metastore in hive-site.xml..."
sudo mkdir ~/metastore
sudo bash -c "cat > $HIVE_HOME/conf/hive-site.xml <<EOL
<configuration>

<property>
  <name>hive.metastore.local</name>
  <value>true</value>
</property>

<property>
  <name>javax.jdo.option.ConnectionURL</name>
  <value>jdbc:derby:$HOME/metastore_db;create=true</value>
</property>

<property>
  <name>javax.jdo.option.ConnectionDriverName</name>
  <value>org.apache.derby.jdbc.EmbeddedDriver</value>
</property>

<property>
  <name>javax.jdo.option.ConnectionUserName</name>
  <value>username</value>
</property>

<property>
  <name>javax.jdo.option.ConnectionPassword</name>
  <value>password</value>
</property>

<property>
  <name>datanucleus.autoCreateSchema</name>
  <value>true</value>
</property>

<property>
  <name>datanucleus.fixedDatastore</name>
  <value>true</value>
</property>

<property>
  <name>datanucleus.autoCreateTables</name>
  <value>true</value>
</property>

</configuration>
EOL"
echo "Hive metastore configured successfully."

# Initialize Hive metastore schema
echo "Initializing Hive metastore schema..."
schematool -dbType derby -info
echo "Hive metastore schema initialized successfully."
