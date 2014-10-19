import csv
import random
import sys
import time

class FieldWeight:
	def __init__(self, field_n, field_b, weight, upperbound = None):
		self.field_n = field_n
		self.field_b = field_b
		self.weight = weight
		if upperbound is not None:
			self.upperbound = upperbound

def calculate_score(row_n, row_b, FIELDS_CATEGORICAL, FIELDS_NUMERICAL):
	score = 0

	for field_weight in FIELDS_CATEGORICAL:
		field_n = field_weight.field_n
		field_b = field_weight.field_b
		weight = field_weight.weight
		if row_n[field_n] == row_b[field_b]:
			score += weight
	
	for field_weight in FIELDS_NUMERICAL:
		field_n = field_weight.field_n
		field_b = field_weight.field_b
		weight = field_weight.weight
		upperbound = field_weight.upperbound

		# 1 - |n - b| / max
		if field_n == 'RIDAGEYR':	
			score += weight * (1 - abs(float(row_n[field_n]) - float(row_b[field_b])) / upperbound)
		elif field_n == 'HSQ480':
			if float(row_n[field_n]) <= 30 and float(row_b[field_b]) <= 30:
				score += weight * (1 - abs(float(row_n[field_n]) - float(row_b[field_b])) / upperbound)
		else:	# DMDEDUC2, SMQ040
			if float(row_n[field_n]) > 0 and float(row_n[field_n]) < 7 and float(row_b[field_b]) > 0 and float(row_b[field_b]) < 7:
				score += weight * (1 - abs(float(row_n[field_n]) - float(row_b[field_b])) / upperbound)

	return score

def make_dir_path(dir_path):
	if not dir_path.endswith('/'):
		return dir_path + '/'
	return dir_path

# Args: output_dir_path nhanes_file_path brfss_file_path
if __name__ == "__main__":

	FIELDS_CATEGORICAL = [
		FieldWeight('RIAGENDR',	'SEX',		.3), 
		FieldWeight('RIDRETH1',	'_RACE_G1',	.2),
		# FieldWeight('SMQ020', 	'SMOKE100',	.025),
		FieldWeight('DIQ010',	'DIABETE3',	.05),
		FieldWeight('MCQ160C',	'CVDCRHD4',	.05),
		FieldWeight('MCQ220',	'CHCCNCR',	.05)
	]
	FIELDS_NUMERICAL = [
		FieldWeight('RIDAGEYR',	'_AGE80',	.2,		99),
		FieldWeight('DMDEDUC2',	'EDUCA',	.05,	5),
		FieldWeight('SMQ040',	'SMOKDAY2', .025,	3),
		# FieldWeight('HSQ480',	'MENTHLTH',	.05,	30)
	]
	fields_out = ['SCORE']
	start_time = time.clock()

	# Read BRFSS data into memory
	rows_brfss = []
	deleted_b = []
	with open(sys.argv[3], 'rb') as in_brfss:
		reader_b = csv.DictReader(in_brfss)
		fields_out.extend(reader_b.fieldnames)
		for row in reader_b:
			rows_brfss.append(row)
			deleted_b.append(False)

	# Find match for each row in NHANES
	with open(sys.argv[2], 'rb') as in_nhanes:
		with open(make_dir_path(sys.argv[1]) + 'nhanes_brfss_match.csv', 'wb') as out:
			reader_n = csv.DictReader(in_nhanes)
			fields_out.extend(reader_n.fieldnames)
			writer = csv.DictWriter(out, fields_out)
			writer.writeheader()

			for index, row_n in enumerate(reader_n):
				highest_score = 0
				highest_score_row_b = {}
				index_to_delete_b = len(rows_brfss)

				for i in range(100):
					index = len(rows_brfss)
					while index == len(rows_brfss) or deleted_b[index] == True:
						index = random.randint(0, len(rows_brfss) - 1)
					row_b = rows_brfss[index]
					score = calculate_score(row_n, row_b, FIELDS_CATEGORICAL, FIELDS_NUMERICAL)
					if score > highest_score:
						highest_score = score
						highest_score_row_b = row_b
						index_to_delete_b = index

				if highest_score > 0:
					row_n.update(rows_brfss[index_to_delete_b])
					row_n['SCORE'] = highest_score
					writer.writerow(row_n)
				else:
					print 'No match found'

	end_time = time.clock()
	print end_time - start_time
	
