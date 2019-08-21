import json
import csv


def write_to_csv(name, type, data, counter=1):
	with open(name, mode=type) as csv_file:
		fieldnames = ['S.No','numOfRaters', 'name', 'language', 'averageRating']
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
		writer.writeheader()
		for info in data:
			# print(info['numOfRaters'])
			writer.writerow({'S.No': counter, 'numOfRaters': info['numOfRaters'],
			                 'name': info['name'],
			                 'language': info['language'],
			                 'averageRating': info['averageRating']})
			counter = counter + 1
	return counter


index = 1
with open('editionsData.json') as json_file:
	data = json.load(json_file)
	index = write_to_csv('editionsData.csv', 'w', data, index)

with open('editionsData2.json') as json_file:
	data = json.load(json_file)
	write_to_csv('editionsData.csv', 'a', data, index)

with open('editionsDataCAP.json') as json_file:
	data = json.load(json_file)
	write_to_csv('editionsDataCAP.csv', 'w', data)

# print('Name: ' + p['name'])
# print('Website: ' + p['website'])
# print('From: ' + p['from'])
# print('')
