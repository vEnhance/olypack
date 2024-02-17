all: packet

packet: output/confidential-probs.pdf output/confidential-solns.pdf output/authors.tsv
report: output/confidential-report.pdf
draft: output/draft-solns-day1.pdf
receipt: output/receipt.html

output/authors.tsv packet/data-index.tex packet/data-probs.tex packet/data-solns.tex: olypack/produce-packet.py data.yaml $(wildcard source/*.tex)
	mkdir -p output/
	python3 $<

packet/internal-NO-SEND-probs.pdf: packet/internal-NO-SEND-probs.tex \
	packet/data-probs.tex packet/data-index.tex \
	packet/meta.sty packet/instructions.tex packet/names.txt
	latexmk -cd -pdf $<
	touch $@

packet/internal-NO-SEND-solns.pdf: packet/internal-NO-SEND-solns.tex \
	packet/data-probs.tex packet/data-solns.tex \
	packet/meta.sty packet/instructions.tex packet/names.txt
	latexmk -cd -pdf $<
	touch $@

output/confidential-probs.pdf: packet/internal-NO-SEND-probs.pdf password password
	qpdf --encrypt $$(cat password) $$(cat password) 256 \
	--print=none --modify=none -- $< $@

output/confidential-solns.pdf: packet/internal-NO-SEND-solns.pdf password password
	qpdf --encrypt $$(cat password) $$(cat password) 256 \
	--print=none --modify=none -- $< $@

output/confidential-report.pdf: final-report/final-NO-SEND-report.pdf password password
	qpdf --encrypt $$(cat password) $$(cat password) 256 \
	--print=none --modify=none -- $< $@

final-report/final-NO-SEND-report.pdf: final-report/final-NO-SEND-report.tex final-report/table.txt
	latexmk -cd -pdf $<
	touch $@

final-report/table.txt output/summary.csv: ratings.tsv olypack/produce-scores.py
	python3 olypack/produce-scores.py

output/draft-solns-day1.pdf: $(wildcard source/*.tex) data.yaml password output/authors.tsv olypack/produce-draft.py
	python3 olypack/produce-draft.py

output/receipt.mkd: data.yaml olypack/produce-receipts.py final-report/final-NO-SEND-report.tex output/summary.csv packet/names.txt
	python3 olypack/produce-receipts.py > $@

output/receipt.html: output/receipt.mkd
	python3 -m markdown $< > $@
