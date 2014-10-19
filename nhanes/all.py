import combine
import extract
import sys
sys.path.append('../')
import util

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print 'Usage: all.py XPT_DIR_PATH INTERIM_CSV_DIR_PATH FINAL_CSV_FILE_PATH'
		sys.exit(1)

	XPT_DIR_PATH = util.make_dir_path(sys.argv[1])
	INTERIM_CSV_DIR_PATH = util.make_dir_path(sys.argv[2])
	FINAL_CSV_DIR_PATH = util.make_dir_path(sys.argv[3])

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
	years = ['G']

	csv_file_paths = []
	for file_name, fields in files_fields.iteritems():
		for year in years:
			extract.extract(INTERIM_CSV_DIR_PATH, XPT_DIR_PATH + file_name + '_' + year + '.XPT', fields)
			csv_file_paths.append(INTERIM_CSV_DIR_PATH + file_name + "_" + year + '.csv')
			combine.combine_fields(FINAL_CSV_DIR_PATH + 'combined_' + year + '.csv', csv_file_paths)
