import pytest

from data.helpers import LabelTable
from tests.concepts.factories import PeriodFactory

from .factories import DatasetFactory, VariableFactory


@pytest.fixture
def variables(db):
    """ This fixture contains two variables from two datasets from two periods
        they appear in an unsorted order
    """
    d1 = DatasetFactory(name="d1")
    d2 = DatasetFactory(name="d2")
    p1 = PeriodFactory(name="2019")
    p2 = PeriodFactory(name="2018")
    v1 = VariableFactory(name="v1")
    v2 = VariableFactory(name="v2")
    d1.period = p1
    d2.period = p2
    v1.dataset = d1
    v2.dataset = d2
    return [v1, v2]


@pytest.fixture
def label_table(variables):
    """ A label table with the variables from the variables fixture """
    return LabelTable(variables)


class TestLabelTable:
    def test_init_method(self, variables):
        """ The init method of the label table sorts the variables by their datasets periods """
        label_table = LabelTable(variables)
        variables.reverse()
        assert label_table.variables == variables

    def test_init_method_without_period(self, variables):
        """ The first variable has no period in this test """
        variables[0].dataset.period = None
        label_table = LabelTable(variables)
        assert label_table.variables == variables

    def test_to_dict_method(self, mocker, variables):
        label_table = LabelTable(variables)
        mocked_fill_header = mocker.patch.object(LabelTable, "_fill_header")
        mocked_fill_body = mocker.patch.object(LabelTable, "_fill_body")
        label_table_dict = label_table.to_dict()
        mocked_fill_header.assert_called_once()
        mocked_fill_body.assert_called_once()

    def test_to_html_method(self, mocker, variables):
        label_table = LabelTable(variables)
        # label_table_html = label_table.to_html()

    def test_fill_header_method(self, label_table):
        pass

    def test_fill_body_method(self, label_table):
        pass

    def test_get_all_category_labels_method(self, label_table):
        pass

    def test_simplify_label_method(self, label_table):
        label = "some-label"
        output = label_table._simplify_label(label)
        assert output == label

    # TODO: SOEP label
    # TODO: Pairfam label

    def test_simplify_label_method_with_non_string_label(self, label_table):
        label = 1
        output = label_table._simplify_label(label)
        expected = ""
        assert output == expected
