class ForceUTF8Response(object):
    """A downloader middleware to force UTF-8 encoding for all responses."""
    encoding = 'utf-8'

    def process_response(self, request, response, spider):
        # Note: Use response.body_as_unicode() instead of response.text in in Scrapy <1.0.
        new_body = response.text.encode(self.encoding)
        return response.replace(body=new_body, encoding=self.encoding)