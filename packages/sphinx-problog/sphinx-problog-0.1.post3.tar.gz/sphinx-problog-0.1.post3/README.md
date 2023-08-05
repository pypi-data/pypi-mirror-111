[![Licence][licence-badge]][licence-link]
[![Python][python-badge]][python-link]
[![PyPI][pypi-badge]][pypi-link]
[![Documentation][doc-badge]][doc-link]

[licence-badge]: https://img.shields.io/github/license/simply-logical/sphinx-problog.svg
[licence-link]: https://github.com/simply-logical/sphinx-problog/blob/master/LICENCE
[python-badge]: https://img.shields.io/badge/python-3.5-blue.svg
[python-link]: https://github.com/simply-logical/sphinx-problog
[pypi-badge]: https://img.shields.io/pypi/v/sphinx-problog.svg
[pypi-link]: https://pypi.org/project/sphinx-problog
[doc-badge]: https://img.shields.io/badge/read-documentation-blue.svg
[doc-link]: https://github.com/simply-logical/sphinx-problog#readme

# :orange_book: ProbLog extension for Jupyter Book (and Sphinx) #

This repository holds a [ProbLog] extensions for [Sphinx], designed to be used
with the [Jupyter Book] platform.
It implements **interactive [ProbLog] code blocks** that can be executed
directly in the browser via [ProbLog API].

**This readme file holds a technical documentation of the `sphinx-problog`
extension.
For a [Jupyter Book] usage example of interactive [ProbLog] code boxes visit
the [ProbLog template] and its source hosted in the
[simply-logical/problog-book-template] GitHub repository.**

> This *readme* file uses [Jupyter Book]'s [MyST Markdown] syntax for **roles**
  and **directives** -- see [MyST overview] for more details.
  For use with [Sphinx], please refer to the [reStructuredText] syntax.

## :snake: Installing `sphinx-problog` ##

To get started with `sphinx-problog`, first install it via `pip`:
```bash
pip install sphinx-problog
```
then, add the `problog` module of the `sphinx_problog` extension to the Sphinx
`extensions` list in your `conf.py`
```Python
...
extensions = ['sphinx_problog.problog']
...
```

## :chart_with_upwards_trend: ProbLog directive ##

The [`sphinx_problog.problog`](sphinx_problog/problog.py) module defines the
`problog` directive, which is used for building
*interactive [ProbLog] code boxes* executed directly in the browser.

### Usage ###

A *[ProbLog] code box* is included with the `problog` directive:

````text
```{problog} problog:1.2.3
optional :- content.
```
````

Each [ProbLog] code box can be referenced with its name using the `ref`
role, e.g., `` {ref}`problog:1.2.3` ``, which produces *ProbLog code box*
hyper-link.

### Configuration parameters ###

The `problog` extension uses the following [Sphinx] configuration parameters:

* `sphinx_problog_code_directory` (**required** when loading the box content
  from a file) -- defines the path to a directory holding files with content
  ([ProbLog] code) of each [ProbLog] code box; and
* `sphinx_problog_execution_server_url` (**optional**) -- specifies the URL of
  the [ProbLog] execution server ([ProbLog API],
  <https://verne.cs.kuleuven.be/problog/api/> by default, which is hard-coded
  in the [ProbLog] JavaScript [`problog_editor_advanced.js`]).

### Arguments, parameters and content ###

Each [ProbLog] code box has one **required** argument that
specifies the *unique* id of this particular interactive code block.
This id **must** start with the `problog:` prefix.
The content of a [ProbLog] box can **either** be provided explicitly within the
directive, **or** -- when the content is left empty -- it is pulled from a code
file whose name is derived from the code box id, and which should be located in
the directory specified via the `sphinx_problog_code_directory` configuration
parameter.
The code file name is expected to be the code block id **without** the
`problog:` prefix and **with** the `.pl` extension.
For example, for a code block with `problog:my_code` id, the code file should
be named `my_code.pl`.
The `problog` [Sphinx] extension *monitors* the code files for
changes and automatically regenerates the affected pages.

---

> The CSS and JS files used by this [Sphinx] extension (namely
  [`sphinx-problog.css`], [`mode-problog.js`] and
  [`problog_editor_advanced.js`], as well as their CDN-pulled dependencies
  [`ace.js`](https://github.com/ajaxorg/ace),
  [`jquery.min.js`](https://github.com/jquery/jquery),
  [`jquery-ui.min.js`](https://github.com/jquery/jquery-ui) and
  [`md5.js`](https://github.com/brix/crypto-js))
  can be found in the [`sphinx_problog/_static`](sphinx_problog/_static)
  directory of this repository.

[sphinx]: https://www.sphinx-doc.org/
[jupyter book]: https://jupyterbook.org/
[problog]: https://dtai.cs.kuleuven.be/problog/
[problog api]: https://verne.cs.kuleuven.be/problog/api/
[myst markdown]: https://myst-parser.readthedocs.io/
[myst overview]: https://jupyterbook.org/content/myst.html
[reStructuredText]: https://docutils.sourceforge.io/rst.html
[problog template]: https://problog-template.simply-logical.space/src/text/bayesian_networks-sp-mnb.html
[simply-logical/problog-book-template]: https://github.com/simply-logical/problog-book-template/blob/master/src/text/bayesian_networks-sp-mnb.md
[`sphinx-problog.css`]: sphinx_problog/_static/sphinx-problog.css
[`mode-problog.js`]: sphinx_problog/_static/mode-problog.js
[`problog_editor_advanced.js`]: sphinx_problog/_static/problog_editor_advanced.js
