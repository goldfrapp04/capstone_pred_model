import csv
import random
import re
import sys
sys.path.append('../')
import util

def calculate(field, in_row):
	for key, value in in_row.iteritems():
		if key.startswith(field) and value == '1':
			lowerbound = int(re.search(r'\d+', key).group())

			if field == 'Age':
				return random.randint(lowerbound, lowerbound + 9)
			elif field == 'LOS':
				if lowerbound == 0 or lowerbound == 1:
					return lowerbound
				else:
					return random.randint(lowerbound, lowerbound + 8)
			elif field == 'labcnt':
				if lowerbound == 1:
					return random.randint(1, 3)
				else:
					return random.randint(lowerbound, lowerbound + 3)
			elif field == 'drugcnt':
				return random.randint(lowerbound, lowerbound + 5)
			else:
				raise NameError(field)
	print 'Error: ' + field + ' ' + str(in_row)
	return -1


def value_nhanes_ize(output_dir_path, input_file_path):
	FIELDS_OUT = [
		# Variables need processing
		'Female', 'Age', 'LOS', 'labcnt', 'drugcnt', 'Congestive Heart Faliure Unspecified', 
		'SECONDARY DIABETES MELLITUS WITHOUT MENTION OF COMPLICATION, NOT STATED AS UNCONTROLLED, OR UNSPECIFIED',

		# Variables need no processing
		'PatientID', 'SYPHILITIC ENDOCARDITIS OF VALVE UNSPECIFIED',	
		'HYPERTROPHIC OBSTRUCTIVE CARDIOMYOPATHY', 'MENINGOCOCCAL ENDOCARDITIS', 'DIPHTHERITIC MYOCARDITIS',
		'Cardioverter-defibrillator, dual chamber (implantable)',
		'Pacemaker, dual chamber, rate-responsive (implantable)', 'Stent, coated/covered, with delivery system',
		'Readmitted0-1month'
	]
	INDEX_LAST_PROCESSED = FIELDS_OUT.index('SECONDARY DIABETES MELLITUS WITHOUT MENTION OF COMPLICATION, NOT STATED AS UNCONTROLLED, OR UNSPECIFIED')

	# _csv.Error: new-line character seen in unquoted field - do you need to open the file in universal-newline mode?
	with open(input_file_path, 'rU') as in_hpn:
		reader = csv.DictReader(in_hpn)
		with open(output_dir_path + 'nhanes_ized.csv', 'wb') as out:
			writer = csv.DictWriter(out, FIELDS_OUT)
			writer.writeheader()

			num_invalid_rows = 0
			for in_row in reader:
				out_row = {}

				# Variables unique to HPN
				for field in FIELDS_OUT[INDEX_LAST_PROCESSED : ]:
					out_row[field] = in_row[field]

				# Variables shared with NHANES and need processing
				out_row['Female'] = 2 if in_row['Female'] == '1' else 1
				out_row['Congestive Heart Faliure Unspecified'] = 2 if in_row['Congestive Heart Faliure Unspecified'] == '1' else 1
				out_row['SECONDARY DIABETES MELLITUS WITHOUT MENTION OF COMPLICATION, NOT STATED AS UNCONTROLLED, OR UNSPECIFIED'] = 2 if in_row['SECONDARY DIABETES MELLITUS WITHOUT MENTION OF COMPLICATION, NOT STATED AS UNCONTROLLED, OR UNSPECIFIED'] == '0' else 1

				for field in ['Age', 'LOS', 'labcnt', 'drugcnt']:
					calculatedValue = calculate(field, in_row)
					if calculatedValue >= 0:
						out_row[field] = calculatedValue
					else:
						num_invalid_rows += 1

				writer.writerow(out_row)
 
			print num_invalid_rows

if __name__ == "__main__":
	value_nhanes_ize(util.make_dir_path(sys.argv[1]), sys.argv[2])