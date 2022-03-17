import os
import mock

os.environ["WEBMON_CONFIG_FILE"] = 'app/config.yaml'
import consumer
from checkentry import CheckEntry

ENTRY_RESPONSE_TIME = 239
ENTRY_WEBSITE_ID = 'b3b20096-a32c-11eb-8d4f-163fd67fbf69'

class MockMessage:
    def __init__(self):
        self.value = (
          "http_status: 200\n"
          "id: 47a73524-a336-11eb-9ee1-acde48001122\n"
          "regex: adp_regex\n"
          "regex_match: true\n"
          "response_time: 239\n"
          "timestamp: 2021-04-22 02:45:09.063430\n"
          "website_id: b3b20096-a32c-11eb-8d4f-163fd67fbf69\n"
        )

@mock.patch.object(CheckEntry, 'save')
def test_processMessage(mock_save):
    entry = consumer.processMessage(MockMessage())
    assert entry
    assert entry.website_id == ENTRY_WEBSITE_ID
    assert entry.response_time == ENTRY_RESPONSE_TIME
