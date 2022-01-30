SOURCEDIR     = .
BUILDDIR      = _build
HTMLDIR       = _build/html

.PHONY: html clean

html:
	sphinx-build -W -T -b html "$(SOURCEDIR)" "$(HTMLDIR)"

clean:
	rm -rf "$(BUILDDIR)"
	rm -rf "$(APIDOCDIR)"
