# Documentation: 
# http://pypi.python.org/pypi/xport/0.1.0

import csv
import sys
sys.path.append('../xport/')
import xport

def extract(output_dir_path, xpt_file_path, fields):
	with xport.XportReader(xpt_file_path) as reader:
	    with open(output_dir_path + xpt_file_path[xpt_file_path.rfind('/') + 1 : xpt_file_path.find('.')] + '.csv', 'wb') as out:
	        writer = csv.DictWriter(out, fields)
	        writer.writeheader()

	        for row in reader:
	        	out_row = {}
	        	are_all_fields_valid = True

	        	for field in fields:
	        		if is_field_valid(field, row[field]):
	        			out_row[field] = row[field]
	        		else:
	        			are_all_fields_valid = False
	        			break

	        	if are_all_fields_valid:
	        		writer.writerow(out_row)

def is_field_valid(field, value):
	if field == 'SEQN':
		return True
	if field.startswith('MCQ') or field == 'BPQ020':	# Medical conditions and Blood pressure
		if value == 1 or value == 2:
			return True
	if field.startswith('RI') or field == 'RXDCOUNT':	# Demographic and Prescription
		if value > 0:
			return True
	if field == 'SMQ040' or field == 'DIQ010':	# Smoking and Diabetes
		if value > 0 and value <= 3:
			return True
	if field == 'DPQ020':	# Depression
		if value >= 0 and value <= 3:
			return True
	if field == 'HUQ050':	# Hospital utilization
		if value >= 0 and value <= 5:
			return True
	return False

if __name__ == "__main__":
	extract(sys.argv[1], sys.argv[2], ['SEQN', 'MCQ160B', 'MCQ053', 'MCQ080', 'MCQ160C', 'MCQ220'])
	