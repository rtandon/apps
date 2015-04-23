#~/hadoop/bin/hadoop dfs -rmr /user/hduser/mia/ch6/output1 
#./compile.sh
#./run.sh


~/hadoop/bin/hadoop dfs -rmr /user/hduser/mia/ch6/output1 
~/hadoop/bin/hadoop dfs -rmr /user/hduser/mia/ch6/output2 
./myscp.sh
./compile.sh
./run.sh
~/hadoop/bin/hadoop jar target/my-app-1.0-SNAPSHOT-jar-with-dependencies.jar com.mycompany.MyHadoopSamples1.FormatConverterSequenceToTextDriver /user/hduser/mia/ch6/output1/part-r-00000 /user/hduser/mia/ch6/output2

