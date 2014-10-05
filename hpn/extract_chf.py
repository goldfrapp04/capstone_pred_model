import csv
import sys

def extract_chf(output_file_path, input_file_path):
	with open(input_file_path, 'rb') as claims:
		with open(output_file_path, 'wb') as out:
			reader = csv.DictReader(claims)
			writer = csv.DictWriter(out, ['MemberID'])
			for in_row in reader:
				if in_row['PrimaryConditionGroup'] == 'CHF':
					out_row = {
						'MemberID': in_row['MemberID']
					}
					writer.writerow(out_row)

if __name__ == "__main__":
	extract_chf(sys.argv[1], sys.argv[2])