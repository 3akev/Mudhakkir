import json
import os
from unittest.mock import MagicMock

import pytest

from deprecated.dep_tadhkeer_backend import TadhkeerBackend
from statics import parentDir
from util.embed import is_embed_valid


@pytest.fixture
def td():
    t = TadhkeerBackend()
    t.client_session = MagicMock()
    yield t


def test_process_response_returns_two_correct_embeds(td):

    for i in range(1, 4):
        file = os.path.join(parentDir, 'tests/test_resources/quran_resp{0}.json'.format(i))
        with open(file, 'r') as f:
            resp = json.loads(f.read())

        ar_embed, en_embed = td._process_response(resp)
        assert is_embed_valid(ar_embed)
        assert is_embed_valid(en_embed)


def test_get_quran_link_formats_quran_link_according_to_api(td):
    test_table = {
        (2, 4, 6): 'http://api.alquran.cloud/surah/2/editions/ar,en.sahih?offset=3&limit=3',
        (15, 9, None): 'http://api.alquran.cloud/surah/15/editions/ar,en.sahih?offset=8&limit=1',
        (114, 2, 5): 'http://api.alquran.cloud/surah/114/editions/ar,en.sahih?offset=1&limit=4'
    }
    for args, result in test_table.items():
        assert td._get_quran_link(*args) == result
