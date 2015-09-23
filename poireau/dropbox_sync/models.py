import os
import contextlib

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

import dropbox

from poireau.common.utils import FilesManager


class FolderSync(models.Model):
    cursor = models.CharField(max_length=512, verbose_name=_("cursor"), null=True)
    date = models.DateTimeField(verbose_name=_("date"), default=timezone.now)
    dropbox_path = models.CharField(max_length=512, verbose_name=_("dropbox path"))
    local_path = models.CharField(max_length=512, verbose_name=_("local path"))

    class Meta(object):
        app_label = "dropbox_sync"
        verbose_name = _("Folder Sync")
        verbose_name_plural = _("Folder Syncs")

    @classmethod
    def sync_folder(cls, dropbox_client, local_base_dir, dropbox_path, files_manager=None):
        files_manager = files_manager or FilesManager()

        dbx = dropbox_client
        dropbox_path_lower = "/" + dropbox_path.lower().strip("/")

        files_manager.make_dir(local_base_dir)

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

            if not is_deleted and files_manager.exists(local_path):
                if is_folder != files_manager.is_dir(local_path):
                    is_deleted = True

            if is_deleted:
                files_manager.remove(local_path)
                continue

            if is_folder:
                files_manager.make_dir(local_path)
                continue

            if is_file:
                __, response = dbx.files_download(os.path.join(dropbox_path_lower, path))
                with contextlib.closing(response):
                    files_manager.write(local_path, response.content)
                continue

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
