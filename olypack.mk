all: packet report test receipt

packet: output/confidential-probs.pdf output/confidential-solns.pdf
report: output/confidential-report.pdf
test: test/final-probs.pdf test/final-solns.pdf
receipt: output/receipt.html

packet/data-index.tex packet/data-probs.tex packet/data-solns.tex: olypack/produce-packet.py data.yaml $(wildcard source/*.tex)
	mkdir -p output/
	python3 $<

packet/internal-NO-SEND-probs.pdf: packet/internal-NO-SEND-probs.tex \
	packet/data-probs.tex packet/data-index.tex \
	packet/meta.sty packet/instructions.tex packet/reviewers.txt
	latexmk -cd -pdf $<
	touch $@

packet/internal-NO-SEND-solns.pdf: packet/internal-NO-SEND-solns.tex \
	packet/data-probs.tex packet/data-solns.tex \
	packet/meta.sty packet/instructions.tex packet/reviewers.txt
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

final-report/final-NO-SEND-report.pdf: final-report/final-NO-SEND-report.tex final-report-materials
	latexmk -cd -pdf $<
	touch $@

.PHONY: final-report-materials
final-report-materials: olypack/produce-scores.py final-report/table.tex final-report/author-table.tex
	python3 olypack/produce-scores.py

test/final-probs.pdf: test/final-probs.tex test-materials
	latexmk -cd -pdf $<
	touch $@

test/final-solns.pdf: test/final-solns.tex test-materials
	latexmk -cd -pdf $<
	touch $@

.PHONY: test-materials
test-materials: olypack/produce-test.py data.yaml $(wildcard test/problems-*.tex) $(wildcard test/solutions-*.tex)
	python3 $<

output/receipt.mkd: data.yaml olypack/produce-receipts.py final-report/final-NO-SEND-report.tex packet/reviewers.txt
	python3 olypack/produce-receipts.py

output/receipt.html: output/receipt.mkd
	python3 -m markdown $< > $@
