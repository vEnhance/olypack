import csv
import re

feedback_regex = re.compile(r'\\ii\[([A-Z]-[0-9][0-9])')
feedback = {}

with open('final-report/final-NO-SEND-report.tex') as f:
	reading_house_comments = False
	slug = ''
	current_comments = ''

	for line in f:
		if line.startswith(r'\chapter{Comment'):
			reading_house_comments = True
		elif reading_house_comments is False:
			continue
		elif (m := feedback_regex.match(line)) is not None:
			if slug:
				feedback[slug] = current_comments
				current_comments = ''
			slug = m.group(1)
		elif line.strip() == r'\end{description}' or line.startswith(r'\chapter'):
			feedback[slug] = current_comments
			if line.startswith(r'\chapter'):
				break
			else:
				current_comments = ''
				slug = ''
		elif slug:
			current_comments += line

with open('output/summary.csv') as f:
	reader = csv.reader(f, delimiter=',', quotechar='"')
	for row in reader:
		print(f'# Problem {row[0]} ({row[1]})\n')
		print(f'The author of the problem ({row[1]}) is {row[2]}.\n')
		print(r'## Comments' + '\n')
		print(feedback[row[0]].strip())
		# TODO
		print(r'## Ratings' + '\n')
		print(f'- Quality ratings: {[int(x) for x in row[3:8]]}')
		print(f'- Difficulty ratings: {[int(x) for x in row[8:13]]}')
		print('\n')
		print(r'---------------------------------')
