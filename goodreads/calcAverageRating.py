from __future__ import division
import json
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import operator
import collections
import numpy as np

class AverageCalculator(object):
    def __init__(self, address):
        with open(address, 'r') as myFile:
            data = myFile.read()
            self.editionsData = json.loads(data)
            self.calculatedAvgs = {}
            self.finalAvgs = {}

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
                self.finalAvgs[language] = average
                print(language + ' : ' + str(average)) 
    
    def plot_bar_x(self, bookName):
        # this is for plotting purpose
        sorted_x = sorted(self.finalAvgs.items(), key = operator.itemgetter(1))
        self.finalAvgs = collections.OrderedDict(sorted_x)
        plt.xlabel('Edition Language', fontsize=10)
        plt.ylabel('Average Rating', fontsize=10)
        plt.title('Average rating vs Language for ' + bookName)
        plt.bar(range(len(self.finalAvgs)), self.finalAvgs.values(), align='center', width=0.5)  
        plt.xticks(range(len(self.finalAvgs)), self.finalAvgs.keys(), fontsize = 8, rotation='vertical') 
        plt.show()

def main():
    ac = AverageCalculator('editionsData.json')
    ac.calcAverage()
    ac.plot_bar_x('Kafka on the Shore')


if __name__ == "__main__":
    main()
