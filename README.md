# DBLP to FWF report

Convert your DBLP-listed publications (or from a local .bib file) into a format suitable for inclusion into an [FWF](https://fwf.ac.at) report. Call like

	python3 dblp2fwf.py <your-DBLP-id>

with your [DBLP id](https://blog.dblp.org/2020/08/18/new-dblp-url-scheme-and-api-changes/). For instance, I would do
	
	python3 dblp2fwf.py 181/3386

because my [DBLP entry](https://dblp.org/pid/181/3386.html) is `https://dblp.org/pid/181/3386.html`.
Don't forget to double-check and clean the output, it will be necessary.
See `python3 dblp2fwf.py -h` for a few more options, in particular filtering based on date of publication.

## Dependencies

You need to install [PyBTeX](https://pybtex.org/), with `pip install pybtex`, and Python 3.6+.
