from __future__ import division
import json

class AverageCalculator(object):
    def __init__(self, address):
        with open(address, 'r') as myFile:
            data = myFile.read()
            self.editionsData = json.loads(data)
            self.calculatedAvgs = {}

    def calcAverage(self):
        for edition in self.editionsData:
            language = edition['language']
            if (language == None):
                continue

            num_of_raters = int(edition['numOfRaters'])
            average = float(edition['averageRating'])

            if (language in self.calculatedAvgs):
                self.calculatedAvgs[language]['numOfRaters'] += num_of_raters
                self.calculatedAvgs[language]['weightedSum'] += average * num_of_raters
            else:
                self.calculatedAvgs[language] = {}
                self.calculatedAvgs[language]['numOfRaters'] = num_of_raters
                self.calculatedAvgs[language]['weightedSum'] = average * num_of_raters
        
        for language in self.calculatedAvgs:
            if(self.calculatedAvgs[language]['numOfRaters'] > 100):
                average = self.calculatedAvgs[language]['weightedSum'] / self.calculatedAvgs[language]['numOfRaters']
                print(language + ' : ' + str(average)) 
        


def main():
    ac = AverageCalculator('editionsData.json')
    ac.calcAverage()


if __name__ == "__main__":
    main()
