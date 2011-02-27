"""
Copyright (c) 2010 Brian J Cunningham

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import pdb

import xml.dom.minidom as xml
import os

def _createTxtElement(doc, tag, text):
    txtNode = doc.createTextNode(text)
    elem = doc.createElement(tag)
    elem.appendChild(txtNode)
    return elem

def _createElement(doc, tag):
    return doc.createElement(tag)



"enum classes"
class altitudeMode(object):
    def __init__(self):
        self._mode = "absolute"
        
    def _setMode(self,modeStr):
        if modeStr not in ["clampToGround","relativeToGround","absolute","relativeToSeaFloor","clampToSeaFloor"]:
            raise ValueError("Invalid altitude mode")
        if type(modeStr) == str:
            self._mode = modeStr
        else:
            self._mode = modeStr.actualMode
        
    def _getMode(self):
        return self._mode
    
    def _getClampToGround(self):
        return "clampToGround"

    def _getRelativeToGround(self):
        return "relativeToGround"

    def _getAbsolute(self):
        return "absolute"

    def _getRelativeToSeaFloor(self):
        return "relativeToSeaFloor"

    def _getClampToSeaFloor(self):
        return"clampToSeaFloor"
    
    actualMode = property(_getMode,_setMode)
    clampToGround = property(_getClampToGround)
    relativeToGround = property(_getRelativeToGround)
    absolute = property(_getAbsolute)
    relativeToSeaFloor = property(_getRelativeToSeaFloor)
    clampToSeaFloor = property(_getClampToSeaFloor)

    def toXmlNode(self,kml):
        return _createTxtElement(kml._doc,"altitudeMode",self._mode)

    def toStr(self,kml,pretty = False):
        theNode = self.toXmlNode(kml)
        if pretty == True:
            return theNode.toprettyxml("\t","\n","UTF-8")
        return theNode.toxml("UTF-8")
    
    def parseKMLNode(self, KMLNode):
        tag = None
        try:
            tag = KMLNode.tagName
        except:
            raise TypeError("KMLNode was not an KML(xml) node")
        if tag != "altitudeMode":
            raise TypeError("KMLNode was not a altitudeMode node")
        self._setMode(str(KMLNode.childNodes[0].data))
    
    
class extrude(object):
    def __init__(self):
        self._toExtrude = False

    def _getValue(self):
        return self._toExtrude
    
    def _setValue(self,val):
        if type(val) != bool:
            raise TypeError("Expecting True of False or an extrude instance")
        if type(val) == bool:
            self._toExtrude = val
        else:
            self._toExtrude = val.value
        
    value = property(_getValue,_setValue)

    def toXmlNode(self,kml):
        return _createTxtElement(kml._doc,"extrude",str(int(self._toExtrude)))

    def toStr(self,kml,pretty = False):
        theNode = self.toXmlNode(kml)
        if pretty == True:
            return theNode.toprettyxml("\t","\n","UTF-8")
        return theNode.toxml("UTF-8")
        
    def parseKMLNode(self, KMLNode):
        tag = None
        try:
            tag = KMLNode.tagName
        except:
            raise TypeError("KMLNode was not an KML(xml) node")
        if tag != "extrude":
            raise TypeError("KMLNode was not a extrude node")
        self._toExtrude = bool(KMLNode.childNodes[0].data)
        
class tessellate:
    def __init__(self):
        self._toTessellate = False

    def _getValue(self):
        return self._toTessellate
    
    def _setValue(self,val):
        if type(val) != bool :
            raise TypeError("Expexting True of False")
        if type(val) == bool:
            self._toTessellate = val
        else:
            self._toTessellate = val.value
        
    value = property(_getValue,_setValue)

    def toXmlNode(self,kml):
        return _createTxtElement(kml._doc,"tessellate",str(int(self._toTessellate)))

    def toStr(self,kml,pretty = False):
        theNode = self.toXmlNode(kml)
        if pretty == True:
            return theNode.toprettyxml("\t","\n","UTF-8")
        return theNode.toxml("UTF-8")

    def parseKMLNode(self, KMLNode):
        tag = None
        try:
            tag = KMLNode.tagName
        except:
            raise TypeError("KMLNode was not an KML(xml) node")
        if tag != "tessellate":
            raise TypeError("KMLNode was not a tessellate node")
        self._toTessellate = bool(KMLNode.childNodes[0].data)

    
"other classes"
class LinearRing(object):
    def __init__(self):
        self._extrude = extrude()
        self._altMode = altitudeMode()
        self._tesselate = tessellate()
        self.Coordinates = coordinates()
        
    def _setExtrude(self, value):
        if type(value) != bool and type(value) != extrude:
            raise TypeError("Expecting value to be True, False or an extrude class object")
        if type(value) == bool:
            self._extrude.value = value
        else:
            self._extrude.value = value.value
            
    def _getExtrudeVal(self):
        return self._extrude.value

    Extrude = property(_getExtrudeVal,_setExtrude)

    def _setAltitudeMode(self, value):
        if type(value) != str and type(value) != altitudeMode:
            raise TypeError("Expecting value to be a str object  or an altitudeMode class object")
        if type(value) == str:
            self._altMode.actualMode = value
        else:
            self._altMode.actualMode = value.actualMode
            
    def _getAltitudeMode(self):
        return self._altMode.actualMode

    AltitudeMode = property(_getAltitudeMode,_setAltitudeMode)

    def _setTessellate(self, value):
        if type(value) != bool and type(value) != tessellate:
            raise TypeError("Expecting value to be True, False or a tessellate class object")
        if type(value) == bool:
            self._tesselate.value = value
        else:
            self._tesselate.value = value.value
            
    def _getTessellate(self):
        return self._tesselate.value

    Tessellate = property(_getTessellate,_setTessellate)


    def toXmlNode(self,kml):
        doc = kml._doc
        lsNode = _createElement(doc,"LinearRing")
        
        if self._extrude.value != False:
            lsNode.appendChild(self._extrude.toXmlNode(kml))
            
        if self._tesselate.value != False:
            lsNode.appendChild(self._tesselate.toXmlNode(kml))
            
        lsNode.appendChild(self._altMode.toXmlNode(kml))
        if len(self.Coordinates) < 4:
            raise Exception("Not enough points to define a linear ring")
        if self.Coordinates[0] != self.Coordinates[len(self.Coordinates)-1]:
            raise Exception("Begining point is not equal to the end point")
        lsNode.appendChild(self.Coordinates.toXmlNode(kml))
        return lsNode
        
    def toStr(self,kml,pretty = False):
        node = self.toXmlNode()
        if pretty == True:
            return node.toprettyxml("\t","\n","UTF-8")
        return node.toxml("UTF-8")

    def parseKMLNode(self,KMLNode):
        tag = None
        self._coords = []
        try:
            tag = KMLNode.tagName
        except:
            raise TypeError("KMLNode was not an KML(xml) node")
        if tag != "LinearRing":
            raise TypeError("KMLNode was not a Point node")
        
        if KMLNode.getElementsByTagName("altitudeMode") != []:
            self._altMode.parseKMLNode(KMLNode.getElementsByTagName("altitudeMode")[0])

        if KMLNode.getElementsByTagName("extrude") != []:
            self._extrude.parseKMLNode(KMLNode.getElementsByTagName("extrude")[0])

        if KMLNode.getElementsByTagName("tessellate") != []:
            self._tessellate.parseKMLNode(KMLNode.getElementsByTagName("tessellate")[0])

        if KMLNode.getElementsByTagName("coordinates") != []:
            self.Coordinates.parseKMLNode(KMLNode.getElementsByTagName("coordinates")[0])
            

class LineString(object):
    def __init__(self):
        self._extrude = extrude()
        self._altMode = altitudeMode()
        self._tesselate = tessellate()
        self.Coordinates = coordinates()
        
    def _setExtrude(self, value):
        if type(value) != bool:
            raise TypeError("Expecting value to be True, False or an extrude class object")
        if type(value) == bool:
            self._extrude.value = value
        else:
            self._extrude.value = value.value
            
    def _getExtrudeVal(self):
        return self._extrude.value

    Extrude = property(_getExtrudeVal,_setExtrude)

    def _setAltitudeMode(self, value):
        if type(value) != str and type(value) != altitudeMode:
            raise TypeError("Expecting value to be a str object  or an altitudeMode class object")
        if type(value) == str:
            self._altMode.actualMode = value
        else:
            self._altMode.actualMode = value.value
            
    def _getAltitudeMode(self):
        return self._altMode.actualMode

    AltitudeMode = property(_getAltitudeMode,_setAltitudeMode)

    def _setTessellate(self, value):
        if type(value) != bool:
            raise TypeError("Expecting value to be True, False or a tessellate class object")
        if type(value) == bool:
            self._tesselate.value = value
        else:
            self._tesselate.value = value.value
            
    def _getTessellate(self):
        return self._tesselate.value

    Tessellate = property(_getTessellate,_setTessellate)


    def toXmlNode(self,kml):
        doc = kml._doc
        lsNode = _createElement(doc,"LineString")
        
        if self._extrude.value != False:
            lsNode.appendChild(self._extrude.toXmlNode(kml))
            
        if self._tesselate.value != False:
            lsNode.appendChild(self._tesselate.toXmlNode(kml))
            
        lsNode.appendChild(self._altMode.toXmlNode(kml))
        lsNode.appendChild(self.Coordinates.toXmlNode(kml))
        return lsNode
        
    def toStr(self,kml,pretty = False):
        node = self.toXmlNode()
        if pretty == True:
            return node.toprettyxml("\t","\n","UTF-8")
        return node.toxml("UTF-8")

    def parseKMLNode(self,KMLNode):
        tag = None
        self._coords = []
        try:
            tag = KMLNode.tagName
        except:
            raise TypeError("KMLNode was not an KML(xml) node")
        if tag != "LineString":
            raise TypeError("KMLNode was not a Point node")
        
        if KMLNode.getElementsByTagName("altitudeMode") != []:
            self._altMode.parseKMLNode(KMLNode.getElementsByTagName("altitudeMode")[0])

        if KMLNode.getElementsByTagName("extrude") != []:
            self._extrude.parseKMLNode(KMLNode.getElementsByTagName("extrude")[0])

        if KMLNode.getElementsByTagName("tessellate") != []:
            self._tessellate.parseKMLNode(KMLNode.getElementsByTagName("tessellate")[0])

        if KMLNode.getElementsByTagName("coordinates") != []:
            self.Coordinates.parseKMLNode(KMLNode.getElementsByTagName("coordinates")[0])
            
        
    
class Point(object):
    def __init__(self):
        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = 0.0
        self._extrude = extrude()
        self._altMode = altitudeMode()
        
    def _setExtrude(self, value):
        if type(value) != bool:
            raise TypeError("Expecting value to be True, False or an extrude class object")
        if type(value) == bool:
            self._extrude.value = value
        else:
            self._extrude.value = value.value
            
    def _getExtrudeVal(self):
        return self._extrude.value

    Extrude = property(_getExtrudeVal,_setExtrude)

    def _setAltitudeMode(self, value):
        if type(value) != str and type(value) != altitudeMode:
            raise TypeError("Expecting value to be a str object  or an altitudeMode class object")
        if type(value) == str:
            self._altMode.actualMode = value
        else:
            self._altMode.actualMode = value.value
            
    def _getAltitudeMode(self):
        return self._altMode.actualMode

    AltitudeMode = property(_getAltitudeMode,_setAltitudeMode)

    def toXmlNode(self,kml):
        doc = kml._doc
        ptNode = _createElement(doc,"Point")
        if self._extrude.value != False:
            ptNode.appendChild(self._extrude.toXmlNode(kml))
        ptNode.appendChild(self._altMode.toXmlNode(kml))
        coord = coordinates()
        coord.append([self.longitude,self.latitude, self.altitude])
        ptNode.appendChild(coord.toXmlNode(kml))
        return ptNode
        
    def toStr(self,kml,pretty = False):
        node = self.toXmlNode()
        if pretty == True:
            return node.toprettyxml("\t","\n","UTF-8")
        return node.toxml("UTF-8")

    def parseKMLNode(self,KMLNode):
        tag = None
        self._coords = []
        try:
            tag = KMLNode.tagName
        except:
            raise TypeError("KMLNode was not an KML(xml) node")
        if tag != "Point":
            raise TypeError("KMLNode was not a Point node")
        
        if KMLNode.getElementsByTagName("altitudeMode") != []:
            self._altMode.parseKMLNode(KMLNode.getElementsByTagName("altitudeMode")[0])

        if KMLNode.getElementsByTagName("extrude") != []:
            self._extrude.parseKMLNode(KMLNode.getElementsByTagName("extrude")[0])

        if KMLNode.getElementsByTagName("coordinates") != []:
            coords = coordinates()
            coords.parseKMLNode(KMLNode.getElementsByTagName("coordinates")[0])
            if len(coords) == 0:
                raise Exception("coordinate xml information not present")
            if len(coords) > 1:
                raise Exception("more than one coordinate")
            
            self.latitude = coords[0][0]
            self.longitude = coords[0][1]
            self.altitude = coords[0][2]
            

class LookAt(object):
    def __init__(self):
        self.latitude = 0.0
        self.longitude = 0.0
        self.altitude = 0.0
        self.heading = 0.0
        self.tilt = 0.0
        self.range = 0.0
        self._altMode = altitudeMode()
   
    def _setAltitudeMode(self, value):
        if type(value) != str and type(value) != altitudeMode:
            raise TypeError("Expecting value to be a str object  or an altitudeMode class object")
        if type(value) == str:
            self._altMode.actualMode = value
        else:
            self._altMode.actualMode = value.value
            
    def _getAltitudeMode(self):
        return self._altMode.actualMode

    AltitudeMode = property(_getAltitudeMode,_setAltitudeMode)

    def toXmlNode(self,kml):
        doc = kml._doc
        lookNode = _createElement(doc,"LookAt")
        lookNode.appendChild(_createTxtElement(kml._doc,"latitude",str(self.latitude)))
        lookNode.appendChild(_createTxtElement(kml._doc,"longitude",str(self.longitude)))
        lookNode.appendChild(_createTxtElement(kml._doc,"altitude",str(self.altitude)))
        lookNode.appendChild(_createTxtElement(kml._doc,"heading",str(self.heading)))
        lookNode.appendChild(_createTxtElement(kml._doc,"tilt",str(self.tilt)))
        lookNode.appendChild(_createTxtElement(kml._doc,"range",str(self.range)))
        lookNode.appendChild(self._altMode.toXmlNode(kml))
        return lookNode
        
    def toStr(self,kml,pretty = False):
        node = self.toXmlNode()
        if pretty == True:
            return node.toprettyxml("\t","\n","UTF-8")
        return node.toxml("UTF-8")

    def parseKMLNode(self,KMLNode):
        tag = None
        self._coords = []
        try:
            tag = KMLNode.tagName
        except:
            raise TypeError("KMLNode was not an KML(xml) node")
        if tag != "Point":
            raise TypeError("KMLNode was not a Point node")

        if KMLNode.getElementsByTagName("latitude") != []:
            self.latitude = float(KMLNode.getElementsByTagName("latitude")[0].childNodes[0].data)

        if KMLNode.getElementsByTagName("longitude") != []:
            self.longitude = float(KMLNode.getElementsByTagName("longitude")[0].childNodes[0].data)

        if KMLNode.getElementsByTagName("altitude") != []:
            self.altitude = float(KMLNode.getElementsByTagName("altitude")[0].childNodes[0].data)

        if KMLNode.getElementsByTagName("heading") != []:
            self.heading = float(KMLNode.getElementsByTagName("heading")[0].childNodes[0].data)

        if KMLNode.getElementsByTagName("tilt") != []:
            self.tilt = float(KMLNode.getElementsByTagName("tilt")[0].childNodes[0].data)

        if KMLNode.getElementsByTagName("range") != []:
            self.range = float(KMLNode.getElementsByTagName("range")[0].childNodes[0].data)
            
        if KMLNode.getElementsByTagName("altitudeMode") != []:
            self._altMode.parseKMLNode(KMLNode.getElementsByTagName("altitudeMode")[0])


        
class MultiGeometry(object):
    def __init__(self):
        self._geoms = []

    def __len__(self):
        return len(self._geoms)

    def __getitem__(self,index):
        if isinstance(index, slice):
            return self._geoms[index.start:index.stop:index.step]
        else:
            return self._geoms[index]

    def append(self,geometry):
        if not any(type(geometry) == aType for aType in [Point,LineString,LinearRing]):
            raise TypeError("Expecting geometry to be Point,LineString, or LinearRing")
        self._geoms.append(geometry)

    def remove(self,geomOrIndex):
        if any(type(geomOrIndex) == aType for aType in [Point,LineString,LinearRing]):
            self._geoms.remove(geomOrIndex)
            coord = list(coordOrIndex)
        if type(geomOrIndex) == int:
            if geomOrIndex >= len(self._geoms) or geomOrIndex < 0:
                raise ValueError("Index out of bounds")
            del self._geoms[geomOrIndex]

    def parseKMLNode(self, KMLNode):
        tag = None
        try:
            tag = KMLNode.tagName
        except:
            raise TypeError("KMLNode was not an KML(xml) node")
        if tag != "MultiGeometry":
            raise TypeError("KMLNode was not a MultiGeometry node")

        if KMLNode.getElementsByTagName("Point") != []:
            for pt in  KMLNode.getElementsByTagName("Point") != []:
                geom = Point()
                geom.parseKMLNode(pt)
                self.append(geom)
        elif KMLNode.getElementsByTagName("LineString") != []:
            for ls in KMLNode.getElementsByTagName("LineString"):
                geom = LineString()
                geom.parseKMLNode(ls)
                self.append(geom)
        elif KMLNode.getElementsByTagName("LinearRing") != []:
            for lr in KMLNode.getElementsByTagName("LinearRing"):
                geom = LineString()
                geom.parseKMLNode(lr)
                self.append(geom)
        
    def toXmlNode(self,kml):
        doc = kml._doc
        multiGeomNode = _createElement(doc,"MultiGeometry")
        for geom in self._geoms:
            multiGeomNode.appendChild(geom.toXmlNode(kml))
        
    def toStr(self,kml,pretty = False):
        node = self.toXmlNode(kml)
        if pretty == True:
            return node.toprettyxml("\t","\n","UTF-8")
        return coordNode.toxml("UTF-8")

class coordinates(object):
    def __init__(self):
        self._coords = []

    def __len__(self):
        return len(self._coords)
    
    def __getitem__(self, index):
        if isinstance(index, slice):
            return self._coords[index.start:index.stop:index.step]
        else:
            return self._coords[index]

    def append(self,coord):
        if type(coord) not in [list,tuple]:
            raise TypeError("Expecting list/tuple of length 3")
        if type(coord) in [list,tuple] and len(coord) != 3:
            raise Exception("list/tuple must have a length of 3")
        self._coords.append(list(coord))
            
    def remove(self,coordOrIndex):
        if type(coordOrIndex) == tuple:
            coord = list(coordOrIndex)
        if type(coordOrIndex) == list:\
           self._coords.remove(coordOrIndex)
        if type(coordOrIndex) == int:
            if coordOrIndex >= len(self._coords) or coordOrIndex < 0:
                raise ValueError("Index out of bounds")
            del self._coords[coordOrIndex]


    def parseKMLNode(self, KMLNode):
        tag = None
        self._coords = []
        try:
            tag = KMLNode.tagName
        except:
            raise TypeError("KMLNode was not an KML(xml) node")
        if tag != "coordinates":
            raise TypeError("KMLNode was not a coordinates node")
        coords = str(KMLNode.childNodes[0].data).strip().split(" ")
        for x in range(0,len(coords)):
            coords[x] = [float(num) for num in coords[x].split(",")]
            if len(coords[x]) == 2:
                coords[x].append(0)
            self._coords.append(coords[x])
    
    def toXmlNode(self,kml):
        doc = kml._doc
        coordStr = ""
        for coord in self._coords:
            coordStr = coordStr + str(coord[0]) + "," + str(coord[1]) + "," + str(coord[2])+ " "
        return _createTxtElement(doc,"coordinates",coordStr.strip())

    def toStr(self,kml,pretty = False):
        coordNode = self.toXmlNode(kml)
        if pretty == True:
            return coordNode.toprettyxml("\t","\n","UTF-8")
        return coordNode.toxml("UTF-8")
    
    
class Placemark(object):
    def __init__(self):
        self.name = ""
        self.description = "None"
        self._geometry = None
        self._view = None

    def setView(self, aView):
        """Currently only supports LookAt but eventually maybe a Camera class
        """
        if not any(type(aView) == aType for aType in [LookAt]):
            raise TypeError("Expecting aView to be LookAt or Camera(eventually)")
        self._view = aView

    def getView(self):
        return self._view

    def clearView(self):
        self._view = None
        
    def getGeometry(self):
        return self._geometry
    
    def setGeometry(self, theGeometry):
        if not any(type(theGeometry) == aType for aType in [Point,LineString,LinearRing,MultiGeometry]):
            raise TypeError("Expecting geometry to be Point,LineString,MultiGeometry, or LinearRing")
        self._geometry = theGeometry

    def clearGeometry(self):
        self._geometry = None
        
    
    
    def addToFolder(self, folderName):
        self.folder = str(folderName)
        
    def parseKMLNode(self, KMLNode):
        tag = None
        try:
            tag = KMLNode.tagName
        except:
            raise TypeError("KMLNode was not an KML(xml) node")
        if tag != "Placemark":
            raise TypeError("KMLNode was not a Placemark node")
        try:
            self.name = str(KMLNode.getElementsByTagName("name")[0].childNodes[0].data)
        except:
            self.name = "Unknown"
            
        try:
            self.description = str(KMLNode.getElementsByTagName("description")[0].childNodes[0].data)
        except:
            self.description = "None"
            
        self._parseGeometry(KMLNode)
        self._parseView(KMLNode)
        
        if KMLNode.parentNode.tagName == str("Folder") and \
           KMLNode.parentNode.getElementsByTagName("name") != []:
            self.folder = KML.parentNode.getElementsByTagName("name")[0].childNodes[0].data

    def _parseView(self,KMLNode):
        if KMLNode.getElementsByTagName("LookAt") != []:
            self._view = LookAt()
            self._view.parseKMLNode(KMLNode.getElementsByTagName("LookAt")[0])
            
    def _parseGeometry(self, KMLNode):
        if KMLNode.getElementsByTagName("Point") != []:
            self._geometry = Point()
            self._geometry.parseKMLNode(KMLNode.getElementsByTagName("Point")[0])
        elif KMLNode.getElementsByTagName("LineString") != []:
            self._geometry = LineString()
            self._geometry.parseKMLNode(KMLNode.getElementsByTagName("LineString")[0])
        elif KMLNode.getElementsByTagName("LinearRing") != []:
            self._geometry = LinearRing()
            self._geometry.parseKMLNode(KMLNode.getElementsByTagName("LinearRing")[0])
        elif KMLNode.getElementsByTagName("MultiGeometry") != []:
            self._geometry = MultiGeometry()
            self._geometry.parseKMLNode(KMLNode.getElementsByTagName("MultiGeometry")[0])
        
    def toXmlNode(self,kml):
        doc = kml._doc
        pmNode = _createElement(doc,"Placemark")
        pmNode.appendChild(_createTxtElement(doc,"name", self.name))
        pmNode.appendChild(_createTxtElement(doc,"description", self.description))
        if self._view != None:
            pmNode.appendChild(self._view.toXmlNode(kml))
        if self._geometry != None:
            pmNode.appendChild(self._geometry.toXmlNode(kml))
        return pmNode
        
    def toStr(self,kml,pretty = False):
        pmNode = self.toXmlNode(kml)
        if pretty == True:
            return pmNode.toprettyxml("\t","\n","UTF-8")
        return pmNode.toxml("UTF-8")
        
class kml(object):
    def __init__(self, kmlFile):
        self.filename = kmlFile
        if not os.path.exists(kmlFile):
            self._doc = xml.getDOMImplementation().createDocument(None,"kml", None)
        else:
            self._doc = xml.parse(kmlFile)
        self._doc.documentElement.attributes["xmlns"] = "http://earth.google.com/kml/2.2"
        self.placemarks = self.getPlacemarks()

    def write(self):
        for child in self._doc.documentElement.childNodes:
            self._doc.documentElement.removeChild(child)
        docNode = _createElement(self._doc,"Document")
        self._doc.documentElement.appendChild(docNode)
        docNode.appendChild(_createTxtElement(self._doc, "name", os.path.split(self.filename)[1]))
        folders = self._determineFolders()
        folders = self._addThingsToFolders(folders)
        for k,v in folders.iteritems():
            docNode.appendChild(v)
        handle = open(self.filename,"w")
        handle.write(self._doc.toxml("UTF-8"))
        handle.close()

    def _addThingsToFolders(self, folderInfo):
        if hasattr(self, "placemarks"):
            for placemark in self.placemarks:
                if type(placemark) != Placemark:
                    raise TypeError("Geometry wasn't a placemark")
                
                if hasattr(placemark, "folder"):
                    folderInfo[placemark.folder].appendChild(placemark.toXmlNode(self))
                else:
                    folderInfo["Default"].appendChild(placemark.toXmlNode(self))
        return folderInfo
        
    def _determineFolders(self):
        folders = ["Default"]
        "find all folders"
        if hasattr(self,"placemarks"):
            for placemark in self.placemarks:
                if hasattr(placemark, "folder"):
                    folders.append(placemark.folder)
        folders = list(set(folders))
        toReturn = {}
        "create all the folders"
        for x in range(0, len(folders)):
            folder = _createElement(self._doc, "Folder")
            folder.appendChild(_createTxtElement(self._doc,"name",str(folders[x])))
            toReturn[folders[x]] = folder
        return toReturn
                    
            

        
    def close(self):
        self._doc.unlink()
        del self._doc
        del self.placemarks
        
    
    def getPlacemarks(self):
        if hasattr(self,"placemarks"):
            return self.placemarks
        self.placemarks = self._doc.getElementsByTagName("Placemark")
        for x in range(0, len(self.placemarks)):
            temp = Placemark()
            temp.parseKMLNode(self.placemarks[x])
            self.placemarks[x] = temp

        return self.placemarks
    
