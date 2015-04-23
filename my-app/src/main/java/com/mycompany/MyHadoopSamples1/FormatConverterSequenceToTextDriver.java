/*********************************************************************************************************
** Driver
** formatProject/FormatConverterTextToSequence/src/FormatConverterSequenceToTextDriver.java
*********************************************************************************************************/

package com.mycompany.MyHadoopSamples1;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.input.SequenceFileInputFormat;
import org.apache.hadoop.mapreduce.Job;
 
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

/*
 * This file convert the sequence file of the Map/reduce WikipediaToItemPrefsMapper_Reducer1
 */
public class FormatConverterSequenceToTextDriver extends Configured implements Tool {
 
//@Override
	public int run(String[] args) throws Exception {
	 
		if (args.length != 2) {
			System.out.printf("Two parameters need to be supplied - <input dir> and <output dir>\n");
			return -1;
		}
		 
		Job job = new Job(getConf());
		job.setJarByClass(FormatConverterSequenceToTextDriver.class);
		job.setJobName("Convert Sequence File and Output as Text");
		 
		FileInputFormat.setInputPaths(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));
		 
		job.setInputFormatClass(SequenceFileInputFormat.class);
		job.setMapperClass(FormatConverterMapper1.class);
		job.setNumReduceTasks(0);
		 
		boolean success = job.waitForCompletion(true);
		return success ? 0 : 1;
	}
 
	public static void main(String[] args) throws Exception {
		int exitCode = ToolRunner.run(new Configuration(), new FormatConverterSequenceToTextDriver(), args);
		System.exit(exitCode);
	}
} 