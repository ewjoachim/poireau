import os

from django.conf import settings
from django.utils import translation

from dropbox.client import DropboxClient

from .xml_song import FoundSong


class Explorer(object):
    def __init__(self, base_folder):
        self.base_folder = base_folder

    def walk(self, folder):
        raise NotImplementedError()

    def get_content(self, found_file):
        raise NotImplementedError()

    def top_dir(self, folder):
        return next(iter(self.walk(folder)))

    def get_dirs(self):
        path, dir_names, __ = self.top_dir(self.base_folder)
        yield path
        for dir_name in dir_names:
            yield os.path.join(path, dir_name)

    def get_songs(self, folder):
        return [
            FoundSong(os.path.join(self.base_folder, folder, dir_path), file_name, self)
            for dir_path, __, file_names in self.walk(folder)
            for file_name in file_names
            if file_name.endswith(".xml")
        ]


class ServerExplorer(Explorer):
    def __init__(self, base_folder=""):
        base_folder = os.path.join(settings.SONGS_FOLDER, base_folder)

        super(ServerExplorer, self).__init__(base_folder)

    def get_content(self, found_file):
        with open(found_file.path, "rb") as file_handler:
            return file_handler.read()

    def walk(self, folder):
        folder = os.path.normpath(folder)
        folder = os.path.join(self.base_folder, folder)
        base_folder_length = len(folder)
        for dirpath, dirnames, filenames in os.walk(folder):
            yield dirpath[base_folder_length + 1:], dirnames, filenames


class DropboxExplorer(Explorer):

    def __init__(self, token, base_folder="/"):
        super(DropboxExplorer, self).__init__(base_folder=base_folder)
        self.token = token
        self.client = DropboxClient(oauth2_access_token=self.token, locale=translation.get_language())

    def walk(self, folder):
        return self.walk_recurs(self.client, folder)

    def get_content(self, found_file):
        with self.client.get_file(found_file.path) as file_handler:
            return file_handler.read()

    def walk_recurs(self, client, base_path, path=""):

        folder_content = list(client.metadata(os.path.join(base_path, path))["contents"])

        dirs = [os.path.basename(item["path"]) for item in folder_content if item["is_dir"]]
        files = [os.path.basename(item["path"]) for item in folder_content if not item["is_dir"]]
        yield path, dirs, files
        for dir_path in dirs:
            for element in self.walk_recurs(client, base_path, os.path.join(path, dir_path)):
                yield element
