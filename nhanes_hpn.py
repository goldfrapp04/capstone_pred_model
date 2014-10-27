import csv
import field_weight
from field_weight import FieldWeight
import random
import sys
import time
import util

def calculate_score(row_n, row_h, FIELDS_WEIGHTS, index_last_categorical):
	score = 0

	for field_weight in FIELDS_WEIGHTS[ : (index_last_categorical + 1)]:
		field_n = field_weight.field_n
		field_h = field_weight.field_b
		weight = field_weight.weight
		if row_n[field_n] == row_h[field_h]:
			score += weight

	for field_weight in FIELDS_WEIGHTS[(index_last_categorical + 1) : ]:
		field_n = field_weight.field_n
		field_h = field_weight.field_b
		weight = field_weight.weight
		upperbound = field_weight.upperbound
		if len(row_h[field_h]):
			score += weight * (1 - abs(float(row_n[field_n]) - float(row_h[field_h])) / upperbound)

	return score

# Args: output_dir_path nhanes_file_path hpn_file_path
if __name__ == "__main__":
	FIELDS_WEIGHTS = [
		# Categorical
		FieldWeight('MCQ160B',	'Congestive Heart Faliure Unspecified',	.3),
		FieldWeight('RIAGENDR',	'Female',	.25),
		FieldWeight('DIQ010',	'SECONDARY DIABETES MELLITUS WITHOUT MENTION OF COMPLICATION, NOT STATED AS UNCONTROLLED, OR UNSPECIFIED',	.1),
		
		# Numerical
		FieldWeight('RIDAGEYR',	'Age',		.25,	89),
		FieldWeight('RXDCOUNT',	'drugcnt',	.1,		15)
	]
	index_last_categorical = 2 	# NEED TO BE CHANGED
	fields_out = ['NHANES_HPN_SCORE']
	start_time = time.clock()

	# Read NHANES data into memory
	rows_n = []
	deleted_n = []
	with open(sys.argv[2], 'rb') as in_n:
		reader_n = csv.DictReader(in_n)
		fields_out.extend(reader_n.fieldnames)
		for row in reader_n:
			rows_n.append(row)
			deleted_n.append(False)

	# Find match for each row in HPN
	with open(sys.argv[3], 'rb') as in_h:
		with open(util.make_dir_path(sys.argv[1]) + 'nhanes_hpn_match.csv', 'wb') as out:
			reader_h = csv.DictReader(in_h)
			fields_out.extend(field_weight.diff_fields(reader_h.fieldnames, FIELDS_WEIGHTS))
			fields_out.remove('PatientID')
			writer = csv.DictWriter(out, fields_out)
			writer.writeheader()

			for row_h in reader_h:
				highest_score = 0
				highest_score_row_n = {}
				index_to_delete_n = len(rows_n)

				for i in range(10):
					index = len(rows_n)
					while index == len(rows_n) or deleted_n[index] == True:
						index = random.randint(0, len(rows_n) - 1)
					row_n = rows_n[index]
					score = calculate_score(row_n, row_h, FIELDS_WEIGHTS, index_last_categorical)
					if score > highest_score:
						highest_score = score
						highest_score_row_n = row_n
						index_to_delete_n = index

				if highest_score > 0:
					row_out = dict(highest_score_row_n)
					for key, value in row_h.iteritems():
						if key in fields_out:
							row_out[key] = value
					row_out['NHANES_HPN_SCORE'] = highest_score
					writer.writerow(row_out)
				else:
					print 'No match found'

	end_time = time.clock()
	print end_time - start_time

			