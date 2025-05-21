if [ -f run.unlock ]; then
    echo "Unlock file exists, exiting"
else
    java -Dlog4j2.configurationFactory=pol.log.CustomConfigurationFactory -Dlog.rootDirectory=logs -Dsimulation.test=c01 -jar ../../jar/pol.jar -configuration modified.properties -until 24192
fi
