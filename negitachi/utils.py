from __future__ import unicode_literals


class Syncer(object):

    @classmethod
    def sync(cls, old, new, commit=True, *args, **kwargs):
        syncer = cls(*args, **kwargs)
        old_objects = syncer.get_old_objects(old)
        new_objects = syncer.get_new_objects(new)

        created = syncer.get_created(old_objects, new_objects)
        deleted = syncer.get_deleted(old_objects, new_objects)
        modified = syncer.get_modified(old_objects, new_objects)
        if commit:
            syncer.apply_changes(created, deleted, modified)

        return created, deleted, modified

    def get_old_objects(self, iterable):
        raise NotImplementedError("")

    def get_new_objects(self, iterable):
        raise NotImplementedError("")

    def get_created(self, old, new):
        raise NotImplementedError("")

    def get_deleted(self, old, new):
        raise NotImplementedError("")

    def get_modified(self, old, new):
        raise NotImplementedError("")

    def apply_changes(self, created, deleted, modified):
        raise NotImplementedError("")
