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

from mods.func_prompt_io import check_exist, check_overwrite



# =============== main =============== #
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description = "gro_resetter.py - reset residue and atom index for gro file", formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-i", dest = "input_file", metavar = "INPUT.gro", required = True, help = "input file")
	parser.add_argument("-o", dest = "output_file", metavar = "OUTPUT.gro", required = True, help = "output file")
	parser.add_argument("-O", dest = "flag_overwrite", action = "store_true", default = False, help = "overwrite forcibly")
	args = parser.parse_args()

	check_exist(args.input_file, 2)

	temp_file = ""
	cnt_atom = 0
	num_atom = 0
	with tempfile.NamedTemporaryFile(mode = "w", delete = False) as obj_output:
		temp_file = obj_output.name
		res_idx = 0
		old_res = ""
		atom_idx = 0
		with open(args.input_file, "r") as obj_input:
			for line_idx, line_val in enumerate(obj_input, 1):
				if line_idx == 1:
					# title
					obj_output.write(line_val)
					continue

				if line_idx == 2:
					# number of atoms
					num_atom = int(line_val.strip())
					obj_output.write(line_val)
					continue

				values = line_val.strip().split()
				if (len(values) == 3 or len(values) == 6) and len(values) == len([True for v in values if "." in v]):
					# Last line (box size)
					obj_output.write(line_val)
					continue

				cnt_atom += 1
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

	if cnt_atom != num_atom:
		sys.stderr.write("WARNING: The number of atoms ({0}) in the file does not match the actual number of atoms ({1}). \nIt is rewritten by the actual number of atoms.\n".format(num_atom, cnt_atom))
		temp_input = temp_file
		temp_file = temp_file + "_rewrite"
		with open(temp_file, "w") as obj_output:
			with open(temp_input, "r") as obj_input:
				for line_idx, line_val in enumerate(obj_input, 1):
					if line_idx == 2:
						obj_output.write("{0:>5}\n".format(cnt_atom))
						continue
					obj_output.write(line_val)
			os.remove(temp_input)

	if args.flag_overwrite == False:
		check_overwrite(args.output_file)

	shutil.move(temp_file, args.output_file)
