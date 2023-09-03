import os
import json
import requests
import time
import logging


class Timer:
    def start(self):
        self.start_time = time.time()

    def end(self):
        self.end_time = time.time()

    def _diff(self):
        if hasattr(self, "start_time") and hasattr(self, "end_time"):
            return self.end_time - self.start_time
        else:
            raise ValueError("Timer not started or ended")

    def diff(self):
        total_seconds = self._diff()

        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)

        return minutes, seconds


class Page(object):
    def __init__(self, url: str, params: dict = None):
        self.url = url
        self.params = params or {}

    def set_params(self, params: dict):
        self.params.update(params)

    def get_param(self, key: str, default=None):
        return self.params.get(key, default)

    def get_url(self) -> str:
        params = []
        for key, value in self.params.items():
            if value:
                params.append(f"{key}={value}")

        return self.url.format("&".join(params))


class Request(object):
    def __init__(self, page: Page):
        self.page = page

    def get(self):
        try:
            response = requests.get(self.page.get_url())
            response.raise_for_status()
            return response.text
        except Exception as e:
            logging.error(f"Error requesting page: {self.page.get_url()} - {str(e)}")
            raise e


class JsonFile(object):
    def __init__(self, folder: str, filename: str):
        self.folder = folder
        self.filename = filename

    @property
    def filepath(self):
        return os.path.join(self.folder, self.filename)

    def write(self, data: dict):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=4)

    def read(self):
        with open(self.filepath, "r") as f:
            return json.load(f)


class HtmlFile(object):
    def __init__(self, folder: str, filename: str):
        self.folder = folder
        self.filename = filename

    @property
    def filepath(self):
        return os.path.join(self.folder, self.filename)

    def write(self, html: str):
        with open(self.filepath, "w") as f:
            f.write(html)

    def read(self):
        with open(self.filepath, "r") as f:
            return f.read()


class Folder(object):
    def __init__(self, folder: str):
        self.folder = folder

    def create(self):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def clear(self):
        for filename in os.listdir(self.folder):
            filepath = os.path.join(self.folder, filename)
            os.remove(filepath)
