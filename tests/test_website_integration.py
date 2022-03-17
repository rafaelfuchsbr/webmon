import os
os.environ["WEBMON_CONFIG_FILE"] = 'app/config.yaml'

from website import Website

WEBSITE_TEST_ID = '12345678-1234-1234-1234-123456789012'
WEBSITE_TEST_NAME = 'test_name'
WEBSITE_TEST_URL = 'test_url'
WEBSITE_TEST_REGEX = 'test_regex'
WEBSITE_TEST_STATUS = 'test_status'
WEBSITE_TEST_TIMESTAMP = '123456789'

def getWebsite():
  website = Website()
  website.id=WEBSITE_TEST_ID
  website.name=WEBSITE_TEST_NAME
  website.url=WEBSITE_TEST_URL
  website.regex=WEBSITE_TEST_REGEX
  website.status=WEBSITE_TEST_STATUS
  website.timestamp=WEBSITE_TEST_TIMESTAMP
  return website

# def test_save_load_delete():
#     website = getWebsite()
#     website.id = None
#     website.save()
#     assert website.id != WEBSITE_TEST_ID
#     website2 = Website(id=website.id)
#     assert website.id == website2.id
#     website.name = "My new name"
#     website.save()
#     assert website.name != WEBSITE_TEST_NAME
#     website.delete()
#     assert not bool(website.__dict__)
