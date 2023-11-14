#!/usr/bin/env bash

PIG_VERSION=0.17.0
PIG_HOME=$HADOOP_HOME/pig

sudo mkdir -p "$PIG_HOME"
sudo chown "$(whoami)":"$(whoami)" -R "$PIG_HOME"

# Download and extract Pig
echo "Downloading Pig ${PIG_VERSION}..."
sudo wget -nc https://downloads.apache.org/pig/pig-${PIG_VERSION}/pig-${PIG_VERSION}.tar.gz -P /tmp
sudo tar -xzf /tmp/pig-${PIG_VERSION}.tar.gz -C "$PIG_HOME" --strip-components=1
sudo chown "$(whoami)":"$(whoami)" -R "$PIG_HOME"

# Set up environment variables
{
  echo "PIG_HOME=${PIG_HOME}"
  echo "PATH=\$PATH:\$PIG_HOME/bin:"
  echo "export PIG_HOME"
  echo "export PATH"
} >> ~/.bashrc

# Display installation completion message
echo "Apache Pig ${PIG_VERSION} has been installed to ${PIG_HOME}."
echo "Make sure to start a new terminal or run 'source ~/.bashrc' to apply the changes."
