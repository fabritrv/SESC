import csv
import os
import sys

from solidity_parser import parser

sys.setrecursionlimit(1000000000)
__owd = os.getcwd()


def get_functions_and_variables(folder):
    directory = __owd + os.sep + "parser"
    if not os.path.isdir(directory):
        os.makedirs(directory)
    os.chdir(folder)
    filename = directory + os.sep + "functions_and_variables.csv"
    with open(filename, "a") as out_file:
        fieldnames = ["address", "functions", "variables"]
        w = csv.DictWriter(out_file, fieldnames)
        w.writeheader()
        for counter, f in enumerate(os.listdir(os.getcwd())):
            try:
                contract_dict = {"address": f, "functions": list(), "variables": list()}
                func_set = set()
                var_set = set()
                sys.stdout = open(os.devnull, "w")
                sourceUnit = parser.parse_file(
                    f
                )  # parse_file tends to print stuff that is not needed, this will avoid it from cluttering your shell too much
                sys.stdout = sys.__stdout__
                for c in sourceUnit["children"]:
                    if c["type"] == "ContractDefinition":
                        for s in c["subNodes"]:
                            try:
                                func_set.add(s["name"])
                            except:
                                if s["type"] == "UsingForDeclaration":
                                    continue
                                var_set.add(s["variables"][0]["name"])
                add_f = sorted(func_set, key=str.casefold)
                add_v = sorted(var_set, key=str.casefold)
                contract_dict["functions"] = add_f
                contract_dict["variables"] = add_v
                w.writerow(contract_dict)
            except (UnicodeDecodeError, TypeError, AttributeError):
                continue
    os.chdir(__owd)
    print(f"\nDone: {counter}")


def get_functions_and_variables_by_address(address, owd=__owd):
    directory = owd + os.sep + "parser"
    if not os.path.isdir(directory):
        os.makedirs(directory)
    filename = directory + os.sep + "functions_and_variables.csv"
    with open(filename, "r") as in_file:
        reader = csv.DictReader(in_file)
        for row in reader:
            if row["address"] == address:
                s = (
                    "Functions: "
                    + row["functions"]
                    + "\nVariables: "
                    + row["variables"]
                )
                print(s)
