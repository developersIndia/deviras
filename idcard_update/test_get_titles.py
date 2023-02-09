import unittest
from unittest.mock import patch
from main import get_titles

# patch out the environ dictionary
# used to instantiate global variables in the titles_updater script
# maybe move the call to os.environ in the script to the update_titles method?
environ_patcher = patch.dict('os.environ', {
    'REDDIT_CLIENT_ID': '',
    'REDDIT_CLIENT_SECRET': '',
    'REDDIT_PASSWORD': ''
})
environ_patcher.start()

class TestGetTitles(unittest.TestCase):
    @patch('main.json.load', return_value={'titles': ['foo', 'bar', 'baz']})
    def test_get_titles_returns_a_list(self, _):
        titles = get_titles()
        self.assertIsInstance(titles, list)

    @patch('main.json.load', return_value={'titles': ['foo', 'bar', 'baz']})
    def test_get_titles_contains_titles_from_dataset_file(self, mock_json_load):
        titles = get_titles()

        self.assertTrue(all(map(lambda title: title in mock_json_load.return_value['titles'], titles)))

environ_patcher.stop()
