#! /usr/bin/python

import copy
import math
import optparse
import os
import shutil

from xml.dom import minidom

usage = "usage: %prog [options] source"

parser = optparse.OptionParser(usage=usage)
parser.add_option("-d", "--destination", dest="destination", help="output file for compression, defaults to <source>.cmp.kml")
parser.add_option("-l", "--limit", dest="limit", type="int", default="1000", help="number of datapoints to compress to")
parser.add_option("-f", "--force", dest="force", action="store_true", help="overwrite existing destination files")

def extractCoordinates(geometryNode):
    coordinateNode = geometryNode.getElementsByTagName("coordinates")[0]
    coordStr = coordinateNode.firstChild.data
    data = [ map(float,x.split(',')) for x in coordStr.split() ]
    return data

def extractPoint(point):
    return (1, [])

def extractLineString(linestring):
    return (0, [linestring])

def extractLinearRing(ring):
    coordData = extractCoordinates(ring)
    return (len(coordData), [])

def determineBearing(p1, p2):
    """ Determines the bearing between p1 and p2 along the great
    circle which connects them.

    p1 -- Point 1 - (long, lat[ ,alt])
    p2 -- Point 2 - (long, lat[ ,alt])

    Source for mathematics: http://www.movable-type.co.uk/scripts/latlong.html
    """
    
    dlon = math.radians(p2[0] - p1[0])

    lat1 = math.radians(p1[1])
    lat2 = math.radians(p2[1])

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

    Parameters:
        p1 -- point 1 - (long, lat[ ,alt])
        p2 -- point 2 - (long, lat[ ,alt])
        p3 -- point 3 - (long, lat[ ,alt])

    Returns:
        angle -- The difference in degrees of the angles between the two
                 lines.  Angles are between 0 and 180 degrees.
    """

    bearing1 = determineBearing(p1,p2);
    bearing2 = determineBearing(p1,p3);

    angle = abs(bearing2 - bearing1)

    if angle > math.pi:
        angle = 2*math.pi - angle

    return math.degrees(angle)   

def constructAngles(coordinates):
    """ Using the algorithm in determineAngle() this function
    computes the list of angles corresponding to a list of coordinates.

    Parameters:
        coordinates -- A list of long,lat[,alt] tuples

    Returns:
        angles -- A list of n-2 angles between 0 and 180 degrees
    """

    angles = []
    for i in range(1,len(coordinates)-1):
        angle = determineAngle(coordinates[i-1],
                               coordinates[i],
                               coordinates[i+1])
        angles.append(angle)
    return sorted(angles)

class KMLPath:
    def __init__(self,geometry):
        self._geo = geometry
        self._coords = extractCoordinates(geometry)
        self._angles = None
    
    def __len__(self):
        return len(self._coords)

    def getAngles(self):
        if not self._angles:
            self._angles = constructAngles(self._coords)

        return copy.copy(self._angles)

    def filterIdentical(self):
        """ Filters the coordinates accociated with this geometry
        entry for identical lat/long coordinates.  It ignores altitude
        at the moment.

        Returns:
            difference -- The number of data points removed
        """
        newcoords = []
        
        for i in range(1,len(self._coords)):
            p1 = self._coord
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
        for angle in self.getAngles():
            bucket = int(angle/bucketSize) * bucketSize
            if bucket not in histogram:
                histogram[bucket] = 0
            histogram[bucket] = histogram[bucket] + 1

        return histogram

# Both Polygon and MultiGeometry are simply containers for these basic geometry
# types so will be ignored by the compression algorithm.
GEOMETRIES = { "Point":extractPoint,
               "LineString":extractLineString,
               "LinearRing":extractLinearRing }

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
    """ Extracts compressable KMLPath objects from the list of Placemark
    DOM elements.

    Parameters:
        placemarks -- A list of DOM Elements corresponding to <Placemark>
                      tags.

    Returns:
        count -- The size of the non-compressable elements
        kmlPaths -- The list of KMLPath objects corresponding to the
                    compressable paths.
    """
    count = 0
    kmlPaths = []

    for pm in placemarks:
        size, geos = extractGeometries(pm)
        count += size
        kmlPaths.extend(geos)

    return (count, kmlPaths)

def printHistogram(histogram):
    print "\n".join(["%s\t%s" % x for x in sorted(histogram.items())])

def compressGeometries(geometries, limit):
    print "Filtering identical lat/long points"

    identical = 0

    for geo in geometries:
        printHistogram(geo.angleProfile(5))

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

    limit = options.limit

    if os.path.exists(dest):
        if options.force:
            os.remove(dest)
        else:
            print "Destination: %s already exists" % dest
            exit()

    compress(source, dest, limit)

