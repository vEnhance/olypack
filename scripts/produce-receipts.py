import csv
import re

feedback_regex = re.compile(r'\\ii\[([A-Z]-[0-9][0-9])')
feedback = {}

salutation = r'''Thank you for submitting your problem!
This is the return email for a problem which made it to the review stage,
meaning it received ratings from my small panel of olympiad experts.
'''

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
		elif line.strip() == r'\end{quote}' or line.strip() == r'\begin{quote}':
			current_comments += '\n'
		elif slug:
			current_comments += line

QUALITY_RATINGS = ['Excellent', 'Nice', 'Acceptable', 'Mediocre', 'Unsuitable']
DIFFICULTY_RATINGS = ['IMO 1', 'IMO 1.5', 'IMO 2', 'IMO 2.5', 'IMO 3']

with open('output/summary.csv') as f:
	reader = csv.reader(f, delimiter=',', quotechar='"')
	for row in reader:
		print(f'# Problem {row[0]} ({row[1]})\n')
		print(f'The author of the problem ({row[1]}) is {row[2]}.\n')

		print(r'## Status' + '\n')
		# if selected
		# else

		print(r'## Comments' + '\n')
		print(feedback[row[0]].strip())
		# TODO
		print('')

		print(r'## Ratings' + '\n')
		print(r'The following ratings in the informal beauty contest appeared:')
		print('')
		for i, r in enumerate(QUALITY_RATINGS):
			print(f'- {row[7-i]} ratings of {r}')
		print('')
		print(r'The following difficulty ratings appeared:')
		print('')
		for i, r in enumerate(DIFFICULTY_RATINGS):
			print(f'- {row[8+i]} ratings of {r}')
		print('\n')
		print(r'---------------------------------')
