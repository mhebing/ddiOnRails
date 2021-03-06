import pytest
from django.urls import resolve, reverse

pytestmark = [pytest.mark.concepts, pytest.mark.urlconf]


@pytest.fixture
def concept_list_url(scope="module"):
    return "concepts:concept_list"


@pytest.fixture
def concept_detail_url_by_id(scope="module"):
    return "concepts:concept_detail"


@pytest.fixture
def concept_detail_url_by_name(scope="module"):
    return "concepts:concept_detail_name"


class TestConceptUrls:
    def test_concept_list_url(self, concept_list_url):
        url = reverse(concept_list_url)
        assert resolve(url).view_name == concept_list_url

    def test_concept_detail_url_with_pk(self, concept_detail_url_by_id):
        url = reverse(concept_detail_url_by_id, kwargs={"pk": 1})
        assert resolve(url).view_name == concept_detail_url_by_id

    def test_concept_detail_url_with_name(self, concept_detail_url_by_name):
        url = reverse(concept_detail_url_by_name, kwargs={"concept_name": "some-concept"})
        assert resolve(url).view_name == concept_detail_url_by_name
