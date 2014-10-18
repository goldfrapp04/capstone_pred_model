import csv
import sys

def count_for_chf():
	with open('/Users/Shia/Documents/Capstone/FeatExtraction/data/brfss/extracted.csv', 'rb') as csv_file:
		reader = csv.DictReader(csv_file)
		count = [0, 0, 0, 0]	# 0-40, 40-60, 60-80, 80+

		for row in reader:
			if row['VETERAN3'] == '1':
				age = float(row['_AGE80'])
				if age < 40:
					count[0] += 1
				elif age < 60:
					count[1] += 1
				elif age < 80:
					count[2] += 1
				else:
					count[3] += 1
		print count



if __name__ == "__main__":
	count_for_chf()