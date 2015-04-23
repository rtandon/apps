/*********************************************************************************************************
** Mapper
** formatProject/FormatConverterTextToSequence/src/FormatConverterMapper.java
** Reads text file and emits the contents out as key-value pairs
*********************************************************************************************************/
 
package com.mycompany.MyHadoopSamples1;

import java.io.IOException;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
 
 
public class FormatConverterMapper extends
Mapper<LongWritable, Text, LongWritable, Text> {
 
@Override
public void map(LongWritable key, Text value, Context context)
throws IOException, InterruptedException {
context.write(key, value);
}
} 