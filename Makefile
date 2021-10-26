all: packet
	
packet: output/confidential-probs.pdf output/confidential-solns.pdf
report: output/confidential-report.pdf

tex/data-index.tex tex/data-probs.tex tex/data-solns.tex: scripts/assemble.py input/data.yaml $(wildcard source/*.tex)
	python3 $<

tex/internal-NO-SEND-probs.pdf: tex/internal-NO-SEND-probs.tex \
	tex/data-probs.tex tex/data-index.tex \
	tex/meta.sty tex/instructions.tex tex/names.txt tex/assign.txt
	latexmk -cd $<

tex/internal-NO-SEND-solns.pdf: tex/internal-NO-SEND-solns.tex \
	tex/data-probs.tex tex/data-solns.tex \
	tex/meta.sty tex/instructions.tex tex/names.txt tex/assign.txt
	latexmk -cd $<

output/confidential-probs.pdf: tex/internal-NO-SEND-probs.pdf input/password input/password
	qpdf --encrypt $$(cat input/password) $$(cat input/password) 128 \
	--print=none --modify=none -- $< $@

output/confidential-solns.pdf: tex/internal-NO-SEND-solns.pdf input/password input/password
	qpdf --encrypt $$(cat input/password) $$(cat input/password) 128 \
	--print=none --modify=none -- $< $@

output/confidential-report.pdf: final-report/final-NO-SEND-report.pdf input/password input/password
	qpdf --encrypt $$(cat input/password) $$(cat input/password) 128 \
	--print=none --modify=none -- $< $@

final-report/final-NO-SEND-report.pdf: final-report/final-NO-SEND-report.tex final-report/table.txt
	latexmk -cd $<

final-report/table.txt: input/ratings.tsv scripts/make-table-twn.py 
	cat $< | python scripts/make-table-twn.py > $@
