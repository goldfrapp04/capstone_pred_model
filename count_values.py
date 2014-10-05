import csv
import sys

def count_value(csv_file_name, fields, values):
	with open(csv_file_name, 'rb') as csv_file:
		reader = csv.DictReader(csv_file)
		count = 0
		for row in reader:
			for i, value in enumerate(values):
				if row[fields[i]] != value:
					break
				if i == len(values) - 1:
					count += 1
		return count

if __name__ == "__main__":
	fields = []
	values = []
	num_fields = (len(sys.argv) - 2) / 2
	for i in range(2, 2 + num_fields):
		fields.append(sys.argv[i])
		values.append(sys.argv[i + num_fields])
	print count_value(sys.argv[1], fields, values)