from tornado.httpclient import HTTPClient
from tornado.httpclient import AsyncHTTPClient


def synchronous_fetch(url):
    http_client = HTTPClient()
    response = http_client.fetch(url)

    return response.body


def synchronous_fetch_callback(url, callback):
    http_client = AsyncHTTPClient()

    def handle_response(response):
        callback(response.body)
        http_client.fetch()

    return response.body

if __name__ == "__main__":
    html_body = synchronous_fetch('http://127.0.0.1:9000/')
    print(html_body)
