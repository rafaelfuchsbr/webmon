import os, sys
import mock, responses

os.environ["WEBMON_CONFIG_FILE"] = 'app/config.yaml'

from website import Website

WEBSITE_TEST_ID = '12345678-1234-1234-1234-123456789012'
WEBSITE_TEST_NAME = 'test_name'
WEBSITE_TEST_URL = 'http://test_url.com'
WEBSITE_TEST_URL_404 = 'http://test_url.com/404.html'
WEBSITE_TEST_REGEX = 'test_regex'
WEBSITE_TEST_STATUS = 'test_status'
WEBSITE_TEST_TIMESTAMP = '123456789'

def getWebsite(msg=''):
  website = Website()
  website.id=WEBSITE_TEST_ID
  website.name=WEBSITE_TEST_NAME
  website.url=WEBSITE_TEST_URL
  website.regex=WEBSITE_TEST_REGEX
  website.status=WEBSITE_TEST_STATUS
  website.timestamp=WEBSITE_TEST_TIMESTAMP
  return website

@responses.activate
@mock.patch.object(Website, 'save')
def test_getCurrentAvailability_200(mock_save):
    mock_save.return_value = True
    responses.add(responses.GET, WEBSITE_TEST_URL,status=200)
    website = getWebsite()
    entry = website.getCurrentAvailability()
    assert entry.http_status == 200

@responses.activate
@mock.patch.object(Website, 'save')
def test_getCurrentAvailability_404(mock_save):
    mock_save.return_value = True
    responses.add(responses.GET, WEBSITE_TEST_URL_404,status=404)
    website = getWebsite()
    website.url=WEBSITE_TEST_URL_404
    entry = website.getCurrentAvailability()
    assert entry.http_status == 404

@mock.patch.object(Website, 'save')
def test_save(mock_save):
    mock_save.return_value = True
    website = getWebsite()
    website.save()
    assert website.id == WEBSITE_TEST_ID