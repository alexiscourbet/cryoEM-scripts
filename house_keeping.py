#!/usr/bin/env python

# Usage:
# python house_keeping.py -p path -f file_you_want_to_keep1.mrc file_you_want_to_keep2.mrc file_you_want_to_keepn.mrc

import argparse
import os

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True,
	help="path to input refinement directory")
ap.add_argument("-f", "--file", required=True, nargs='+',
	help="Names of the good file(s) that you want to keep separated by spaces (will delete all the others)")
args = vars(ap.parse_args())

def main():
	get_the_bad_files(args["file"],args["path"])

def get_the_bad_files(file, rootdir):
	for root, dirs, files in os.walk(rootdir):
		for f in files:
			print("Checking file name..." + str(f)) 
			if f not in file:
				fullname = os.path.join(root, f)
				try:
					if os.path.getsize(fullname) == 0:
						print("Bad, bad file...!" + str(fullname)) 
						os.remove(fullname)
				except Exception as e:
					print(e)
					print ("Couldn't find that bad file...")   

main()
print ('Done!') 