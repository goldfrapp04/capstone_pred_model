import csv
import sys

def extract(output_dir_path, input_file_path, fields):
	with open(input_file_path, 'rb') as in_asc:
		with open(output_dir_path + 'extracted.csv', 'wb') as out:
			writer = csv.DictWriter(out, fields.keys())
			writer.writeheader()
			for line in in_asc:
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
		'SEQNO':	[35,	10],
		'GENHLTH':	[80,	1],
		'PHYSHLTH':	[81,	2],
		'EDUCA':	[150,	1],
		'EMPLOY1':	[151,	1],
		'SMOKE100':	[187,	1],
		'SMOKDAY2':	[188,	1],
		'EXERANY2':	[220,	1]
	}
	extract(make_dir_path(sys.argv[1]), sys.argv[2], fields)