"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # Load NEO data from the given CSV file.
    with open(neo_csv_path, "r") as f:
        reader = csv.DictReader(f)
        neos = []
        for n in reader:
            n["name"] = n["name"] or None
            n["diameter"] = float(n["diameter"]) if n["diameter"] else None
            n["pha"] = False if n["pha"] in ["", "N"] else True
            try:
                neo = NearEarthObject(
                    designation=n["pdes"],
                    name=n["name"],
                    diameter=n["diameter"],
                    hazardous=n["pha"],
                )
            except Exception as e:
                print(e)
            else:
                neos.append(neo)
    return neos


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # Load close approach data from the given JSON file.
    with open(cad_json_path, "r") as f:
        reader = json.load(f)
        reader = [dict(zip(reader["fields"], data)) for data in reader["data"]]
        approaches = []
        for line in reader:
            try:
                approach = CloseApproach(
                    designation=line["des"],
                    time=line["cd"],
                    distance=float(line["dist"]),
                    velocity=float(line["v_rel"]),
                )
            except Exception as e:
                print(e)
            else:
                approaches.append(approach) 
    return approaches
