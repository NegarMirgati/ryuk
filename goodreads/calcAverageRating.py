from __future__ import division
import json
import matplotlib.pyplot as plt
import operator
import collections
import numpy as np

class AverageCalculator(object):
    def __init__(self, address):
        with open(address, 'r') as myFile:
            data = myFile.read()
            self.editionsData = json.loads(data)
            self.calculatedAvgs = collections.defaultdict(lambda : collections.defaultdict(dict))
            self.finalAvgs = collections.defaultdict(lambda : collections.defaultdict(dict))

    def calcAverage(self):
        for edition in self.editionsData:
            language = edition['language']
            orig_name = edition['original_name']
            if (language == None):
                continue

            num_of_raters = int(edition['numOfRaters'])
            average = float(edition['averageRating'])

            if (orig_name in self.calculatedAvgs and language in self.calculatedAvgs[orig_name]):
                self.calculatedAvgs[orig_name][language]['numOfRaters'] += num_of_raters
                self.calculatedAvgs[orig_name][language]['weightedSum'] += average * num_of_raters
            else:
                self.calculatedAvgs[orig_name][language]['numOfRaters'] = num_of_raters
                self.calculatedAvgs[orig_name][language]['weightedSum'] = average * num_of_raters
        
        
        for book in self.calculatedAvgs:
            for language in self.calculatedAvgs[book]:
                if(self.calculatedAvgs[book][language]['numOfRaters'] > 100):
                    average = self.calculatedAvgs[book][language]['weightedSum'] / self.calculatedAvgs[book][language]['numOfRaters']
                    self.finalAvgs[book][language]['average'] = average
                    self.finalAvgs[book][language]['num_of_ratings'] = self.calculatedAvgs[book][language]['numOfRaters']
                    print(book + ' in ' + language + ' : ' + str(average)) 
        
        with open('results.json', 'w') as json_file:
            json.dump(self.finalAvgs, json_file)
    
    def plot_bar_x(self, bookName):
        # this is for plotting purpose
        #fig, ax = plt.subplots()
        sorted_x = sorted(self.finalAvgs.items(), key = operator.itemgetter(1))
        self.finalAvgs = collections.OrderedDict(sorted_x)
        plt.xlabel('Edition Language', fontsize=10)
        plt.ylabel('Average Rating', fontsize=10)
        plt.title('Average rating vs Language for ' + bookName)
        plt.bar(range(len(self.finalAvgs)), self.finalAvgs.values(), align='center', width=0.5)  
        plt.xticks(range(len(self.finalAvgs)), self.finalAvgs.keys(), fontsize = 8, rotation='vertical') 
        #rects = ax.patches
        #labels = ["label%d" % i for i in xrange(len(rects))]
        #print(labels)

        #for rect, label in zip(rects, labels):
        #    height = rect.get_height()
        #    ax.text(rect.get_x() + rect.get_width() / 2, height + 5, label,
        #    ha='center', va='bottom')

        plt.show()

def main():
    ac = AverageCalculator('editionsData.json')
    ac.calcAverage()
    #ac.plot_bar_x('Nausea')


if __name__ == "__main__":
    main()
