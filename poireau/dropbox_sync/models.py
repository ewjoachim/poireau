import os
import shutil

from django.db import models
from django.utils.translation import ugettext_lazy as _

import dropbox


class FolderSync(models.Model):
    cursor = models.CharField(max_length=512, verbose_name=_("cursor"), null=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("date"))
    dropbox_path = models.CharField(max_length=512, verbose_name=_("dropbox path"))
    local_path = models.CharField(max_length=512, verbose_name=_("local path"))

    class Meta(object):
        app_label = "dropbox"
        verbose_name = _("Folder Sync")
        verbose_name_plural = _("Folder Syncs")

    @classmethod
    def sync_folder(cls, dropbox_client, local_base_dir, dropbox_path):
        dbx = dropbox_client
        dropbox_path_lower = "/" + dropbox_path.lower().strip("/")

        os.makedirs(local_base_dir, exist_ok=True)

        latest_sync = cls.objects.filter(local_path=local_base_dir).order_by("-date").first()

        cursor = None
        if latest_sync:
            cursor = latest_sync.cursor

        if cursor:
            folder_list = dbx.files_list_folder_continue(cursor=cursor)
        else:
            folder_list = dbx.files_list_folder(dropbox_path, recursive=True)

        metadata_list = []

        while True:
            cursor = folder_list.cursor
            metadata_list += folder_list.entries
            if not folder_list.has_more:
                break

            folder_list = dbx.files_list_folder_continue(cursor=cursor)

        for metadata in metadata_list:
            is_folder = isinstance(metadata, dropbox.files.FolderMetadata)
            is_deleted = isinstance(metadata, dropbox.files.DeletedMetadata)
            is_file = isinstance(metadata, dropbox.files.FileMetadata)

            path = metadata.path_lower[len(dropbox_path_lower) + 1:]
            local_path = os.path.join(local_base_dir, path)

            if not is_deleted and os.path.exists(local_path):
                if is_folder != os.path.isdir(local_path):
                    is_deleted = True

            if is_deleted:
                try:
                    os.remove(local_path)
                except OSError:
                    shutil.rmtree(local_path)
                continue

            if is_folder:
                os.makedirs(local_path, exist_ok=True)
                continue

            if is_file:
                try:
                    __, response = dbx.files_download(os.path.join(dropbox_path_lower, path))
                finally:
                    response.close()
                with open(local_path, "wb") as file_handler:
                    file_handler.write(response.content)

        cls.objects.create(
            cursor=cursor,
            dropbox_path=dropbox_path,
            local_path=local_base_dir,
        )

    @classmethod
    def fake_sync_folder(cls, dropbox_client, local_base_dir, dropbox_path):
        cursor = dropbox_client.files_list_folder_get_latest_cursor(dropbox_path, recursive=True).cursor
        cls.objects.create(
            cursor=cursor,
            dropbox_path=dropbox_path,
            local_path=local_base_dir,
        )

    @classmethod
    def reset_folder(cls, local_base_dir, dropbox_path):
        cls.objects.create(
            cursor=None,
            dropbox_path=dropbox_path,
            local_path=local_base_dir,
        )
