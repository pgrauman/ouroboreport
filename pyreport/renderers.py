"""Renderers are the ogic that converts the pyrhon report extractions to intened formats
"""
import os
import tempfile

from abc import ABC
from abc import abstractmethod
from copy import deepcopy
from shutil import copyfile
import pypandoc

from atlassian import Confluence
from pyreport.components import Plot
from pyreport.shared import ifnotexistmkdir



class AbstractRenderer(ABC):
    """Abstract definition of a Renderer
    """
    @abstractmethod
    def save(self):
        """Abstract save method
        """
        return NotImplementedError


class MarkdownRenderer(AbstractRenderer):
    """Renderer that converts report to Markdown
    """
    def save(self, report, dest):
        """Save report to destination
        """
        content = self._render_markdown(report.get_components())
        with open(str(dest), "w") as out:
            out.write(content)

    def _render_markdown(self, components):
        return "\n".join([c.to_markdown() for c in components])


class HTMLRenderer(MarkdownRenderer):
    """Renderer that converts Report to HTML via Markdown
    """
    def __init__(self, cp_img_to_path=False):
        self.cp_img_to_path = cp_img_to_path

    def save(self, report, dest):
        """Save report to destination
        """
        # if `cp_img_to_path` then copy files and update Report object
        if self.cp_img_to_path:
            report = self._relocate_image_files(dest, report)

        content = self._render_markdown(report.get_components())
        content = pypandoc.convert_text(content, "html", "markdown")
        with open(dest, "w") as out:
            out.write(content)

    def _relocate_image_files(self, dest, report):
        # make a copy of report with no component
        out_report = deepcopy(report)
        out_report.components = []

        # Iterate through report components, copy plots to new location
        plots_dir = ifnotexistmkdir(f"{dest.parent}/plots")
        for component in report.get_components():
            if isinstance(component, Plot):
                new_plot = deepcopy(component)
                old_path = component.get_path()
                new_path = plots_dir / os.path.basename(old_path)
                copyfile(old_path, new_path)
                new_plot.set_path(new_path)
                out_report.add_component(new_plot)
            else:
                out_report.add_component(component)
        return out_report


class PDFRenderer():
    """Renderer that converts Report to PDF via Markdown
    """
    def save(self, report, dest):
        """Save report to destination
        """
        with tempfile.TemporaryDirectory() as tmpdirname:
            filepath = f"{tmpdirname}/temp.md"
            MarkdownRenderer().save(report, filepath)
            pypandoc.convert_file(filepath, "pdf", outputfile=dest)


class ConfluenceAPIError(Exception):
    pass


class ConfluenceRenderer(MarkdownRenderer):
    """Render report to comfluence via the atlassian API
    """
    def __init__(self, space="", url="", username="", token="", parent=None):
        self.parent = parent
        self.space = space

        # if not all([space, url, username, token]):
        #     raise ConfluenceAPIError("Must assigne a space, url, unername and token") 

        # Define atlassian api connection
        self.conn = Confluence(url=url, username=username,
                               password=token, cloud=True)

    def set_parent(self, parent):
        """Set id of parent to write conluence page to
        """
        self.parent = parent

    def set_space(self, space):
        """Set id of space to write conluence page to
        """
        self.space = space

    def save(self, report):
        """Save report to Confluence
        """
        # report must have title, check that it's unique?

        content = self._convert_to_jira_wiki(report)
        self.conn.create_page(self.space, report.title, content, type="page", representation="wiki")

    def _test_connection(self):
        """Test initialized confluence connection
        """

    def _test_space_page_exists(self):
        """Test initialized confluence connection
        """


    def _convert_to_jira_wiki(self, report):
        content = self._render_markdown(report.get_components())
        content = pypandoc.convert_text(content, "jira", "markdown")
        return content
