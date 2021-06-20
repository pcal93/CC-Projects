import sys
from operator import add
import re
from pyspark import SparkContext

def line_parser(row):
    title_page = row[row.find("<title>")+7:row.find("</title>")]
    inner_text = row[row.find("<text"):row.find("</text>")]
    outlinks = re.findall("\\[\\[(.*?)\\]\\]", inner_text)
    ret_outlinks = []

    for item in outlinks:
        item_splitted = item.split("|")
        if len(item_splitted) < 2:
            ret_outlinks.append(item)
            continue
        ret_outlinks.append(item_splitted[0])
    return title_page, ret_outlinks


def rank_calculator(row):
    title_page = row[0]
    outlinks = row[1][0]
    pagerank = row[1][1]
    outlinks_size = len(outlinks)
    return_list = []
    if outlinks_size > 0:
        pagerank_contr = pagerank/outlinks_size
        for outlink in outlinks:
            return_list.append([outlink, pagerank_contr])
    return_list.append([title_page, 0])
    return return_list


def pr_calculator(row, alpha, total_node):
    final_pr = ((alpha/total_node)+((1-alpha)*row))
    return final_pr


if __name__ == "__main__":

    if len(sys.argv) != 5:
        print("Follow this sample: <Iteration> <Alpha> <Input Path> <Output Path>")
        sys.exit(-1)

    # Get Spark Context
    sc = SparkContext("yarn", "PageRank")

    iteration = int(sys.argv[1])
    alpha = float(sys.argv[2])
    input_path = sys.argv[3]
    output_path = sys.argv[4]

    # Get the input data from text file and put these in rdd
    input_data = sc.textFile(input_path).cache()
    # Save the total number of nodes
    total_node = input_data.count()

    rows = input_data.map(lambda row: line_parser(row)).cache()

    pagerank = rows.mapValues(lambda rank: 1/total_node)

    for i in range(iteration):
        parse_output = rows.join(pagerank)

        print(parse_output.collect())
        print("parse_output")

        pagerank_contribution = parse_output.flatMap(lambda row: rank_calculator(row))

        print(pagerank_contribution.collect())
        print("pr_contribution")

        total_PR = pagerank_contribution.reduceByKey(add)

        pagerank = total_PR.mapValues(lambda row: pr_calculator(row, alpha, total_node))

    rank_output = pagerank.sortBy(lambda row: row[1], False)
    rank_output.saveAsTextFile(output_path)
