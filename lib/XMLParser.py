from xml.etree import ElementTree

class XMLParser:
    def __init__(self, configFileName):
        self.configFileName = configFileName
        self.tree = ElementTree.parse(self.configFileName)
        self.root = self.tree.getroot()

    def FirstLevelParser(self, firstLvlTag):
        for firstLvlchild in self.root:
            if firstLvlchild.tag == firstLvlTag:
                return firstLvlchild.text

    def SecondLevelParser(self, firstLvlTag, attribKey, attribValue, secondLvlTag):
        for firstLvlchild in self.root:
            if firstLvlchild.tag == firstLvlTag and firstLvlchild.attrib[attribKey] == attribValue:
                for secondLvlchild in firstLvlchild:
                    if secondLvlchild.tag == secondLvlTag:
                        return secondLvlchild.text
                    
    def ThirdLevelParser(self, firstLvlTag, firstLvlAttribKey, firstLvlAttribValue,
                         secondLvlTag, secondLvlAttribKey, secondLvlAttribValue, thirdLvlTag):
        for firstLvlchild in self.root:
            if firstLvlchild.tag == firstLvlTag and firstLvlchild.attrib[firstLvlAttribKey] == firstLvlAttribValue:
                for secondLvlchild in firstLvlchild:
                    if secondLvlchild.tag == secondLvlTag and secondLvlchild.attrib[secondLvlAttribKey] == secondLvlAttribValue:
                        for thirdLvlChild in secondLvlchild:
                            if thirdLvlChild.tag == thirdLvlTag:
                                return thirdLvlChild.text