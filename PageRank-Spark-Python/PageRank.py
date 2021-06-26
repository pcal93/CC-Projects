import sys
from operator import add
import re
from pyspark import SparkContext

# Return titlePage and the list of outlinks
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

    # Get info from the row
    title_page = row[0]
    outlinks = row[1][0]
    pagerank = row[1][1]
    outlinks_size = len(outlinks)

    return_list = []

    if outlinks_size > 0:
        # If the node titlePage isn't a sinknode

        # Calculate the father's contribution
        pagerank_contr = pagerank/outlinks_size

        # Compose the list of outlinks with the father's contribution
        for outlink in outlinks:
            return_list.append([outlink, pagerank_contr])

    # It's needed to return the title page and 0 Page Rank otherwise the graph structure will be lost (the page not pointed will be lost)
    return_list.append([title_page, 0])

    return return_list


def pr_calculator(sumPR, alpha, total_node):

    final_pr = ((alpha/total_node)+((1-alpha)*sumPR))
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

    # Map trasformation to parse the input rows in (titlePage, listOutlinks)
    rows = input_data.map(lambda row: line_parser(row)).cache()

    # Values trasformation to insert initial page rank to rows (titlePage, initialPR)
    pagerank = rows.mapValues(lambda rank: 1 / total_node)

    # Iterations of page rank stages, the first transformation is a join since in the output i want the dangling nodes
    for i in range(iteration):

        # Inner join between rows and page rank, obtaining (titlePage, [listOutlinks, initialPR])
        parse_output = rows.join(pagerank)

        # Calculate the page rank contribution for all the outlinks given a title page
        pagerank_contribution = parse_output.flatMap(lambda row: rank_calculator(row))

        # Sum the page rank by key (title page)
        total_PR = pagerank_contribution.reduceByKey(add)

        # Calculate pagerank
        pagerank = total_PR.mapValues(lambda sumPR: pr_calculator(sumPR, alpha, total_node))

    # Sort in descending order
    rank_output = pagerank.sortBy(lambda row: row[1], False)

    rank_output.saveAsTextFile(output_path)
