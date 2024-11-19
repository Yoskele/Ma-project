from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify

class CKEditorStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # Replace spaces with underscores in file names
        name = name.replace(" ", "_")
        return super().get_available_name(name, max_length)
