/*
 * Source code for Listing 6.1
 * 
 */
//package mia.recommender.ch06;
package com.mycompany.MyHadoopSamples1;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Reducer.Context;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.SequenceFileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;
import org.apache.hadoop.util.ToolRunner;
import org.apache.mahout.common.AbstractJob;
import org.apache.mahout.math.RandomAccessSparseVector;
import org.apache.mahout.math.VarLongWritable;
import org.apache.mahout.math.Vector;
import org.apache.mahout.math.VectorWritable;
import org.apache.mahout.math.hadoop.*;
import org.apache.hadoop.mapreduce.*;

import com.mycompany.MyHadoopSamples1.MyWordCount1.IntSumReducer;
import com.mycompany.MyHadoopSamples1.MyWordCount1.TokenizerMapper;

//import com.mycompany.MyHadoopSamples1.MyWordCount2.TokenizerMapper;



//public class WikipediaToItemPrefsMapper {

public class WikipediaToItemPrefsMapper_Reducer1 extends AbstractJob{
	
	public static class WikipediaToItemPrefsMapper  extends
		Mapper<LongWritable, Text, VarLongWritable, VarLongWritable> {

			private final Pattern NUMBERS = Pattern.compile("(\\d+)");
		
			@Override
			protected void map(LongWritable key, Text value, Context context)
					throws IOException, InterruptedException {
				String line = value.toString();
				Matcher m = NUMBERS.matcher(line);
				m.find();
				VarLongWritable userID = new VarLongWritable(Long.parseLong(m.group()));
				VarLongWritable itemID = new VarLongWritable();
				while (m.find()) {
					itemID.set(Long.parseLong(m.group()));
					context.write(userID, itemID);
				}
			}
	}
	
	public static class WikipediaToUserVectorReducer
		extends	Reducer<VarLongWritable, VarLongWritable, VarLongWritable, VectorWritable> {

//		@Override
		public void reduce(VarLongWritable userID,
				Iterable<VarLongWritable> itemPrefs, Context context)
				throws IOException, InterruptedException {
			Vector userVector = new RandomAccessSparseVector(Integer.MAX_VALUE, 100);
			for (VarLongWritable itemPref : itemPrefs) {
				userVector.set((int) itemPref.get(), 1.0f);
			}
			context.write(userID, (new VectorWritable(userVector)) );
		}
	}

	public int run(String[] arg0) throws Exception {
		// TODO Auto-generated method stub

	    Configuration conf = new Configuration();
	    
//	    Job job = new Job(conf, "MyCommender1--WikipediaToItemPrefsMapper_Reducer");
	    
	    Job job_preferenceValues = new Job (getConf());
	    job_preferenceValues.setJarByClass(WikipediaToItemPrefsMapper_Reducer1.class);
	    job_preferenceValues.setJobName("job_preferenceValues");	    

	    job_preferenceValues.setInputFormatClass(TextInputFormat.class);
	    job_preferenceValues.setOutputFormatClass(SequenceFileOutputFormat.class);
//	    job_preferenceValues.setOutputFormatClass(TextOutputFormat.class);
	    

	    FileInputFormat.setInputPaths(job_preferenceValues, new Path(arg0[0]));
	    SequenceFileOutputFormat.setOutputPath(job_preferenceValues, new Path(arg0[1]));
	    FileOutputFormat.setOutputPath(job_preferenceValues, new Path(arg0[1]));

	    job_preferenceValues.setMapOutputKeyClass(VarLongWritable.class);
	    job_preferenceValues.setMapOutputValueClass(VarLongWritable.class);

	    job_preferenceValues.setOutputKeyClass(VarLongWritable.class);
	    job_preferenceValues.setOutputValueClass(VectorWritable.class);
//	    job_preferenceValues.setOutputValueClass(TextOutputFormat.class);
	    

	    job_preferenceValues.setMapperClass(WikipediaToItemPrefsMapper.class);
	    job_preferenceValues.setReducerClass(WikipediaToUserVectorReducer.class);
	    
	    job_preferenceValues.waitForCompletion(true);
	    
		return 0;
	}

	public static void main(String[] args) throws Exception {
		ToolRunner.run(new WikipediaToItemPrefsMapper_Reducer1(), args);
	}

	
//	  public void run(String inputPath, String outputPath) throws Exception {
//		    JobConf conf = new JobConf(WordCount.class);
//		    conf.setJobName("wordcount");
//
//		    // the keys are words (strings)
//		    conf.setOutputKeyClass(Text.class);
//		    // the values are counts (ints)
//		    conf.setOutputValueClass(IntWritable.class);
//
//		    conf.setMapperClass(MapClass.class);
//		    conf.setReducerClass(Reduce.class);
//
//		    FileInputFormat.addInputPath(conf, new Path(inputPath));
//		    FileOutputFormat.setOutputPath(conf, new Path(outputPath));
//
//		    JobClient.runJob(conf);
//	  }
	  
//	  public static void main(String[] args) throws Exception {
//		    Configuration conf = new Configuration();
//		    String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
//		    if (otherArgs.length != 2) {
//		      System.err.println("Usage: N/A...do it your self :-) and get lost..!!");
//		      System.exit(2);
//		    }
//		    Job job = new Job(conf, "MyCommender1--WikipediaToItemPrefsMapper_Reducer");
//		    job.setJarByClass(WikipediaToItemPrefsMapper_Reducer.class);
//		    job.setMapperClass(WikipediaToItemPrefsMapper.class);
//		    
//		    //You can just set the number of reduce tasks to 0 by 
//		    //using JobConf.setNumReduceTasks(0). This will make the 
//		    //results of the mapper go straight into HDFS.
////		    job.setNumReduceTasks(0);
//
//		    job.setCombinerClass(WikipediaToUserVectorReducer.class);
//		    job.setReducerClass(WikipediaToUserVectorReducer.class);
//		    
////		    job.setOutputFormatClass(SequenceFileOutputFormat.class);
//		    job.setOutputKeyClass(VarLongWritable.class);
//		    job.setOutputValueClass(VectorWritable.class);
//		    
//		    FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
//		    FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));
//		    System.exit(job.waitForCompletion(true) ? 0 : 1);
//		    
//		  }

}