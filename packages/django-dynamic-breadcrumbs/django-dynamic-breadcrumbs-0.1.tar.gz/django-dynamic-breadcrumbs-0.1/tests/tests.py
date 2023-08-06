from django.test import TestCase, override_settings

from dynamic_breadcrumbs.utils import Breadcrumbs, BreadcrumbsItem
from tests.models import Continent, Country, City

@override_settings(ROOT_URLCONF='tests.urls')
class GenericModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Continent.objects.create(
            name="America", slug="america")
        Country.objects.create(
            name="República Oriental del Uruguay", slug="republica-oriental-uruguay")
        City.objects.create(
            name="Montevideo", slug="monte-vidi-eu")


class BreadcrumbsTests(GenericModelTestCase):

    def setUp(self):
        pass

    def test_split_path_ending_in_slash(self):
        path = "/scale/minor-scale/"
        expected_result = ['scale', 'minor-scale']
        breadcrumbs = Breadcrumbs()

        paths = breadcrumbs._split_path(path=path)

        self.assertEqual(paths, expected_result)

    def test_split_path_ending_in_char(self):
        path = "/scale/minor-scale/c"
        expected_result = ["scale", "minor-scale", "c"]
        breadcrumbs = Breadcrumbs()

        paths = breadcrumbs._split_path(path=path)

        self.assertEqual(paths, expected_result)

    def test_process_all_paths(self):
        base_url = "https://example.com"
        path = "/scale/minor-scale/c"
        breadcrumbs = Breadcrumbs(base_url=base_url, path=path)

        result = breadcrumbs.get_items()

        self.assertEqual(len(result), 3)

    def test_as_list(self):
        path = "/continent/some-continent/"
        breadcrumbs = Breadcrumbs(path=path)

        result = breadcrumbs.as_list()

        self.assertEqual(result[0]['name'], 'continent')
        self.assertEqual(result[0]['resolved'], True)
        self.assertEqual(result[1]['name'], 'some-continent')
        self.assertEqual(result[1]['resolved'], True)

class BreadcrumbsItemTests(GenericModelTestCase):

    def test_get_resolved_url_metadata_resolves_valid_path(self):
        item = BreadcrumbsItem(
            name_raw="some-continent",
            path = "/continent/some-continent/",
            position=2
        )

        result = item._get_resolved_url_metadata()

        self.assertEqual(result, True)

    def test_get_resolved_url_metadata_resolves_valid_path(self):
        item = BreadcrumbsItem(
            name_raw="some-continent",
            path = "/continent/some-continent/",
            position=2
        )

        result = item._get_resolved_url_metadata()

        self.assertTrue(result)

    def test_get_resolved_url_metadata_not_resolves_invalid_path(self):
        item = BreadcrumbsItem(
            name_raw="some-continent",
            path = "/conti/some-continent/",
            position=2
        )

        result = item._get_resolved_url_metadata()

        self.assertFalse(result)
        
