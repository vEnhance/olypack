all: packet

packet: output/confidential-probs.pdf output/confidential-solns.pdf
report: output/confidential-report.pdf
draft: output/draft-solns-day1.pdf
receipt: output/receipt.html

output/authors.tsv tex/data-index.tex tex/data-probs.tex tex/data-solns.tex: olypack/produce-packet.py data.yaml $(wildcard source/*.tex)
	python3 $<

tex/internal-NO-SEND-probs.pdf: tex/internal-NO-SEND-probs.tex \
	tex/data-probs.tex tex/data-index.tex \
	tex/meta.sty tex/instructions.tex tex/names.txt tex/assign.txt
	latexmk -cd $<
	touch $@

tex/internal-NO-SEND-solns.pdf: tex/internal-NO-SEND-solns.tex \
	tex/data-probs.tex tex/data-solns.tex \
	tex/meta.sty tex/instructions.tex tex/names.txt tex/assign.txt
	latexmk -cd $<
	touch $@

output/confidential-probs.pdf: tex/internal-NO-SEND-probs.pdf password password
	qpdf --encrypt $$(cat password) $$(cat password) 128 \
	--print=none --modify=none -- $< $@

output/confidential-solns.pdf: tex/internal-NO-SEND-solns.pdf password password
	qpdf --encrypt $$(cat password) $$(cat password) 128 \
	--print=none --modify=none -- $< $@

output/confidential-report.pdf: final-report/final-NO-SEND-report.pdf password password
	qpdf --encrypt $$(cat password) $$(cat password) 128 \
	--print=none --modify=none -- $< $@

final-report/final-NO-SEND-report.pdf: final-report/final-NO-SEND-report.tex final-report/table.txt
	latexmk -cd $<
	touch $@

final-report/table.txt output/summary.csv: ratings.tsv olypack/produce-scores.py
	cat $< | python olypack/produce-scores.py > $@

output/draft-solns-day1.pdf: $(wildcard source/*.tex) data.yaml password output/authors.tsv olypack/produce-draft.py
	python olypack/produce-draft.py

output/receipt.mkd: data.yaml olypack/produce-receipts.py final-report/final-NO-SEND-report.tex output/summary.csv
	python olypack/produce-receipts.py > $@

output/receipt.html: output/receipt.mkd
	python -m markdown $< > $@