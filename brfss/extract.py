import csv
import sys

# extract VETERAN3=1 only
def extract(output_dir_path, input_file_path, fields):
	VETERAN3_STARTING_COLUMN = 146
	VETERAN3_FIELD_LENGTH = 1

	with open(input_file_path, 'rb') as in_asc:
		with open(output_dir_path + 'extracted.csv', 'wb') as out:
			writer = csv.DictWriter(out, fields.keys())
			writer.writeheader()
			for line in in_asc:
				if line[(VETERAN3_STARTING_COLUMN - 1) : (VETERAN3_STARTING_COLUMN - 1 + VETERAN3_FIELD_LENGTH)] == '1':
					out_row = {}
					for field, indices in fields.iteritems():
						starting_column = indices[0]
						field_length = indices[1]
						# BRFSS columns start at 1, so minus 1
						out_row[field] = line[(starting_column - 1) : (starting_column - 1 + field_length)]
					writer.writerow(out_row)

def make_dir_path(dir_path):
	if not dir_path.endswith('/'):
		return dir_path + '/'
	return dir_path

if __name__ == "__main__":

	# Variable name: [Starting column, Field length]
	fields = {

		# Merging variables
		'_AGE80':	[2364,	2],
		'SEX':		[178, 	1],
		'_RACE_G1':	[2176,	1],
		'EDUCA':	[150,	1],
		'SMOKE100':	[187,	1],
		'SMOKDAY2':	[188,	1],
		'DIABETE3':	[109,	1],
		'CVDCRHD4':	[99,	1],
		'CHCSCNCR':	[103,	1],
		'CHCOCNCR':	[104,	1],
		'MENTHLTH':	[83,	2],

		# BRFSS unique variables
		'GENHLTH':	[80,	1],
		'PHYSHLTH':	[81,	2],
		'EMPLOY1':	[151,	1],
		'EXERANY2':	[220,	1],
		'ADDEPEV2':	[107,	1],
		'TOLDHI2':	[97,	1],
		'CVDSTRK3':	[100,	1],
		'ASTHMA3':	[101,	1],
		'CHCCOPD1':	[105,	1],
		'MARITAL':	[147,	1],
		'RENTHOM1':	[177,	1],
		'MAXDRNKS':	[200,	2],
		'FRUIT1':	[205,	3],
		'FVGREEN':	[211,	3],
		'WTCHSALT':	[352,	1],
		'EMTSUPRT':	[532,	1]
	}
	extract(make_dir_path(sys.argv[1]), sys.argv[2], fields)