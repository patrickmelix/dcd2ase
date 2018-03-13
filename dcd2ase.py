#!/usr/bin/env python2
# Convert/Read dcd files to ASE Atoms
#
#
# Requires: pwtools, ase, os
#
# pwtools from https://github.com/elcorto/pwtools
# WARNING: pip install pwtools installs something different!!
#
#
# by: Patrick Melix, 2018


from pwtools import dcd
from ase import Atoms
from ase import io as aseIO
import os, argparse


def _combine2Atoms(cellsIn, coordsIn, elements):
    #make that cell angles and lengths are complete
    lenSet = set([ len(x) for x in cellsIn ])
    assert len(lenSet) == 1
    assert 6 in lenSet
    #compare number of cells and coords
    assert len(cellsIn) == len(coordsIn)
    #compare nAtoms
    lenSet = set([ len(x) for x in coordsIn ])
    assert len(lenSet) == 1
    assert len(elements) in lenSet

    #convert
    traj = []
    for i, coordsI in enumerate(coordsIn):
        traj.append(Atoms(elements, coordsI))
        traj[-1].set_cell(cellsIn[i])
    return traj




def dcd2ase(dcdFile,refStructFile):
    cellsIn, coordsIn = dcd.read_dcd_data(dcdFile)
    refStruct = aseIO.read(refStructFile)

    #make sure number of atoms is the same for all structures
    lenSet = set([ len(x) for x in coordsIn ])
    assert len(lenSet) == 1
    assert len(refStruct) in lenSet

    #list of element symbols from reference
    elements = refStruct.get_chemical_symbols()
    assert len(elements) == len(refStruct)

    return _combine2Atoms(cellsIn, coordsIn, elements)




def _writeExtXYZ(traj, outFile='traj.xyz'):
    #write to xyz
    if isinstance(outFile,basestring):
        out = open(outFile, mode='w')
    else:
        out = outFile
    if len(traj) == 1:
        return
    for frame in traj:
        frame.write(out, format='xyz', append=True)
    return



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert XYZ and DCD input to ASE-extxyz trajectory')
    parser.add_argument('inxyz', type=str, help='input xyz file')
    parser.add_argument('indcd', type=str, help='input dcd file')
    parser.add_argument('output', type=argparse.FileType('w'), help='output file')
    args = parser.parse_args()
    traj = dcd2ase(args.indcd,args.inxyz)
    _writeExtXYZ(traj,args.output)
