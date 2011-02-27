#! /usr/bin/python

import optparse
import os
import shutil

from xml.dom import minidom

usage = "usage: %prog [options] source"

parser = optparse.OptionParser(usage=usage)
parser.add_option("-d", "--destination", dest="destination", help="output file for compression, defaults to <source>.cmp.kml")
parser.add_option("-n", "--number", dest="number", type="int", default="950", help="number of datapoints to compress to")
parser.add_option("-a", "--angle", dest="angle", type="float", default=30, help="maximum angle in degrees for a datapoint to be removed")
parser.add_option("-f", "--force", dest="force", action="store_true", help="overwrite existing destination files")

def extractCoordinates(geometryNode):
    coordinateNode = geometryNode.getElementsByTagName("coordinates")[0]
    coordStr = coordinateNode.firstChild.data
    return coordStr.split()

def extractPoint(point):
    return (1, [])

def extractLineString(linestring):
    return (0, [linestring])

def extractLinearRing(ring):
    coordData = extractCoordinates(ring)
    return (len(coordData), [])
    
# Both Polygon and MultiGeometry are simply containers for these basic geometry
# types so will be ignored by the compression algorithm.
GEOMETRIES = { "Point":extractPoint,
               "LineString":extractLineString,
               "LinearRing":extractLinearRing }

def extractGeometries(pm):
    count = 0
    tocompress = []

    for (geo,action) in GEOMETRIES.items():
        for aGeo in pm.getElementsByTagName(geo):
            size, geos = action(aGeo)
            count += size
            tocompress.extend(geos)

    return (count, tocompress)

def extractCompressable(placemarks):
    count = 0
    tocompress = []

    for pm in placemarks:
        size, geos = extractGeometries(pm)
        count += size
        tocompress.extend(geos)

    return (count, tocompress)

def compressGeometries(geometries, limit, angle):
    pass


def compress(source, dest, limit, angle):
    doc = minidom.parse(source)

    placemarks = doc.getElementsByTagName("Placemark")

    size, geometries = extractCompressable(placemarks)

    remainingDP = limit - size

    

    destfile = open(dest, 'w')

    doc.writexml(destfile)

#    geometries = [pm.getGeometry() for pm in kml.getPlacemarks()]

#    (count, tocompress) = extractLineStrings(geometries)
    
#    limit -= count

 #   existing = [len(x.Coordinates) for x in tocompress]

  #  total = sum(existing)

   # counts = [x/total*limit for x in existing]
    
#    for aCount, geo in zip(counts, tocompress):
#        compressCoordinates(geo.Coordinates, aCount, angle)
        
#    kml.write()

    

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

    compress(source, dest, limit, angle)

