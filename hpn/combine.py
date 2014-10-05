import csv
import sys

def combine(output_dir_path, csv_file_paths, key_field, other_fields):
	readers = []
	for csv_file_path in csv_file_paths:
		readers.append(csv.DictReader(open(csv_file_path, 'rb')))

	out_rows = {}
	out_fields = [key_field]

	for in_row in readers[0]:	# MemberID of CHF
		out_rows[in_row[key_field]] = {key_field: in_row[key_field]}

	for i in range(1, len(readers)):
		out_fields.extend(other_fields[i])
		for in_row in readers[i]:
			if in_row[key_field] in out_rows:
				for field in other_fields[i]:
					out_rows[in_row[key_field]][field] = in_row[field]

	with open(output_dir_path + 'combined.csv', 'wb') as out:
		writer = csv.DictWriter(out, out_fields)
		writer.writeheader()

		for out_row in out_rows.itervalues():
			writer.writerow(out_row)

def make_dir_path(dir_path):
	if not dir_path.endswith('/'):
		return dir_path + '/'
	return dir_path

if __name__ == "__main__":
	OUTPUT_CSV_DIR_PATH = make_dir_path(sys.argv[1])
	INPUT_CSV_DIR_PATH = make_dir_path(sys.argv[2])
	files_fields = [
		{'chf':						[]},
		{'Members':					['AgeAtFirstClaim', 'Sex']},
		{'DaysInHospital_Y2':		['DaysInHospital_Y2']},
		{'DaysInHospital_Y3':		['DaysInHospital_Y3']},
		{'DrugCount':				['DrugCount']}
	]

	csv_file_paths = []
	other_fields = []

	for file_field in files_fields:
		csv_file_paths.append(INPUT_CSV_DIR_PATH + file_field.keys()[0] + ".csv")
		other_fields.append(file_field.values()[0])

	combine(OUTPUT_CSV_DIR_PATH, csv_file_paths, 'MemberID', other_fields)
