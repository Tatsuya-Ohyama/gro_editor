#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
gro_resetter - reset residue and atom index for gro file
"""

import sys, signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

import argparse
import tempfile
import os
import shutil

from basic_func import check_exist, check_overwrite, get_file_length


# =============== main =============== #
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = "gro_resetter.py - reset residue and atom index for gro file", formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-i", dest = "input_file", metavar = "INPUT.gro", required = True, help = "input file")
	parser.add_argument("-o", dest = "output_file", metavar = "OUTPUT.gro", required = True, help = "output file")
	parser.add_argument("-O", dest = "flag_overwrite", action = "store_true", default = False, help = "overwrite forcibly")
	args = parser.parse_args()

	check_exist(args.input_file, 2)

	temp_file = ""
	with tempfile.NamedTemporaryFile(mode = "w", delete = False) as obj_output:
		temp_file = obj_output.name
		line_max = get_file_length(args.input_file)
		res_idx = 0
		old_res = ""
		atom_idx = 0
		with open(args.input_file, "r") as obj_input:
			for line_idx, line_val in enumerate(obj_input):
				if line_idx <= 1 or line_idx + 1 == line_max:
					pass

				else:
					if old_res != line_val[0:5]:
						old_res = line_val[0:5]
						res_idx += 1
						if 5 < len(str(res_idx)):
							res_idx = 1
					atom_idx += 1
					if 5 < len(str(atom_idx)):
						atom_idx = 1
					line_val = "{0:>5}{1}{2:>5}{3}".format(res_idx, line_val[5:15], atom_idx, line_val[20:])

				obj_output.write(line_val)

	if args.flag_overwrite == False:
		check_overwrite(args.output_file)

	shutil.move(temp_file, args.output_file)
