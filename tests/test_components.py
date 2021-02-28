import pytest

from pathlib import Path
from ouroboreport.components import Header
from ouroboreport.components import Paragraph
from ouroboreport.components import UnorderedList
from ouroboreport.components import OrderedList
from ouroboreport.components import CheckboxList
from ouroboreport.components import Plot

@pytest.fixture
def header(request):
    return Header("Head", level=request.param)

@pytest.fixture
def paragraph(request):
    return Paragraph("PPP")

@pytest.fixture
def ul(request):
    return UnorderedList(["item1", "item2"])

@pytest.fixture
def ol(request):
    return OrderedList(["item1", "item2"])

@pytest.fixture
def cbl(request):
    return CheckboxList(["item1", "item2"])

@pytest.fixture
def plot(request):
    return Plot("test.png", title="title", alttxt="alt")


def test_component_eq(paragraph):
    other = Paragraph("PPP")
    assert paragraph == other
    other = Paragraph("PPPP")
    assert paragraph != other


def test_list_component_eq(ul):
    other = UnorderedList(["item1", "item2"])
    assert ul == other
    other = UnorderedList(["item1", "item3"])
    assert ul != other
    other = UnorderedList(["item1"])
    assert ul != other


@pytest.mark.parametrize("header, expected",
    [(1, "# Head"), (2, "## Head"), (3, "### Head")],
    indirect=["header"])
def test_header_to_markdown(header, expected):
    assert header.to_markdown() == expected


@pytest.mark.parametrize("header, expected",
    [(1, "<h1>Head</h1>"), (2, "<h2>Head</h2>"),
    (3, "<h3>Head</h3>")],
    indirect=["header"])
def test_header_to_html(header, expected):
    assert header.to_html() == expected


def test_paragraph_to_html(paragraph):
    assert paragraph.to_html() == "<p>PPP</p>"


def test_paragraph_to_markdown(paragraph):
    assert paragraph.to_markdown() == "PPP\n"


def test_unordered_list_html(ul):
    list_string = "<ul>\n<li>item1</li>\n<li>item2</li>\n</ul>"
    assert ul.to_html() == list_string


def test_unordered_list_markdown(ul):
    list_string = "* item1\n* item2\n"
    assert ul.to_markdown() == list_string


def test_ordered_list_html(ol):
    list_string = "<ol>\n<li>item1</li>\n<li>item2</li>\n</ol>"
    assert ol.to_html() == list_string


def test_checkbox_list_to_mardown(cbl):
    list_string = "- [ ] item1\n- [ ] item2\n"
    assert cbl.to_markdown() == list_string


def test_checkbox_list_to_html(cbl):
    list_string = ('<ul class="task-list">\n<li><input type="checkbox" ''disabled="" />\n'
                   'item1</li>\n<li><input type="checkbox" disabled="" />\nitem2</li>\n</ul>')
    assert cbl.to_html() == list_string


def test_plot_set_path(plot):
    new_path = "new_plot_path.png"
    plot.set_path(new_path)
    assert plot.filepath == Path(new_path)


def test_plot_get_path(plot):
    assert plot.filepath == Path("test.png")


def test_plot_to_markdown(plot):
    expected = '![alt](test.png "title")'
    assert plot.to_markdown() == expected


def test_plot_to_html(plot):
    expected = '<p><img href="test.png" title="title">alt</img></p>'
    assert plot.to_html() == expected
