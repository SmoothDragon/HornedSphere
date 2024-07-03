#!/usr/bin/env python3

'''
Two "C" shaped tori can slide into each other. After rotating one, another
slide can be done to entangle them further.
'''

import numpy as np

from solid import *
from solid.utils import *


def parseArguments():
    # Argument parsing
    import argparse
    parser = argparse.ArgumentParser(
        description='Generate SCAD for Puzzle Torus.')
    parser.add_argument('-l', action='store', default='25', dest='length',
        type=float, help='Diameter (in millimeters) of torus arm.')
    parser.add_argument('--gap', action='store', default='.5', dest='gap',
        type=float, help='Tolerance gap between pieces.')  # gap=.1 tight
    parser.add_argument('-n', action='store', default='30', dest='fn',
        type=int, help='Curvature parameter. Number of sides on circle.')
    return parser.parse_args()


def angleTorus(
        sep:'Distance between bottom tori arms',
        segments:'Number of copies of "block" that are unioned to create a path',
        obj:'Something to put between the arms'=None,
        ):
    R = .75*sep
    r = R/8
    torus = rotate_extrude(convexity=10)(translate([R, 0])(circle(r)))
    cut = cube(2*R)
    cut = translate([0,0,-R])(cut)
    cut = rotate([0,0,-45])(cut)
    theta = np.arccos(np.sqrt(2)*4/3-1)*180/np.pi
    cut = intersection()(rotate([0,0,-45+theta])(cut),rotate([0,0,45-theta])(cut))
    block =  torus - cut
    block = translate([R,0,0])(block)
    # insert piece here
    if obj is not None:
        obj = rotate([0,0,90])(obj)
        obj = rotate([0,45,0])(obj)
        obj = translate([R+(np.sqrt(2)*4/3-1)*R,0,0])(obj)
        block += obj
    block = rotate([0,-45,0])(block)
    block = rotate([0,0,30])(block)
    block = translate([-2/3*R,0,0])(block)
    block += rotate([0,0,180])(block)
    return block


if __name__ == '__main__':
    args = parseArguments()
    size = args.length
    fn = args.fn
    gap = args.gap

    sep = 100
    R = .75*sep
    r = R/4
    final = angleTorus(sep=sep, segments=fn)
    mini = scale(2**-.5)(final)
    final = angleTorus(sep=sep, segments=fn, obj=mini)
    mini = scale(2**-.5)(final)
    final = angleTorus(sep=sep, segments=fn, obj=mini)
    mini = scale(2**-.5)(final)
    final = angleTorus(sep=sep, segments=fn, obj=mini)
    print(scad_render(final, file_header=f'$fn={args.fn};'))
