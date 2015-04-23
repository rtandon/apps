/*********************************************************************************************************
** Mapper
** formatProject/FormatConverterTextToSequence/src/FormatConverterMapper.java
** Reads text file and emits the contents out as key-value pairs
*********************************************************************************************************/
 
package com.mycompany.MyHadoopSamples1;

//import java.io.IOException;

//import org.apache.hadoop.io.LongWritable;
import java.io.IOException;
import java.util.Iterator;

import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.mahout.cf.taste.hadoop.item.VectorOrPrefWritable;
import org.apache.mahout.math.VarLongWritable;
import org.apache.mahout.math.Vector;
import org.apache.mahout.math.VectorWritable;
 
 
public class FormatConverterMapper1 extends
	Mapper<VarLongWritable, VectorWritable, LongWritable, Text> {
 
//	@Override
//	public void map(VarLongWritable key, VectorWritable value, Context context) {
//		context.write(key, value);
//	}
	
	public void map(VarLongWritable key, VectorWritable value, Context context)
	        throws IOException, InterruptedException {
	    long userID = key.get();
	    Vector userVector = value.get();
	    Iterator<Vector.Element> it = userVector.iterateNonZero();
	    IntWritable itemIndexWritable = new IntWritable();
	    while (it.hasNext()) {
	        Vector.Element e = it.next();
	        int itemIndex = e.index();
	        IntWritable myItemIdx = new IntWritable(itemIndex);
	        
	        float preferenceValue = (float) e.get();
	        FloatWritable myPreferenceValue = new FloatWritable(preferenceValue);
	        
	        LongWritable myUserId = new LongWritable(userID);
	        
	        String item_pref = String.valueOf(itemIndex) + ":" + String.valueOf(myPreferenceValue);
	        Text my_Item_Pref = new Text(item_pref);
	        
	        
//	        context.write(myItemIdx,myPreferenceValue);
	        context.write(myUserId, my_Item_Pref);
	        
//	        itemIndexWritable.set(itemIndex);
//	        context.write(itemIndexWritable, 
//	                new VectorOrPrefWritable(userID, preferenceValue));
	    }
	}

} 