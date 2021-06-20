package it.unipi.spark;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.api.java.function.Function;
import org.apache.spark.api.java.function.Function2;
import org.apache.spark.api.java.function.PairFlatMapFunction;
import org.apache.spark.api.java.function.PairFunction;
import scala.Tuple2;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class PageRank {
    public static void main(String[] args){
        if(args.length < 4){
            System.err.println("Follow this sample: <Iteration> <Alpha> <Input Path> <Output Path>");
            System.exit(-1);
        }

        //Get Spark Context
        SparkConf sparkConf = new SparkConf().setAppName("pageRankSpark").setMaster("local");
        JavaSparkContext sc = new JavaSparkContext(sparkConf);

        int iteration = Integer.parseInt(args[0]);
        final float alpha = Float.parseFloat(args[1]);
        String inputPath = args[2];
        String outputPath = args[3];

        //Get the input data from text file and put these in rdd
        JavaRDD<String> inputData = sc.textFile(inputPath);
        //Save the total number of nodes
        final long totalNode = inputData.count();

        JavaPairRDD<String, List<String>> rows = inputData.mapToPair(new PairFunction<String, String, List<String>>() {
            public Tuple2<String, List<String>> call(String line) throws Exception {
                Pattern titlePattern = Pattern.compile("<title>(.*)</title>");
                Pattern textPattern = Pattern.compile("<text(.*?)</text>");
                Pattern outLinkPattern = Pattern.compile("\\[\\[(.*?)\\]\\]");

                String title="";
                Matcher titleMatcher = titlePattern.matcher(line);
                if(titleMatcher.find()) {
                    title = titleMatcher.group(1).trim().split("\\|")[0];
                }

                String innerText = "";
                Matcher innerTextMatcher = textPattern.matcher(line);
                if(innerTextMatcher.find()) {
                    innerText = innerTextMatcher.group(1);
                }

                List<String> outlinks = new ArrayList<String>();
                Matcher outlinksMatcher = outLinkPattern.matcher(innerText);
                while(outlinksMatcher.find()){
                    String aux = outlinksMatcher.group(1);
                    outlinks.add(aux.trim().split("\\|")[0]);
                }
                return new Tuple2<String, List<String>>(title, outlinks);
            }
        }).cache();

        JavaPairRDD<String, Float> pagerank = rows.mapValues(new Function<List<String>, Float>() {
            public Float call(List<String> strings) throws Exception {
                return (float) 1/totalNode;
            }
        });

        for(int i=0; i<iteration; i++){
            JavaPairRDD<String, Tuple2<List<String>, Float>> parseOutput = rows.join(pagerank);
            JavaPairRDD<String, Float> pagerankContribution = parseOutput.flatMapToPair(new PairFlatMapFunction<Tuple2<String, Tuple2<List<String>, Float>>, String, Float>() {
                public Iterator<Tuple2<String, Float>> call(Tuple2<String, Tuple2<List<String>, Float>> tupla) throws Exception {
                    String titlePage = tupla._1;
                    List<String> outlinks = tupla._2._1;
                    Float pagerank = tupla._2._2;

                    List<Tuple2<String, Float>> returnList = new ArrayList<Tuple2<String, Float>>();
                    if(outlinks.size()>0){
                        Float pagerankContribution = pagerank/outlinks.size();
                        for(String outlink:outlinks){
                            returnList.add(new Tuple2<String, Float>(outlink, pagerankContribution));
                        }
                    }
                    returnList.add(new Tuple2<String, Float>(titlePage, 0.0f));
                    return returnList.iterator();
                }
            });

            JavaPairRDD<String, Float> totalPR = pagerankContribution.reduceByKey(new Function2<Float, Float, Float>() {
                public Float call(Float aFloat, Float aFloat2) throws Exception {
                    return aFloat + aFloat2;
                }
            });

            pagerank = totalPR.mapValues(new Function<Float, Float>() {
                public Float call(Float aFloat) throws Exception {
                    return ((alpha/totalNode)+((1-alpha)*aFloat));
                }
            });
        }

        JavaPairRDD<String, Float> rankOutput = pagerank.mapToPair(x -> x.swap()).sortByKey(false).mapToPair(x -> x.swap());

        rankOutput.saveAsTextFile(outputPath);
    }
}
