import argparse

# Make a script that takes two json files and merges them into one
# The first file is the base file, the second file is the file to merge into the base file
# The second file will overwrite any values in the base file
# The merged file will be saved as a new file
args = argparse.ArgumentParser()
args.add_argument("base_file")
args.add_argument("merge_file")
args.add_argument("output_file")
args = args.parse_args()

import json
from pprint import pprint
import os

# Read the base file
if not os.path.exists(args.base_file):
    print("Base file does not exist")
    exit()
if not os.path.exists(args.merge_file):
    print("Merge file does not exist")
    exit() 

print("Reading files...")
with open(args.base_file) as f:
    base = json.load(f)
# Read the merge file
with open(args.merge_file) as f:
    merge = json.load(f)
    
# Merge the material keys
print("")
print("Merging materials...")
mats = {} # (name, material)
base_mat = base["materials"]
for m in base_mat:
    mat_name = m["name"]
    mats[mat_name] = m
merge_mat = merge["materials"]
for m in merge_mat:
    mat_name = m["name"]
    if mat_name in mats:
        print("- Material {} is replaced".format(mat_name))
        mats[mat_name] = m # Replace
    else:
        print("- WARN: Material {} not found (added)".format(mat_name))
        mats[mat_name] = m

# Print all materials
print("")
print("Materials:")
for m in mats.keys():
    print("- {}".format(m))
    
base["materials"] = list(mats.values())

# Save the merged file
with open(args.output_file, "w") as f:
    json.dump(base, f, indent=4)