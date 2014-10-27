#!/bin/bash

python nhanes_brfss.py /Users/Shia/Documents/Capstone/FeatExtraction/data /Users/Shia/Documents/Capstone/FeatExtraction/data/nhanes/csv_final/merged.csv /Users/Shia/Documents/Capstone/FeatExtraction/data/brfss/extracted_nhanes_ized.csv

python nhanes_hpn.py /Users/Shia/Documents/Capstone/FeatExtraction/data /Users/Shia/Documents/Capstone/FeatExtraction/data/nhanes_brfss_match.csv /Users/Shia/Documents/Capstone/FeatExtraction/data/hpn/nhanes_ized.csv