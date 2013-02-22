texlive
texlive-latex-recommended
texlive-latex-extra


pandoc -N --template=mytemplate.tex -V title-meta="anwenzhi" -V author-meta="anwen team" -V subject-meta="essay novel" -V keywords-meta="cheate share" -V mainfont="WenQuanYi Micro Hei" -V fontsize=16pt -V version=0.1 anwen_z_1.md --latex-engine=xelatex --toc -o anwen_z_1.pdf
