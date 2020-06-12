import csv
import json
import os
from operator import itemgetter

import edlib
import networkx


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
                            if weight <= 30:  # require at least 70% matching
                                uwgraph.add_edge(
                                    source_node,
                                    compare_node,
                                    weight=int(
                                        100 - weight
                                    ),  # the weight of the edge is bigger when the contracts are similar
                                )
                            """
                            if (
                                uwgraph.number_of_edges() > 69
                            ):  # show 60 results in the graph, limits the number of results if your machine isn't powerful enough and if you want to print the graph
                                break
                            """
                    break
        show_neighbors(uwgraph[address], address)
        to_json(uwgraph[address], address)
        print("\nA .json of the graph was created.")
    except FileNotFoundError:
        print("To create the graph you have to run the parser first!")


def show_neighbors(neighbors, address):
    to_print = list()
    for n in neighbors.items():
        if n[0] != address:
            to_print.append({"address": n[0], "weight": n[1]["weight"]})
    print("\nThe results seen in the graph:")
    for printable in sorted(to_print, key=itemgetter("weight"), reverse=True):
        print(f'{printable["address"]} - {printable["weight"]}% match')


def to_json(neighbors, address):
    possible_weights = [
        # {"name": 60, "children": list()}, depending on the lowest percentage of matching required
        {"name": 70, "children": list()},
        {"name": 80, "children": list()},
        {"name": 90, "children": list()},
        {"name": 100, "children": list()},
    ]
    layout = {"name": address, "children": possible_weights}
    for count, n in enumerate(
        sorted(neighbors.items(), key=lambda e: int(e[1]["weight"]), reverse=True)
    ):
        if n[0] != address:
            for sub_lay in layout["children"]:
                weight = int(n[1]["weight"])
                if sub_lay["name"] == weight:
                    to_add = {"name": n[0], "value": weight}
                    sub_lay["children"].append(to_add)
        if count >= 200:
            break
    folder = "localh" + os.sep + "dendrogram" + os.sep + "files"
    if not os.path.isdir(folder):
        os.makedirs(folder)
    filename = folder + os.sep + "graph.json"
    with open(filename, "w+") as fp:
        json.dump(layout, fp, indent=4)
