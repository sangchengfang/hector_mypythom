#!/usr/bin/env python3
# 
# Convert the time series files at the Nevada Geodetic Laboratory site into
# my mom-file format. The sol-files are stored in the ./ori_files directory. 
# The mom-files will be stored in the ./raw_files directory.
#
# NOTE:
# -----
# 1) Daily solutions are assumed. If not, update sampling period.
# 2) The East, North and Up displacements are counted relative to the first
#    observation which is set to zero.
#
# Machiel Bos, 2/9/2018, Santa Clara
#
#  This script is part of Hector 1.9
# ===============================================================================

import sys
import os
import glob
import re

# ===============================================================================
# Main program
# ===============================================================================

# --- Read all filenames in ./ori_files
fnames = glob.glob("./ori_files/*.tenv3")
# print(fnames)
fnames.sort()

# --- Did we find some sol-files?
if len(fnames)==0:
    print("Did not found any tenv3-files in the ./ori_files directory")
    sys.exit()

# --- Does the raw_files exists?
if not os.path.exists('./raw_files'):
    os.mkdir('./raw_files')

# --- Save file pointers in array
# fp_out = [None]*3
fp_out = list()
# print(fp_out)

# --- Convert each tenv3 file
for fname in fnames:

    # --- Extract station name
    m = re.search('/(\w+)\.', fname)
    # print(m)
    if m:
        station = m.group(1)
        # print(station)
    else:
        print("Cannot figure out filename of: {0}".format(fname))
        sys.exit()

    # --- Open a mom file for each component
    for comp in range(0, 3):
        # fp_out[comp] = open('./raw_files/{0:s}_{1:d}.mom'.format(station, comp), 'w')
        comp = open('./raw_files/{0:s}_{1:d}.mom'.format(station, comp), 'w')
        fp_out.append(comp)
    for item in fp_out:
        item.write('# sampling period 1.0\n')

    # --- Parse file
    first_value = True
    with open(fname, 'r') as fp_in:
        for line in fp_in:
            if not line.startswith('site'):
                cols = line.split()
                mjd = cols[3]
                e = float(cols[8])*1000.0
                n = float(cols[10])*1000.0
                u = float(cols[12])*1000.0

                if first_value:
                    first_value = False
                    e0 = e
                    n0 = n
                    u0 = u
                e -= e0
                n -= n0
                u -= u0

                fp_out[0].write('{0:s} {1:8.2f}\n'.format(mjd, e))
                fp_out[1].write('{0:s} {1:8.2f}\n'.format(mjd, n))
                fp_out[2].write('{0:s} {1:8.2f}\n'.format(mjd, u))

for item in fp_out:
    item.close()
