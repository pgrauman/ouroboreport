import os
import pytest

from pathlib import Path
from ouroboreport.components import Plot
from ouroboreport.renderers import ConfluenceRenderer
from ouroboreport.renderers import MarkdownRenderer
from ouroboreport.renderers import HTMLRenderer


class FakeComponent():
    def to_markdown(self):
        return  "# TEST"

class FakeReport():
    def __init__(self, components):
        self.components = components

    def get_components(self):
        return self.components

    def add_component(self, component):
        self.components.append(component)


@pytest.fixture()
def report():
    return FakeReport([FakeComponent(), FakeComponent()])


def test_markdown_renderer(tmpdir, report):
    p = tmpdir.mkdir("sub").join("test.md")
    MarkdownRenderer().save(report, p)
    assert p.read() == "# TEST\n# TEST"


def test_html_renderer(tmpdir, report):
    p = tmpdir.mkdir("sub").join("test.html")
    HTMLRenderer().save(report, p)
    expected = '<h1 id="test">TEST</h1>\n<h1 id="test-1">TEST</h1>\n'
    assert p.read() == expected


def test_confluence_set_parent():
    renderer = ConfluenceRenderer()
    renderer.set_parent("test")
    assert renderer.parent == "test"


def test_confluence_set_space():
    renderer = ConfluenceRenderer()
    renderer.set_space("TEST")
    assert renderer.space == "TEST"


def test_conlfluence_renderer_to_jira(report):
    renderer = ConfluenceRenderer()
    content = renderer._convert_to_jira_wiki(report)
    expected = "h1. {anchor:test}TEST\nh1. {anchor:test-1}TEST\n"
    assert content == expected


# Not ideal but inherit Plot object and fake methods used by test
class FakePlot(Plot):
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.filepath.touch()

    def get_path(self):
        return self.filepath

    def set_path(self, filepath):
        self.filepath = Path(filepath)


def test_confluence_process_images(tmpdir):
    # setup
    renderer = ConfluenceRenderer()
    src_plot_path = Path(f"{tmpdir}/plot.png")
    plot = FakePlot(src_plot_path)
    report = FakeReport([plot, FakeComponent()])

    # Process
    new_report, images_to_upload = renderer._process_images(report)

    # Check plot handling
    exepected_plot = Path("plot.png")
    assert new_report.components[0].get_path() == exepected_plot
    assert images_to_upload[0][0] == src_plot_path
    assert images_to_upload[0][1] == str(exepected_plot)

    # Check non-plot handling
    assert new_report.components[1].to_markdown() == "# TEST"


def test_html_renderer_move_plots(tmpdir):
    tmpdir = Path(tmpdir)

    # setup report and renderer and directories
    renderer = HTMLRenderer(cp_img_to_path=True)
    src_dir = tmpdir / "src"
    os.mkdir(src_dir)
    dst_dir = tmpdir / "dst"
    os.mkdir(dst_dir)
    plot = FakePlot(src_dir / "test.png")
    report = FakeReport([plot, FakeComponent()])

    new_report = renderer._relocate_image_files(dst_dir / "fake.html", report)

    # Test expectations: 1. plot copies; 2. plot in report has new path;
    #  3. other components untouched
    exepected_plot = dst_dir / "plots" / "test.png"
    assert os.path.exists(exepected_plot)
    assert new_report.components[0].get_path() == exepected_plot
    assert new_report.components[1].to_markdown() == "# TEST"


