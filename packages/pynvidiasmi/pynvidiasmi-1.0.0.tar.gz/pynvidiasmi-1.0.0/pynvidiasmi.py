#!/usr/bin/env python3
"""
Very simple package to query nvidia-smi command and return object output.
"""

import io, json, csv, subprocess, argparse, time


class NvidiaSmiCsvDialect(csv.Dialect):
    delimiter = ","
    lineterminator = "\n"
    skipinitialspace = True
    strict = True
    quoting = csv.QUOTE_MINIMAL
    doublequote = True
    escapechar = None
    quotechar = '"'


def _convert_numbers(dct):
    """
    Converts string properties to numbers when they are composed only of digits.
    """
    newdct = {}
    for key, value in dct.items():
        if value.isdigit():
            value = int(value)
        newdct[key] = value
    return newdct

    
def query(fields: list):
    """
    Queries the nvidia-smi command (which must be installed in the system) with specified fields,
    parses the returned csv format and returns it as a list of dictionaries.
    """
    query_string = ",".join(fields)
    output = subprocess.run(
        ["nvidia-smi", "--query-gpu=" + query_string, "--format=csv,nounits,noheader"],
        capture_output=True,
        check=True,
    )
    csvfile = io.StringIO(output.stdout.decode())
    reader = csv.DictReader(csvfile, fieldnames=fields, dialect=NvidiaSmiCsvDialect)
    return list(map(_convert_numbers, reader))


def get_available_gpus(
        memory_threshold : int = 0,
        compute_threshold : int = 0,
        times : int = 1,
        sleep : float = 1.0):
    """
    Returns a list of indices of the GPUs which show memory and compute lower than the given threshold (in integer percentage).

    If 'times' > 1 queries the GPUs multiple times, waiting 'sleep' time between the queries, and returns the intersection of the set.
    Useful when GPU loads oscillate.
    """
    freegpus = None
    for i in range(times):
        if i > 0:
            time.sleep(sleep)
        results = query(["index", "utilization.gpu", "utilization.memory"])
        nowfree = [result["index"] for result in results
                   if (result["utilization.gpu"] <= compute_threshold
                       and result["utilization.memory"] <= memory_threshold)]
        if freegpus is None:
            freegpus = set(nowfree)
        freegpus.intersection(nowfree)
    return list(freegpus)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Invokes nvidia-smi and returns json formatted output for the queries fields.")
    parser.add_argument("--fields", type=str, nargs="+")
    args = parser.parse_args()
    result = query(fields=args.fields)
    print(json.dumps(result, indent=2))
