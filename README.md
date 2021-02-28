# README.md

# Ouroboreport

Ouroboreport is a package for writing simple reports in line with your analysis code, then publishing it to whatever format you need. Adding content to the report is simple and the details of typesetting and format conversion is done for you.

# Installation

While in development, this package is not on pypi. To use it early install via poetry to your environment of choice

```bash
# <activate python environment....>
cd ouroboreport/
poetry install
```
Note the dependencies in `pyproject.toml` are likely overly strict. I haven't yet checked comptibility with older dependencies. Feel free to modfy the versions as needed and feel free to report back :) 

# Basic Usage

```python
import pandas as pd
from ouroboreport.report import Report

report = Report(title="Example Report")

# Some basic text stuff
report.add_header1("Background")
report.add_paragraph("This is a paragraph and it is very important that we read it")
report.add_checkbox_list(["thing to do 1", "thing to do 1"])

# Data tables from pandas dataframes
report.add_header1("Data Table")
report.add_table(data_df)

# Dynamically produce subsections and plots in a loop
report.add_header1("Scatter Plots")
for category, sub_df in data_df.groupby("category"):
	report.add_header2(category)
	plot_path = function_that_makes_plot(sub_df)
	report.add_plot(plot_path, title=f"{category} scatter")

# Save to Markdown
report.save_markdown("report.md")

# Save to HTML
report.save_html("report.html")

# Save to Confluence
report.save_confluence(space="TEAM",
                       url="https://mcfakeface.atlassian.net",
                       username="fake@mcfakeface.net",
                       token=atalssian_api_token,
                       parent="123454321")
```

## Confluence

Conluence functionality is one of my main goals here since its a pain to navigate. `Report.save_confluence` will handle all the plot and content upload for you.

To generate a confluence token checkout this [page](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/)

# Dependencies

Most of the rendering options rely on external software you will want to install to get the most of Ouroboreport:

- [Pandoc](https://pandoc.org/) (distributed via pip wheels with pypandoc in x86 Mac and Windows)
- PDFLatex (for latex and pdf rendering)
    - [Mactex](https://www.tug.org/mactex/) (🍎)
    - [Texlive-core](https://anaconda.org/conda-forge/texlive-core) (🐧)

# Why another reporting framework?

There already are great software packages for writing reports and documentation: [Sphinx](https://www.sphinx-doc.org/en/master/), [Knitr](https://www.rdocumentation.org/packages/knitr/versions/1.30), [Pandoc](https://pandoc.org/) (and [pypandoc](https://pypi.org/project/pypandoc/) on which I lean here). My goal here is not to create a competitively deep package, but rather to create a pythonic framework for writing and publishing simple reports decoupled from the details of formatting. I hope that providing simple python abstractions and hiding the messy formatting details to make it easier to write reports in line with analyses.

# Contributing

TBD

# License

MIT