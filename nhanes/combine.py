import csv
import sys

def combine_fields(output_csv_path, csv_file_paths):
	readers = []
	for csv_file_path in csv_file_paths:
		readers.append(csv.DictReader(open(csv_file_path, 'rb')))

	fields = ['SEQN']
	out_rows = {}
	for reader in readers:

		for field in reader.fieldnames:
			if field != 'SEQN':
				fields.append(field)

		for in_row in reader:
			if in_row['SEQN'] not in out_rows:
				out_rows[in_row['SEQN']] = {}
			for key, value in in_row.iteritems():
				out_rows[in_row['SEQN']][key] = value

	with open(output_csv_path, 'wb') as out:
		writer = csv.DictWriter(out, fields)
		writer.writeheader()

		for out_row in out_rows.itervalues():
			if (has_all_fields(out_row, fields)):
				writer.writerow(out_row)

def has_all_fields(row, fields):
	# for field in fields:
	# 	if field not in row:
	# 		return False
	return True

def combine_years():
	return True

if __name__ == "__main__":
	csv_file_paths = []
	for i in range(2, len(sys.argv)):
		csv_file_paths.append(sys.argv[i])
	combine_fields(sys.argv[1], csv_file_paths)
	