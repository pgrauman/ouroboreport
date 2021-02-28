"""Report Obect
"""
from datetime import datetime
from pathlib import Path
from pyreport.renderers import ConfluenceRenderer
from pyreport.renderers import MarkdownRenderer
from pyreport.renderers import HTMLRenderer
from pyreport.renderers import PDFRenderer
from pyreport.components import Header
from pyreport.components import Paragraph
from pyreport.components import UnorderedList
from pyreport.components import OrderedList
from pyreport.components import CheckboxList
from pyreport.components import Plot


DEFAULT_TITLE = "Ouroboreport"


class Report():
    """Report
    """
    def __init__(self, title="", author=""):
        self.components = []
        self.author = author

        if not title:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            title = f"{dt} - {DEFAULT_TITLE}"

        self.title = title

    def __add__(self, other):
        """Add to Reports together
        """
        merged_components = self.components + other.components
        new_report = Report()
        new_report.components = merged_components
        return new_report

    def get_components(self):
        """Get list of Report components
        """
        return self.components

    def add_component(self, component):
        """Add component to report
        """
        self.components.append(component)

    def add_header1(self, content):
        """Add header1 to report
        """
        self.add_component(Header(content, 1))

    def add_header2(self, content):
        """Add header2 to report
        """
        self.add_component(Header(content, 2))

    def add_header3(self, content):
        """Add header3 to report
        """
        self.add_component(Header(content, 3))

    def add_header4(self, content):
        """Add header4 to report
        """
        self.add_component(Header(content, 4))

    def add_paragraph(self, content):
        """Add paragraph to report
        """
        self.add_component(Paragraph(content))

    def add_ordered_list(self, content):
        """Add ordered_list to report
        """
        self.add_component(OrderedList(content))

    def add_unordered_list(self, content):
        """Add unordered_list to report
        """
        self.add_component(UnorderedList(content))

    def add_checkbox_list(self, content):
        """Add checkbox list to report
        """
        self.add_component(CheckboxList(content))

    def add_table(self, df):
        """Add table from pandas dataframe to report
        """
        self.add_component(df)

    def add_plot(self, filepath,  title="", alttxt=""):
        """Add plot to report
        """
        self.add_component(Plot(filepath, title=title, alttxt=alttxt))

    def save_markdown(self, destination):
        """Save Report to markdown format
        """
        destination = Path(destination)
        renderer = MarkdownRenderer()
        renderer.save(self, destination)

    def save_html(self, destination, cp_img_to_path=False):
        """Save Report to html format
        """
        destination = Path(destination)
        renderer = HTMLRenderer(cp_img_to_path=cp_img_to_path)
        renderer.save(self, destination)

    def save_pdf(self, destination):
        """Save Report to pdf format
        """
        destination = Path(destination)
        renderer = PDFRenderer()
        renderer.save(self, destination)

    def save_to_confluence(self, space=None, url=None, username=None, token=None, parent=None):
        """Save Report to to_confluence format
        """
        renderer = ConfluenceRenderer(space=space, url=url, username=username,
                                      token=token, parent=parent)
        renderer.save(self)
