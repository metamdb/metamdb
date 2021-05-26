import re
import json


class AtomMapping():
    def __init__(self, identifier, file, imgPath):
        self.identifier = identifier
        self.file = file
        self.imgPath = imgPath

    def generateAtomMappingForElement(self, element):
        rxn = self.file.splitlines()

        molFiles = self.__getMolFilesFromFile(rxn)

        return self.__getAtomMappingFromMolFilesForElement(molFiles, element)

    def __getMolFilesFromFile(self, file):
        countRow = file[4]
        eductLength = int(countRow[:3].strip())

        molStartIndex = self.__getIndexForKeywordsInFile(file, '$MOL')
        molEndIndex = self.__getIndexForKeywordsInFile(file, 'M  END')

        return [{
            'molFile': file[startIndex:endIndex],
            'reactant': 'EDUCT' if index < eductLength else 'PRODUCT'
        } for index, (startIndex,
                      endIndex) in enumerate(zip(molStartIndex, molEndIndex))]

    def __getIndexForKeywordsInFile(self, file, keyword):
        return [
            index for index, row in enumerate(file) if row.strip() == keyword
        ]

    def __getAtomMappingFromMolFilesForElement(self, molFiles, element):
        atomMappingRegex = re.compile(r'^.{31}([A-Z]..).{26}(..\d)')

        atomMap = []
        for molFile in molFiles:
            name = molFile['molFile'][1]
            try:
                name = json.loads(name)
            
            #TODO: Error message
            except json.decoder.JSONDecodeError as error_message:
                print(error_message)
            reactant = molFile['reactant']

            atomNumbering, indices = [], []
            for index, row in enumerate(molFile['molFile'][5:]):
                atomMappingHit = atomMappingRegex.search(row)

                if atomMappingHit:
                    atomElement, atomNumber = atomMappingHit.groups()
                    if atomElement.strip() == element:
                        atomNumbering.append(int(atomNumber))
                        indices.append(index + 1)

            atomMap.append({
                'name': name,
                'reactant': reactant,
                'atomNumbering': atomNumbering,
                'indices': indices
            })

        return atomMap
