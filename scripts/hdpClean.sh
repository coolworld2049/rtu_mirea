#!/bin/bash

rm -rf /tmp/Jetty* && \
rm -rf /tmp/hadoop-`whoami` && \
hdfs namenode -format
