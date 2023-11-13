#!/usr/bin/env bash

# Specify the Pig version
PIG_VERSION="0.17.0"

# Specify the mirror URL to download Pig
MIRROR_URL="https://downloads.apache.org/pig/pig-${PIG_VERSION}/pig-${PIG_VERSION}.tar.gz"

# Specify the directory where Pig will be installed
INSTALL_DIR=$HADOOP_HOME/pig

# Download and extract Pig
echo "Downloading Pig ${PIG_VERSION}..."
wget -q "${MIRROR_URL}" -O pig-${PIG_VERSION}.tar.gz
tar -xzf pig-${PIG_VERSION}.tar.gz
rm pig-${PIG_VERSION}.tar.gz

# Move Pig to the installation directory
sudo mv pig-${PIG_VERSION} "${INSTALL_DIR}"

# Set up environment variables
echo "export PIG_HOME=${INSTALL_DIR}" >> ~/.bashrc
echo "export PATH=\$PATH:\$PIG_HOME/bin" >> ~/.bashrc

# Display installation completion message
echo "Apache Pig ${PIG_VERSION} has been installed to ${INSTALL_DIR}."
echo "Make sure to start a new terminal or run 'source ~/.bashrc' to apply the changes."
