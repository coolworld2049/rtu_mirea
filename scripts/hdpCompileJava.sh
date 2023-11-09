#!/bin/bash

#export HADOOP_CLASSPATH=$JAVA_HOME/lib/tools.jar
#hadoop com.sun.tools.javac.Main $1
export HADOOP_JARS=$HADOOP_HOME/share/hadoop
javac -cp $HADOOP_JARS/common/hadoop-common-2.9.2.jar:$HADOOP_JARS/mapreduce/hadoop-mapreduce-client-core-2.9.2.jar $1
bn=`basename $1 .java`
jar cf $bn.jar $bn*.class
