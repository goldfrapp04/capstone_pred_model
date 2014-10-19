import csv
import sys

def count_value_equal(csv_file_name, field0, field1):
	with open(csv_file_name, 'rb') as csv_file:
		reader = csv.DictReader(csv_file)
		count = 0
		for row in reader:
			if row[field0] == row[field1]:
				count += 1
		print 'equal:' + str(count) + ' unequal:' + str(reader.line_num - count)

if __name__ == "__main__":
	count_value_equal(sys.argv[1], sys.argv[2], sys.argv[3])