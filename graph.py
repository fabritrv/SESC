import csv
import os
from operator import itemgetter

import edlib
import networkx
import matplotlib.pyplot as plt


def create(address):
    filename = os.getcwd() + os.sep + "parser" + os.sep + "functions_and_variables.csv"
    uwgraph = networkx.Graph()
    try:
        with open(filename, "r") as source_file:
            source_reader = csv.DictReader(source_file)
            for source_row in source_reader:
                source_node = source_row["address"]
                if source_node == address:
                    source_funcs = source_row["functions"].translate(
                        str.maketrans({"{": "", "}": "", "'": "", ",": ""})
                    )
                    source_vars = source_row["variables"].translate(
                        str.maketrans({"{": "", "}": "", "'": "", ",": ""})
                    )
                    with open(filename, "r") as compare_file:
                        compare_reader = csv.DictReader(compare_file)
                        for compare_row in compare_reader:
                            compare_funcs = compare_row["functions"].translate(
                                str.maketrans({"{": "", "}": "", "'": "", ",": ""})
                            )
                            compare_vars = compare_row["variables"].translate(
                                str.maketrans({"{": "", "}": "", "'": "", ",": ""})
                            )
                            align_funcs = edlib.align(source_funcs, compare_funcs)[
                                "editDistance"
                            ]  # levenshtein applied to the functions
                            align_vars = edlib.align(source_vars, compare_vars)[
                                "editDistance"
                            ]  # levenshtein applied to the variables
                            align = align_funcs + align_vars
                            S_LEN = len(source_funcs + source_vars)
                            similarity_coeff = (
                                align * 100 / S_LEN
                            )  # (number of char that must be changed to make the strings match)/(length of the string for source contract), should be a number comparable to a percentage
                            weight = round(
                                int(round(similarity_coeff, 0)), -1
                            )  # round it to multiples of 10
                            compare_node = compare_row["address"]
                            if weight < 40:  # require at least 60% matching
                                uwgraph.add_edge(
                                    source_node,
                                    compare_node,
                                    weight=int(
                                        100 - weight
                                    ),  # the weight of the edge is bigger when the contracts are similar
                                )
                            if (
                                uwgraph.number_of_edges() > 59
                            ):  # show 60 results in the graph
                                break
                    break
        print_graph(uwgraph)
        show_neighbors(uwgraph[address], address)
    except FileNotFoundError:
        print("To create the graph you have to run the parser first!")


def print_graph(graph):
    elarge = [(u, v) for (u, v, d) in graph.edges(data=True) if d["weight"] > 70]
    esmall = [(u, v) for (u, v, d) in graph.edges(data=True) if d["weight"] <= 70]
    pos = networkx.spring_layout(graph)
    # nodes
    networkx.draw_networkx_nodes(graph, pos, node_size=150)
    # edges
    networkx.draw_networkx_edges(graph, pos, edgelist=elarge, width=3)
    networkx.draw_networkx_edges(
        graph, pos, edgelist=esmall, width=3, alpha=0.5, edge_color="b", style="dashed"
    )
    # labels
    networkx.draw_networkx_labels(
        graph, pos, font_size=5, font_family="sans-serif", alpha=0.5, font_weight="bold"
    )
    plt.axis("off")
    plt.show()


def show_neighbors(neighbors, address):
    to_print = list()
    for n in neighbors.items():
        if n[0] != address:
            to_print.append({"address": n[0], "weight": n[1]["weight"]})
    print("\nThe results seen in the graph:")
    for printable in sorted(to_print, key=itemgetter("weight"), reverse=True):
        print(f'{printable["address"]} - {printable["weight"]}% match')
