/***
 *This code allows us to read the large vector in chunk 
 *and write the same in mahout understandable sequence file. 
 *Hence we are able to scale the solution in terms of 
 *reading data in chunks
 */
package mia.clustering.ch07;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import javax.xml.stream.events.EndDocument;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.SequenceFile;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.util.Shell.ExitCodeException;
import org.apache.mahout.clustering.WeightedVectorWritable;
import org.apache.mahout.clustering.kmeans.Cluster;
import org.apache.mahout.clustering.kmeans.KMeansDriver;
import org.apache.mahout.common.distance.EuclideanDistanceMeasure;
import org.apache.mahout.math.RandomAccessSparseVector;
import org.apache.mahout.math.Vector;
import org.apache.mahout.math.VectorWritable;

public class SimpleKMeansClustering {
  public static final double[][] points = { {1, 1}, {2, 1}, {1, 2},
                                           {2, 2}, {3, 3}, {8, 8},
                                           {9, 8}, {8, 9}, {9, 9}};

  public static final double[][] points1 = { {2, 2}, {3, 3}, {8, 8},
      										{9, 8}, {8, 9}, {9, 9}};


  public static final double[][] points2 = { {1, 1}, {2, 1}, {1, 2}};
  
  public static void writePointsToFile(List<Vector> points,
                                       String fileName,
                                       FileSystem fs,
                                       Configuration conf) throws IOException {
    Path path = new Path(fileName);
    SequenceFile.Writer writer = new SequenceFile.Writer(fs, conf,
        path, LongWritable.class, VectorWritable.class);
    long recNum = 0;
    VectorWritable vec = new VectorWritable();
    for (Vector point : points) {
      vec.set(point);
      writer.append(new LongWritable(recNum++), vec);
    }
    writer.close();
  }

  public static long writePointsToFile(List<Vector> points,
          String fileName,
          FileSystem fs,
          Configuration conf , long recNum ,SequenceFile.Writer writer) throws IOException {
//	Path path = new Path(fileName);
//	SequenceFile.Writer writer = new SequenceFile.Writer(fs, conf,
//	path, LongWritable.class, VectorWritable.class);
//	long recNum = 0;
	VectorWritable vec = new VectorWritable();
	for (Vector point : points) {
	vec.set(point);
	writer.append(new LongWritable(recNum++), vec);
	}
	return recNum;
}

  
  public static List<Vector> getPoints(double[][] raw) {
    List<Vector> points = new ArrayList<Vector>();
    for (int i = 0; i < raw.length; i++) {
      double[] fr = raw[i];
      Vector vec = new RandomAccessSparseVector(fr.length);
      vec.assign(fr);
      points.add(vec);
    }
    return points;
  }
  
  public static void main(String args[]) throws Exception {
    
    int k = 2;
    Configuration conf = new Configuration();
    FileSystem fs = FileSystem.get(conf);

    List<Vector> vectors = getPoints(points);

    List<Vector> vectors1 = getPoints(points1);
    List<Vector> vectors2 = getPoints(points2);

    File testData = new File("testdata");
    if (!testData.exists()) {
      testData.mkdir();
    }
    testData = new File("testdata/points");
    if (!testData.exists()) {
      testData.mkdir();
    }
    
//    Configuration conf = new Configuration();
//    FileSystem fs = FileSystem.get(conf);
//    writePointsToFile(vectors, "testdata/points/file1", fs, conf);

    String fileName = "testdata/points/file1" ;
    
	Path path = new Path(fileName);
	SequenceFile.Writer writer1 = new SequenceFile.Writer(fs, conf,
	path, LongWritable.class, VectorWritable.class);
    long recNum = 0;
    recNum = writePointsToFile(vectors1, "testdata/points/file1", fs, conf , recNum , writer1);
    System.out.println("recNum == " + recNum );
    recNum = writePointsToFile(vectors2, "testdata/points/file1", fs, conf , recNum , writer1);
    System.out.println("recNum == " + recNum );
	writer1.close();

    
//    SequenceFile.Reader reader = new SequenceFile.Reader(fs,
//    		new Path("testdata/points/file1"), conf);
//
//    LongWritable key = new LongWritable();
//	VectorWritable value = new VectorWritable() ; // new WeightedVectorWritable();
//	while (reader.next(key, value)) {
////		Vector randVec = value.get();
//		System.out.println(key.toString() + " ------- " + value.toString());
//	}
//	reader.close();

    
    Path path1 = new Path("testdata/clusters/part-00000");
    SequenceFile.Writer writer = new SequenceFile.Writer(fs, conf,
        path1, Text.class, Cluster.class);
    
    for (int i = 0; i < k; i++) {
      Vector vec = vectors1.get(i);
      Cluster cluster = new Cluster(vec, i, new EuclideanDistanceMeasure());
      writer.append(new Text(cluster.getIdentifier()), cluster);
    }
    writer.close();
    
    
////    Vector vec = vectors2.get(1);
////    Cluster cluster = new Cluster(vec, 0, new EuclideanDistanceMeasure());
////    writer.append(new Text(cluster.getIdentifier()), cluster);
////
////    vec = vectors2.get(2);
////    cluster = new Cluster(vec, 1, new EuclideanDistanceMeasure());
////    writer.append(new Text(cluster.getIdentifier()), cluster);
////
////    writer.close();
//
////////////////////////////////////////////////////////////////////////////////////////////

    
    
    KMeansDriver.run(conf, new Path("testdata/points"), new Path("testdata/clusters"),
      new Path("output"), new EuclideanDistanceMeasure(), 0.001, 10,
      true, false);
    
    System.out.println("Cluster.CLUSTERED_POINTS_DIR === " + Cluster.CLUSTERED_POINTS_DIR);
    
    SequenceFile.Reader reader = new SequenceFile.Reader(fs,
        new Path("output/" + Cluster.CLUSTERED_POINTS_DIR
                 + "/part-m-00000"), conf);
    
    IntWritable key = new IntWritable();
    WeightedVectorWritable value = new WeightedVectorWritable();
    while (reader.next(key, value)) {
      System.out.println(value.toString() + " belongs to cluster "
                         + key.toString());
    }
    reader.close();
  }
  
}
