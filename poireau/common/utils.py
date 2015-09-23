import os
import shutil


class FilesManager(object):
    def make_dir(self, path):
        os.makedirs(path, exist_ok=True)

    def exists(self, path):
        return os.path.exists(path)

    def is_dir(self, path):
        return os.path.isdir(path)

    def remove_file(self, path):
        return os.remove(path)

    def remove_dir(self, path):
        return shutil.rmtree(path)

    def remove(self, path):
        if self.is_dir(path):
            self.remove_dir(path)
        else:
            self.remove_file(path)

    def write(self, path, content):
        with open(path, "wb") as handler:
            handler.write(content)

    def read(self, path):
        with open(path, "rb") as handler:
            return handler.read()

    def walk(self, path):
        return os.walk(path)

# Todo : implement a S3 Manager for Heroku
