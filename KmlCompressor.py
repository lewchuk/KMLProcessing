#! /usr/bin/python

import optparse
import os
import shutil

from PythonKML import PythonKML as pykml

usage = "usage: %prog [options] source"

parser = optparse.OptionParser(usage=usage)
parser.add_option("-d", "--destination", dest="destination", help="output file for compression, defaults to <source>.cmp.kml")
parser.add_option("-n", "--number", dest="number", type="int", default="950", help="number of datapoints to compress to")
parser.add_option("-a", "--angle", dest="angle", type="float", default=30, help="maximum angle in degrees for a datapoint to be removed")
parser.add_option("-f", "--force", dest="force", action="store_true", help="overwrite existing destination files")

def extractLineStrings(geometries):
    count = 0
    tocompress = []

    for geo in geometries:
        if type(geo) == pykml.Point:
            count += 1
        elif type(geo) == pykml.LineString:
            tocompress.append(geo)
        elif type(geo) == pykml.LinearRing:
            count += len(geo.Coordinates)
        elif type(geo) == pykml.MultiGeometry:
            (c2, comp2) = extractLineStrings(geo._geoms)
            count += c2
            tocompress.extend(comp2)
        else:
            print "Did not recognize geometry type"

    return (count, tocompress)

def compressCoordinates(coords, limit, angle):
    pass

def compress(dest, limit, angle):
    kml = pykml.kml(dest)

    geometries = [pm.getGeometry() for pm in kml.getPlacemarks()]

    (count, tocompress) = extractLineStrings(geometries)
    
    limit -= count

    existing = [len(x.Coordinates) for x in tocompress]

    total = sum(existing)

    counts = [x/total*limit for x in existing]
    
    for aCount, geo in zip(counts, tocompress):
        compressCoordinates(geo.Coordinates, aCount, angle)
        
    kml.write()

if __name__ == "__main__":
    (options, args) = parser.parse_args();

    if len(args) != 1:
        parser.print_help()
        exit()

    source = args[0]
    if not os.path.exists(source):
        print "Source: %s does not exist" % source
        exit()

    dest = options.destination

    if dest is None:
        dest = "%s.cmp.kml" % source

    limit = options.number
    angle = options.angle

    if os.path.exists(dest):
        if options.force:
            os.remove(dest)
        else:
            print "Destination: %s already exists" % dest
            exit()

    shutil.copy(source, dest)

    compress(dest, limit, angle)

