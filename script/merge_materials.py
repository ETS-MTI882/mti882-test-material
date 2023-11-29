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

mat_added = []
mat_replaced = []
merge_mat = merge["materials"]
for m in merge_mat:
    mat_name = m["name"]
    if mat_name in mats:
        mat_replaced.append(mat_name)
        mats[mat_name] = m # Replace
    else:
        mat_added.append(mat_name)
        mats[mat_name] = m

# Print all materials
print("")
print("Materials:")
for m in mats.keys():
    print("- {}".format(m))
    
base["materials"] = list(mats.values())

if len(mat_replaced) > 0:
    print("")
    print("Replacing materials:")
    for m in mat_replaced:
        print("- {}".format(m))

if len(mat_added) > 0:
    print("")
    print("WARNING: Added materials:")
    print("These materials were not in the base file, but were in the merge file")
    for m in mat_added:
        print("- {}".format(m))

print("")
print("Save file...")
# Save the merged file
with open(args.output_file, "w") as f:
    json.dump(base, f, indent=4)