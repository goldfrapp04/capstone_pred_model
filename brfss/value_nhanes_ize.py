import csv
import sys

# extract VETERAN3=1 only
def value_nhanes_ize(output_dir_path, input_file_path):
	with open(input_file_path, 'rb') as in_asc:
		reader = csv.DictReader(in_asc)
		with open(output_dir_path + 'extracted_nhanes_ized.csv', 'wb') as out:

			writer_fields = list(reader.fieldnames)

			# Skin cancer + Other cancer = Cancer
			writer_fields.remove('CHCSCNCR')
			writer_fields.remove('CHCOCNCR')
			writer_fields.append('CHCCNCR')

			writer = csv.DictWriter(out, writer_fields)
			writer.writeheader()

			for in_row in reader:
				out_row = {}

				out_row['_AGE80'] = in_row['_AGE80']
				out_row['SEX'] = in_row['SEX']
				out_row['CVDCRHD4'] = in_row['CVDCRHD4']

				# _RACE_G1
				try:
					race = int(in_row['_RACE_G1'])
					if race == 1:
						out_row['_RACE_G1'] = 3
					elif race == 2:
						out_row['_RACE_G1'] = 4
					elif race == 3:
						out_row['_RACE_G1'] = 1	# BRFSS Hispanic -> NHANES Mexican American, not Other Hispanic
					elif race == 4 or race == 5:
						out_row['_RACE_G1'] = 5
				except ValueError:
					continue	# Discard rows where _RACE_G1 is not provided

				# EDUCA
				try:
					edu = int(in_row['EDUCA'])
					if edu == 1 or edu == 2:
						out_row['EDUCA'] = 1
					elif edu <= 6:
						out_row['EDUCA'] = edu - 1
					else:
						out_row['EDUCA'] = edu
				except ValueError:
					out_row['EDUCA'] = 9

				# SMOKE100
				try:
					smoke = int(in_row['SMOKE100'])
					out_row['SMOKE100'] = smoke
				except ValueError:
					out_row['SMOKE100'] = 9

				# SMOKDAY2
				try:
					smoke_day = int(in_row['SMOKDAY2'])
					out_row['SMOKDAY2'] = smoke_day
				except ValueError:
					out_row['SMOKDAY2'] = 9

				# DIABETE3
				try:
					diabetes = int(in_row['DIABETE3'])
					if diabetes == 2 or diabetes == 3:
						out_row['DIABETE3'] = 2
					elif diabetes == 4:
						out_row['DIABETE3'] = 3
					else:
						out_row['DIABETE3'] = diabetes
				except ValueError:
					out_row['DIABETE3'] = 9

				# CANCER
				skin_cancer = int(in_row['CHCSCNCR'])
				other_cancer = int(in_row['CHCOCNCR'])
				if skin_cancer == 1 or other_cancer == 1:
					out_row['CHCCNCR'] = 1
				else:
					out_row['CHCCNCR'] = 2

				# MENTHLTH
				try:
					mental_health = int(in_row['MENTHLTH'])
					if mental_health == 88:
						out_row['MENTHLTH'] = 0
					else:
						out_row['MENTHLTH'] = mental_health
				except ValueError:
					out_row['MENTHLTH'] = 99

				writer.writerow(out_row)
					

def make_dir_path(dir_path):
	if not dir_path.endswith('/'):
		return dir_path + '/'
	return dir_path

if __name__ == "__main__":
	value_nhanes_ize(make_dir_path(sys.argv[1]), sys.argv[2])