#! /usr/bin/python

import math
import optparse
import os
import shutil

from xml.dom import minidom

usage = "usage: %prog [options] source"

parser = optparse.OptionParser(usage=usage)
parser.add_option("-d", "--destination", dest="destination", help="output file for compression, defaults to <source>.cmp.kml")
parser.add_option("-n", "--number", dest="number", type="int", default="950", help="number of datapoints to compress to")
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

class KMLPath:
    def __init__(self,geometry):
        self._geo = geometry
        self._coords = extractCoordinates(geometry)
    
    def __len__(self):
        return len(self._coords)

    def filterIdentical(self):
        """ Filters the coordinates accociated with this geometry
        entry for identical lat/long coordinates.  It ignores altitude
        at the moment.

        Returns:
            difference -- The number of data points removed
        """
        newcoords = []
        
        for i in range(1,len(self._coords)):
            p1 = coordinates[i-1].split(',')
            p2 = coordinates[i].split(',')
            if p1[0] != p2[0] or p1[1] != p2[1]:
                filtered.append(coordinates[i])

        difference = len(self._coords) - len(newcoords)
        self._coords = newcoords

        return difference
  
    def angleProfile(self, bucketSize):
        """ Generates a histogram of angles in the coordinates.
        For every point [1,n-1] determines the difference of the angle
        between it and the previous point and between the previous point
        and the following point.

        Parameters:
            bucketSize -- The size of bucket to use for the histogram
                          buckets are [0,bucketSize), [bucketSize,bucketSize*2)...

        Returns:
            histogram -- A dictionary of bucket to frequency.
        """
    
        histogram = {}
        for i in range(1,len(self._coords) -1):
            angle = determineAngle(self._coords[i-1],
                                   self._coords[i],
                                   self._coords[i+1])

            bucket = int(angle/bucketSize) * bucketSize
            if bucket not in histogram:
                histogram[bucket] = 0
            histogram[bucket] = histogram[bucket] + 1

        return histogram


def extractGeometries(pm):
    """ Extracts from a <Placemark> any compressable geometries
    and the size of any non-compressable geometries

    Parameters:
        pm -- A DOM Element preresenting a Placemark

    Returns:
        count -- Number of datapoints for all non-compressable geometries
        kmlPaths -- A list of KMLPath objects which can be compressed
    """

    count = 0
    tocompress = []

    for (geo,action) in GEOMETRIES.items():
        for aGeo in pm.getElementsByTagName(geo):
            size, geos = action(aGeo)
            count += size
            tocompress.extend(geos)

    kmlPaths = [KMLPath(x) for x in tocompress]
    return (count, kmlPaths)

def extractCompressable(placemarks):
    count = 0
    tocompress = []

    for pm in placemarks:
        size, geos = extractGeometries(pm)
        count += size
        tocompress.extend(geos)

    return (count, tocompress)

def determineBearing(p1, p2):
    """ Determines the bearing between p1 and p2 along the great
    circle which connects them.

    p1 -- Point 1 - "long,lat[,alt]"
    p2 -- Point 2 - "long,lat[,alt]"

    Source for mathematics: http://www.movable-type.co.uk/scripts/latlong.html
    """
    
    point1 = p1.split(',')
    point2 = p2.split(',')
    
    dlon = math.radians(float(point2[0]) - float(point1[0]))

    lat1 = math.radians(float(point1[1]))
    lat2 = math.radians(float(point2[1]))

    y = math.sin(dlon) * math.cos(lat2) 
    x = (math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) *
         math.cos(dlon))
    bearing = math.atan2(y, x)

    if bearing < 0:
        bearing += 2*math.pi

    return bearing

def determineAngle(p1, p2, p3):
    """ This function used three strings of "lat,long[,alt]" to determine
    the angle between the line p1p2 and p1p3.  The angle is based on the
    initial bearings along the great circles connecting p1 and p2 and
    p1 and p3. Because the angle is based on the difference of two angles
    the absolute value is returned.

    Source for mathematics: http://www.movable-type.co.uk/scripts/latlong.html

    p1 -- point 1 - "long,lat[,alt]"
    p2 -- point 2 - "long,lat[,alt]"
    p3 -- point 3 - "long,lat[,alt]"
    """

    bearing1 = determineBearing(p1,p2);
    bearing2 = determineBearing(p1,p3);

    angle = bearing2 - bearing1

    return math.degrees(abs(angle))

def compressGeometries(geometries, limit):
    print "Filtering identical lat/long points"

    identical = 0

    for geo in geometries:
        print "\n".join(["%s\t%s" % x for x in sorted(geo.angleProfile(5).items())])

def compress(source, dest, limit):
    doc = minidom.parse(source)

    placemarks = doc.getElementsByTagName("Placemark")

    size, geometries = extractCompressable(placemarks)

    remainingDP = limit - size

    compressGeometries(geometries, remainingDP) 

    destfile = open(dest, 'w')

    doc.writexml(destfile)

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

    if os.path.exists(dest):
        if options.force:
            os.remove(dest)
        else:
            print "Destination: %s already exists" % dest
            exit()

    compress(source, dest, limit)

