cd $DERBY_HOME/data

# If you are using JDK 1.7u51+, you'll need to either specify an ephemeral port (typically between 49152 and 65535)
# or add a grant to your JDK version's java.policy file.
# See http://stackoverflow.com/questions/21154400/unable-to-start-derby-database-from-netbeans-7-4 for details.
nohup $DERBY_HOME/startNetworkServer -h 0.0.0.0 &