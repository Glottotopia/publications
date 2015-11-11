#! /usr/bin/bash

pdftk A=master.pdf  cat A2-2 output frontmatter.pdf
pdftk A=master.pdf  cat A3-4 output toc.pdf
pdftk A=master.pdf  cat A5-7 output contributors.pdf
pdftk A=master.pdf  cat A8-8 output acknowledgments.pdf
pdftk A=master.pdf  cat A10-40 output good.pdf 
pdftk A=master.pdf  cat A41-70 output nordhoff.pdf
pdftk A=master.pdf  cat A71-85 output musgrave.pdf
pdftk A=master.pdf  cat A86-109 output baraby.pdf
pdftk A=master.pdf  cat A111-136 output black.pdf
pdftk A=master.pdf  cat A137-167 output bouda.pdf
pdftk A=master.pdf  cat A168-186 output drude.pdf
pdftk A=master.pdf  cat A187-214 output bender.pdf 
pdftk A=master.pdf  cat A215-242 output maxwell.pdf
pdftk A=master.pdf  cat A243-258 output mosel.pdf
pdftk A=master.pdf  cat A259-261 output appendix.pdf
