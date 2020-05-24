import csv
import os
import sys

from solidity_parser import parser

sys.setrecursionlimit(10000000)
__owd = os.getcwd()


def get_functions_and_variables(folder):
    skipped = 0
    done = 0
    directory = __owd + os.sep + "parser"
    if not os.path.isdir(directory):
        os.makedirs(directory)
    os.chdir(folder)
    filename = directory + os.sep + "functions_and_variables.csv"
    with open(filename, "a") as out_file:
        fieldnames = ["address", "functions", "variables"]
        w = csv.DictWriter(out_file, fieldnames)
        w.writeheader()
        for f in os.listdir(os.getcwd()):
            try:
                contract_dict = {"address": f, "functions": set(), "variables": set()}
                sys.stdout = open(os.devnull, "w")
                sourceUnit = parser.parse_file(
                    f
                )  # parse_file tends to print stuff that is not needed, this will avoid it from cluttering your shell too much
                sys.stdout = sys.__stdout__
                for c in sourceUnit["children"]:
                    if c["type"] == "ContractDefinition":
                        for s in c["subNodes"]:
                            try:
                                contract_dict["functions"].add(s["name"])
                                done += 1
                            except:
                                if s["type"] == "UsingForDeclaration":
                                    continue
                                contract_dict["variables"].add(
                                    s["variables"][0]["name"]
                                )
                                done += 1
                w.writerow(contract_dict)
            except (UnicodeDecodeError, TypeError, AttributeError):
                skipped += 1
    os.chdir(__owd)
    print(f"\nDone: {done}\nSkipped: {skipped}")


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
