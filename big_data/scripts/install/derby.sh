#!/bin/bash

# Define the Derby version
DERBY_VERSION=10.15.2.0

# Define the installation directory
DERBY_INSTALL_DIR=$HADOOP_HOME/derby

# Create the installation directory
sudo mkdir -p $DERBY_INSTALL_DIR

# Check if Derby is already installed
if [ -d "$DERBY_INSTALL_DIR" ]; then
  echo "Apache Derby is already installed in $DERBY_INSTALL_DIR. "
  exit 0
else
  echo "Downloading Apache Derby..."
  sudo wget -P /tmp https://downloads.apache.org/db/derby/db-derby-$DERBY_VERSION/db-derby-$DERBY_VERSION-bin.tar.gz
fi

# Extract the downloaded archive
echo "Extracting Apache Derby..."
sudo tar -xf /tmp/db-derby-$DERBY_VERSION-bin.tar.gz -C /tmp

# Move Derby files to the installation directory
sudo mv /tmp/db-derby-$DERBY_VERSION-bin/* $DERBY_INSTALL_DIR

# Set environment variables for Derby
echo "export DERBY_HOME=$DERBY_INSTALL_DIR" >> ~/.bashrc
echo "export PATH=\$PATH:\$DERBY_HOME/bin" >> ~/.bashrc
source ~/.bashrc

echo "Apache Derby $DERBY_VERSION has been installed to $DERBY_INSTALL_DIR."
