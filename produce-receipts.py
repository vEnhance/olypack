import csv
import re

import yaml

feedback_regex = re.compile(r'\\item\[([A-Z]-[0-9][0-9])')
feedback = {}

NOT_LISTED = r'''# Not listed

Thank you for submitting this problem!
We ended up not shortlisting this problem to keep the
size of the review packet manageable,
however you should shortly hear back about other problems of yours
which did make it into the review stage.

This problem is hereby returned now, and you may send it wherever you like.


-------------------------

'''
print(NOT_LISTED)

salutation = r'''Thank you for submitting your problem!
This is the return email for a problem which made it to the review stage,
meaning it received ratings from my small panel of olympiad enthusiasts.
Below you can find your problem status,
a few comments summarizing the feedback from the reviewers,
and numerical ratings among those reviewers who worked on the problem.
Feel free to follow up with any questions.'''

DELETABLE_ENVIRONMENTS = [
	r'\begin{itemize}',
	r'\end{itemize}',
	r'\begin{enumerate}',
	r'\end{enumerate}',
	r'\begin{quote}',
	r'\end{quote}',
]

with open('data.yaml') as f:
	data = yaml.load(f, Loader=yaml.SafeLoader)
	chosen = []
	for day in data['chosen'].values():
		chosen += day

with open('final-report/final-NO-SEND-report.tex') as f:
	reading_house_comments = False
	slug = ''
	current_comments = ''

	for line in f:
		if line.startswith(r'\chapter{Comment'):
			reading_house_comments = True
		elif reading_house_comments is False:
			continue
		elif (m := feedback_regex.match(line.strip())) is not None:
			if slug:
				feedback[slug] = current_comments
			current_comments = ' '.join(line.split(' ')[1:])
			slug = m.group(1)
		elif line.strip() == r'\end{description}' or line.startswith(r'\chapter'):
			feedback[slug] = current_comments
			if line.startswith(r'\chapter'):
				break
			else:
				current_comments = ''
				slug = ''
		elif line.strip() in DELETABLE_ENVIRONMENTS and slug:
			current_comments += '\n'
		elif line.strip().startswith(r'\ii') and slug:
			current_comments += line.lstrip().replace(r'\ii', '- ')
		elif slug:
			current_comments += line.strip() + '\n'

QUALITY_RATINGS = ['Excellent', 'Nice', 'Acceptable', 'Mediocre', 'Unsuitable']
DIFFICULTY_RATINGS = ['IMO 1', 'IMO 1.5', 'IMO 2', 'IMO 2.5', 'IMO 3']

with open('tex/names.txt') as f:
	report_audience = [line.strip() for line in f.readlines()]

with open('output/summary.csv') as f:
	reader = csv.reader(f, delimiter=',', quotechar='"')
	for row in reader:
		code = row[0]
		author = row[2]
		s = '*' if author not in report_audience else ''
		print(f'# {s} Problem {code} ({row[1]})\n')
		print(f'The author of the problem ({row[1]}) is **{row[2]}**.\n')
		print(r'')
		print(salutation)

		print(r'## Status' + '\n')
		if code in chosen:
			n = 1 + chosen.index(code)
			print(f"Congratulations! This problem was selected as problem {n}.")
			print("Here is the current statement:")
			print("> INSERT STATEMENT HERE" + "\n")
			print("If you notice anything you think should change, please let me know.")
			print("And of course, keep this confidential of course until after the exam.")
		else:
			print("This problem is hereby returned to you now,")
			print("meaning that you can now propose it to any other competition,")
			print("including next year if you so choose.")
			print("If possible, please avoid discussing this problem decision with others")
			print("until after the exam, to avoid potentially leaking indirect information")
			print("about other problems that may have been chosen.")

		print(r'## Comments' + '\n')
		print(feedback.get(code, "No comments.").strip())
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
