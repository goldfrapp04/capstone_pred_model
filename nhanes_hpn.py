
# Args: output_dir_path nhanes_file_path hpn_file_path
if __name__ == "__main__":
	fields_out = []
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
			