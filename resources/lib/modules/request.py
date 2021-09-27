import requests


class Request:
    def __init__(self, base: str):
        self.base = base

    def get(self, page: str):
        page = self.base + page if self.base not in page else page
        return requests.request('GET', page)
