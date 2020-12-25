import datetime
import io
import json
from unittest import TestCase, mock

from django.core.serializers.json import DjangoJSONEncoder

from expenses.utils import prettify


class UtilsTestCase(TestCase):
    def test_prettify(self):
        now = datetime.datetime.now()
        obj = {'a_number': 123, 'a_string': 'foo', 'a_date': now}

        stream = io.StringIO()
        with mock.patch('pprint.pprint') as pprint_mock:
            prettify(obj, stream=stream)
        stream.seek(0)

        pprint_mock.assert_not_called()
        iso_now = now.isoformat()
        iso_now = iso_now[:23] + iso_now[26:]  # DjangoJSONEncoder does this under the hood to match ECMA spec
        expected = {'a_number': 123, 'a_string': 'foo', 'a_date': iso_now}
        self.assertEqual(stream.read(), json.dumps(expected, indent=4, sort_keys=True, cls=DjangoJSONEncoder))
