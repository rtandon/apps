#~/hadoop/bin/hadoop dfs -copyFromLocal ~/Downloads/20417-8.txt /user/hduser/gutenberg/20417-8.txt
#~/hadoop/bin/hadoop jar target/my-app-1.0-SNAPSHOT.jar com.mycompany.MyHadoopSamples1.MyWordCount2 /user/hduser/gutenberg /user/hduser/gutenberg-output1

#~/hadoop/bin/hadoop jar target/my-app-1.0-SNAPSHOT-jar-with-dependencies.jar com.mycompany.MyHadoopSamples1.WikipediaToItemPrefsMapper /user/hduser/mia/ch6/input/users.txt /user/hduser/mia/ch6/output1

#~/hadoop/bin/hadoop jar target/my-app-1.0-SNAPSHOT-jar-with-dependencies.jar com.mycompany.MyHadoopSamples1.WikipediaToItemPrefsMapper_Reducer /user/hduser/mia/ch6/input/users.txt /user/hduser/mia/ch6/output1

~/hadoop/bin/hadoop jar target/my-app-1.0-SNAPSHOT-jar-with-dependencies.jar com.mycompany.MyHadoopSamples1.WikipediaToItemPrefsMapper_Reducer1 /user/hduser/mia/ch6/input/users.txt /user/hduser/mia/ch6/output1

