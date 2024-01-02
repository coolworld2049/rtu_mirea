#!/bin/bash

# Install OpenJDK 8
echo "Installing OpenJDK 8..."
sudo apt-get install -y openjdk-8-jdk
echo "OpenJDK 8 installed successfully."

# Set up Java environment variables
JAVA_HOME=$(readlink -f /usr/bin/java | sed "s:bin/java::")
echo "Setting up Java environment variables..."
echo "JAVA_HOME=$JAVA_HOME" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh
echo "Java environment variables set up successfully."

echo "Setting up Hadoop environment variables..."
{
  echo "JAVA_HOME=$JAVA_HOME"
  echo "PATH=\$PATH:\$JAVA_HOME/bin:"
  echo "export JAVA_HOME"
  echo "export PATH"
} >> ~/.bashrc

echo "Make sure to start a new terminal or run 'source ~/.bashrc' to apply the changes."
