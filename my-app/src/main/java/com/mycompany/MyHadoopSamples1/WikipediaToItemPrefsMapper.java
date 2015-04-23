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
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;
import org.apache.mahout.math.VarLongWritable;

//import com.mycompany.MyHadoopSamples1.MyWordCount2.TokenizerMapper;



//public class WikipediaToItemPrefsMapper {

public final class WikipediaToItemPrefsMapper extends
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
//			PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter("links-converted.txt")));
			while (m.find()) {
				itemID.set(Long.parseLong(m.group()));
//				out.println(userID + "," + Long.parseLong(m.group()));
				context.write(userID, itemID);
			}
//			out.close();
		}
//	}
	  public static void main(String[] args) throws Exception {
		    Configuration conf = new Configuration();
		    String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
		    if (otherArgs.length != 2) {
		      System.err.println("Usage: wordcount <in> <out>");
		      System.exit(2);
		    }
		    Job job = new Job(conf, "word count");
		    job.setJarByClass(WikipediaToItemPrefsMapper.class);
		    job.setMapperClass(WikipediaToItemPrefsMapper.class);
		    
		    //You can just set the number of reduce tasks to 0 by 
		    //using JobConf.setNumReduceTasks(0). This will make the 
		    //results of the mapper go straight into HDFS.
		    job.setNumReduceTasks(0);
		    
//		    job.setCombinerClass(WikipediaToUserVectorReducer.class);
//		    job.setReducerClass(WikipediaToUserVectorReducer.class);
		    
		    job.setOutputKeyClass(VarLongWritable.class);
		    job.setOutputValueClass(VarLongWritable.class);
		    FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
		    FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));
		    System.exit(job.waitForCompletion(true) ? 0 : 1);
		  }

}