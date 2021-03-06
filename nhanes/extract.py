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
	        		out_row[field] = row[field]
	        		# if is_field_valid(field, row[field]):
	        		# 	out_row[field] = row[field]
	        		# else:
	        		# 	are_all_fields_valid = False
	        		# 	break

	        	# if are_all_fields_valid:
	        	writer.writerow(out_row)

def get_valid_value(field, value):
	return value
	# if field == 'SEQN':
	# 	return value
	# if field.startswith('MCQ') or field == 'BPQ020':	# Medical conditions and Blood pressure
	# 	if value == 1 or value == 2:
	# 		return value
	# 	else
	# 		return 2
	# if field.startswith('RI') or field == 'RXDCOUNT':	# Demographic and Prescription
	# 	if value > 0:
	# 		return value
	# 	else
	# 		return 1
	# # Smoking, Diabetes, Oral health dentition, Weight history 
	# if field == 'SMQ040':
	# 	if value >= 1 and value <= 3:
	# 		return value
	# 	else
	# 		return 3
	# if field == 'DIQ010':
	# 	if value >= 1 and value <= 3:
	# 		return value
	# 	else
	# 		return 2
	# if field == 'OHDEXSTS' or field == 'WHQ030':
	# 	if value >= 1 and value <= 3:
	# 		return value
	# 	else
	# 		return 1
	# if field == 'DPQ020':	# Depression
	# 	if value >= 0 and value <= 3:
	# 		return value
	# 	else
	# 		return 0
	# if field == 'HUQ050':	# Hospital utilization
	# 	if value >= 0 and value <= 5:
	# 		return value
	# 	else
	# 		return 2
	# if field == 'DMDEDUC2':	# Demographic - Education
	# 	if value >= 1 and value <= 5:
	# 		return value
	# 	else
	# 		return 
	# if field == 'OHQ030':
	# 	if value >= 1 and value <= 7:	# Oral health
	# 		return value
	# 	else
	# 		return 1

def is_field_valid(field, value):
	if field == 'SEQN':
		return True
	if field.startswith('MCQ') or field == 'BPQ020':	# Medical conditions and Blood pressure
		if value == 1 or value == 2:
			return True
	if field.startswith('RI') or field == 'RXDCOUNT':	# Demographic and Prescription
		if value > 0:
			return True
	if field == 'SMQ040' or field == 'DIQ010' or field == 'OHDEXSTS' or field == 'WHQ030':	# Smoking, Diabetes, Oral health dentition, Weight history 
		if value >= 1 and value <= 3:
			return True
	if field == 'DPQ020':	# Depression
		if value >= 0 and value <= 3:
			return True
	if field == 'HUQ050':	# Hospital utilization
		if value >= 0 and value <= 5:
			return True
	if field == 'DMDEDUC2':	# Demographic - Education
		if value >= 1 and value <= 5:
			return True
	if field == 'OHQ030':
		if value >= 1 and value <= 7:	# Oral health
			return True
	return False

if __name__ == "__main__":
	extract(sys.argv[1], sys.argv[2], ['SEQN', 'MCQ160B', 'MCQ053', 'MCQ080', 'MCQ160C', 'MCQ220'])
