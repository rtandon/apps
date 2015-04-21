
############################
#
############################

#How to Compile
	mvn package
	java -cp '.:./target/my-app-1.0-SNAPSHOT.jar' com.mycompany.app3.App3
	mvn clean compile package

#How execute Hadoop MyWordCount1 Job 
	~/hadoop/bin/hadoop jar target/my-app-1.0-SNAPSHOT.jar com.mycompany.MyHadoopSamples1.MyWordCount1 /user/hduser/gutenberg /user/hduser/gutenberg-output1
