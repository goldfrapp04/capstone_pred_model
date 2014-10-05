import csv
import sys
sys.path.append('/xport/')
import xport

def write_to_csv(output_file_path, xpt_dir_path, files_fields, years):
	

	out_fields = ['Year']
	for fields in files_fields.itervalues():
		out_fields.extend(fields)

	out_rows = []
	for year in years:
		out_row = {'Year': year}
		for file_name, fields in files_fields.iteritems():
			for field in fields:
				out_row[field] = 1 if has_field(xpt_dir_path + file_name + year + '.XPT', field) else 0
				# print file_name + '_' + year + ':' + field + ':' + str(has_field(sys.argv[1] + file_name + '_' + year + '.XPT', field))
		out_rows.append(out_row)

	with open(output_file_path, 'wb') as out:
		writer = csv.DictWriter(out, out_fields)
		writer.writeheader()
		for out_row in out_rows:
			writer.writerow(out_row)

def has_field(xpt_file_name, field_name):
	with xport.XportReader(xpt_file_name) as reader:
		for field_obj in reader.fields:
			if field_obj['name'] == field_name:
				return True
		return False

# def has_fields(xpt_file_name, fields_names):
# 	for field_name in fields_names:
# 		if has_field(xpt_file_name, field_name) == False:
# 			return False
# 	return True

def make_dir_path(dir_path):
	if not dir_path.endswith('/'):
		return dir_path + '/'
	return dir_path

if __name__ == "__main__":
	XPT_DIR_PATH = make_dir_path(sys.argv[2])

	files_fields = {
		'MCQ':		['SEQN', 'MCQ160B', 'MCQ053', 'MCQ080', 'MCQ160C', 'MCQ220'],
		'BPQ':		['SEQN', 'BPQ020'],
		'DEMO':		['SEQN', 'DMDEDUC2', 'RIAGENDR', 'RIDAGEYR', 'RIDRETH3'],
		'DIQ':		['SEQN', 'DIQ010'],
		'DPQ':		['SEQN', 'DPQ020'],
		'HUQ':		['SEQN', 'HUQ050'],
		'OHQ':		['SEQN', 'OHQ030'],
		'OHXDEN':	['SEQN', 'OHDEXSTS'],
		'RXQ_RX':	['SEQN', 'RXDCOUNT'],
		'SMQ':		['SEQN', 'SMQ040'],
		'WHQ':		['SEQN', 'WHQ030']
	}
	years = ['_F', '_G']

	write_to_csv(sys.argv[1], XPT_DIR_PATH, files_fields, years)
