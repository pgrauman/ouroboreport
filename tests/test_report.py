import pandas as pd
import pytest

from pyreport.report import Report
from pyreport.report import Header
from pyreport.report import Paragraph
from pyreport.report import UnorderedList
from pyreport.report import OrderedList

@pytest.fixture
def report():
    return Report()

@pytest.fixture
def content():
    return "content"

class FakeComponent():
    v = 1
    def __eq__(self, other):
        return self.v == other.v

@pytest.fixture
def fake_component():
    return FakeComponent()


def test_get_components(report, fake_component):
    report.components = [fake_component, fake_component]
    assert len(report.get_components()) == 2
    assert report.get_components()[0] == fake_component
    assert report.get_components()[1] == fake_component


def test_add_component(report, fake_component):
    report.add_component(fake_component)
    assert report.get_components()[0] == fake_component


def test_add_reports(report, fake_component):
    report.add_component(fake_component)
    report2 = Report()
    report2.add_component(fake_component)

    combined = report + report2
    assert len(combined.components) == 2
    assert combined.get_components()[0] == fake_component
    assert combined.get_components()[1] == fake_component


def test_add_header1(report, content):
    expected = Header(content, 1)
    report.add_header1(content)
    assert report.get_components()[0] == expected


def test_add_header2(report, content):
    expected = Header(content, 2)
    report.add_header2(content)
    assert report.get_components()[0] == expected


def test_add_header3(report, content):
    expected = Header(content, 3)
    report.add_header3(content)
    assert report.get_components()[0] == expected


def test_add_header4(report, content):
    expected = Header(content, 4)
    report.add_header4(content)
    assert report.get_components()[0] == expected


def test_add_paragraph(report, content):
    expected = Paragraph(content)
    report.add_paragraph(content)
    assert report.get_components()[0] == expected


def test_add_ordered_list(report, content):
    expected = OrderedList([content, content])
    report.add_ordered_list([content, content])
    assert report.get_components()[0] == expected


def test_add_unordered_list(report, content):
    expected = UnorderedList([content, content])
    report.add_unordered_list([content, content])
    assert report.get_components()[0] == expected


def test_add_table(report):
    df = pd.DataFrame([[1,2]])
    report.add_component(df)
    pd.testing.assert_frame_equal(report.get_components()[0], df)
