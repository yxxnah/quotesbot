class MyCustomDownloaderMiddleware(object):
  
    def process_request(self, request, spider):
        request._url = request.url.replace("%20", "-", 2)