"""Components to comprise a report
"""

from abc import ABC
from abc import abstractmethod
from pathlib import Path


class AbstractComponent(ABC):
    """Abstract Component
    """
    @abstractmethod
    def to_html(self):
        """Convert content to html format
        """
        return NotImplementedError

    @abstractmethod
    def to_markdown(self):
        """Convert content to markdown format
        """
        return NotImplementedError

class Component(AbstractComponent):
    """Concrete Component
    """
    content = ""

    def __eq__(self, other):
        """Test compoent equality
        """
        return self.content == other.content


class Header(Component):
    """Header Component
    """
    def __init__(self, content, level=1):
        self.content = content
        self.level = level

    def to_html(self):
        """Convert content to html format
        """
        return f"<h{self.level}>{self.content}</h{self.level}>"

    def to_markdown(self):
        """Convert content to markdown format
        """
        prefix = "#" * self.level
        return f"{prefix} {self.content}"


class Paragraph(Component):
    """Paragraph Component
    """
    def __init__(self, content):
        self.content = content

    def to_html(self):
        """Convert content to html format
        """
        return f"<p>{self.content}</p>"

    def to_markdown(self):
        """Convert content to markdown format
        """
        return f"{self.content}\n"


class UnorderedList(Component):
    """Unordered list component
    """
    top_html_tag = "<ul>"
    bottom_html_tag = "</ul>"
    item_open_html_tag = "<li>"
    item_close_html_tag = "</li>"
    md_prefix = "* "
    def __init__(self, content):
        self.content = content

    def __eq__(self, other):
        """Test compoent equality
        """
        samelen = len(self.content) == len(other.content)
        if not samelen:
            return False
        return all(a == b for a, b in zip(self.content, other.content))

    def to_html(self):
        """Convert content to html format
        """
        html = self.top_html_tag + "\n"
        for item in self.content:
            html += f"{self.item_open_html_tag}{str(item)}{self.item_close_html_tag}\n"
        html += self.bottom_html_tag
        return html

    def to_markdown(self):
        """Convert content to markdown format
        """
        return "\n".join([f"{self.md_prefix}{str(c)}" for c in self.content])


class OrderedList(UnorderedList):
    """Order list component
    """
    top_html_tag = "<ol>"
    bottom_html_tag = "</ol>"
    def to_markdown(self):
        """Convert content to markdown format
        """
        return "\n".join([f"{i+1}. {str(c)}" for i, c in enumerate(self.content)])


class CheckboxList(UnorderedList):
    """Checkbox list component
    """
    top_html_tag = '<ul class="task-list">'
    bottom_html_tag = "</ul>"
    item_open_html_tag = '<li><input type="checkbox" disabled="" />\n'
    item_close_html_tag = "</li>"
    md_prefix = "- [ ] "


class Plot(Component):
    """Plot component
    """
    def __init__(self, filepath, title="", alttxt=""):
        self.filepath = Path(filepath)
        self.title = title
        self.alttxt  = alttxt
        self.content = "|".join([filepath, title, alttxt])

    def set_path(self, filepath):
        """Set path for Plot object
        """
        self.filepath = Path(filepath)

    def get_path(self):
        """Get path from Plot object
        """
        return self.filepath

    def to_html(self):
        """Convert content to html format
        """
        return f'<p><img href="{self.filepath}" title="{self.title}">{self.alttxt}</img></p>'

    def to_markdown(self):
        """Convert content to markdown format
        """
        return f'[{self.alttxt}]({self.filepath} "{self.title}")'
