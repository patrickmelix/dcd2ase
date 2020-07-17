#!/usr/bin/env python3
# Convert/Read dcd files to ASE Atoms and write as xyz
#
#
# Requires: ase, os
#
#
#
# by: Patrick Melix, 2019


from ase import Atoms, io
from ase.io.cp2k import iread_cp2k_dcd
import os, argparse


def dcd2ase(dcdFile,refStructFile):
    ref = io.read(refStructFile)
    with open(dcdFile, 'rb') as f:
        idcd = iread_cp2k_dcd(f, indices=slice(0,None), ref_atoms=ref, aligned=True)
        for image in idcd:
            yield image





def _writeExtXYZ(traj, outFile='traj.xyz'):
    #write to xyz
    if isinstance(outFile, str):
        out = open(outFile, mode='w')
    else:
        out = outFile
    for frame in traj:
        frame.wrap()
        frame.write(out, format='xyz', append=True)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert XYZ and DCD input to ASE-extxyz trajectory')
    parser.add_argument('inxyz', type=str, help='input xyz file')
    parser.add_argument('indcd', type=str, help='input dcd file')
    parser.add_argument('output', type=argparse.FileType('w'), help='output file')
    args = parser.parse_args()
    _writeExtXYZ(dcd2ase(args.indcd,args.inxyz),args.output)
