import datetime
import os
import tempfile

from django.conf import settings
from django.core.files.uploadedfile import (
    UploadedFile,
    TemporaryUploadedFile
)
from django.core.files.uploadhandler import FileUploadHandler


class TimingUploadedFile(UploadedFile):
    """
    A file uploaded to a temporary location (i.e. stream-to-disk).
    including `start_upload_time` field
    """
    def __init__(
            self, name,
            content_type,
            size, charset,
            content_type_extra=None,
            start_upload_time=None,
            upload_time=None
    ):
        _, ext = os.path.splitext(name)
        file = tempfile.NamedTemporaryFile(
            suffix='.upload' + ext,
            dir=settings.FILE_UPLOAD_TEMP_DIR
        )
        self.start_upload_time = start_upload_time
        self.upload_time = upload_time
        super().__init__(
            file, name,
            content_type,
            size, charset,
            content_type_extra
        )

    def temporary_file_path(self):
        """Return the full path of this file."""
        return self.file.name

    def close(self):
        try:
            return self.file.close()
        except FileNotFoundError:
            # The file was moved or deleted before the tempfile could unlink
            # it. Still sets self.file.close_called and calls
            # self.file.file.close() before the exception.
            pass


class ChunkFileUploadHandler(FileUploadHandler):
    """
    Upload handler that chunk streams data into a file.
    """

    chunk_size = settings.UPLOAD_CHUNK_SIZE

    def new_file(self, *args, **kwargs):
        """
        Create the file object to append to as data is coming in.
        """
        super().new_file(*args, **kwargs)
        self.file = TemporaryUploadedFile(
            self.file_name,
            self.content_type, 0,
            self.charset,
            self.content_type_extra
        )

    def receive_data_chunk(self, raw_data, start):
        self.file.write(raw_data)

    def file_complete(self, file_size):
        self.file.seek(0)
        self.file.size = file_size
        return self.file

    def upload_interrupted(self):
        if hasattr(self, 'file'):
            temp_location = self.file.temporary_file_path()
            try:
                self.file.close()
                os.remove(temp_location)
            except FileNotFoundError:
                pass

class TimingUploadHandler(FileUploadHandler):
    """
    Upload handler that measures time of streaming data into a file.
    # TODO: it calculates upload time but we have no upload_time property in model to save it
    """

    chunk_size = settings.UPLOAD_CHUNK_SIZE

    def new_file(self, *args, **kwargs):
        """
        Create the file object to append to as data is coming in.
        """
        super().new_file(*args, **kwargs)
        self.file = TimingUploadedFile(
            self.file_name,
            self.content_type, 0,
            self.charset,
            self.content_type_extra,
            datetime.datetime.now()
        )

    def receive_data_chunk(self, raw_data, start):
        self.file.write(raw_data)

    def file_complete(self, file_size):
        self.file.seek(0)
        self.file.size = file_size
        return self.file

    def upload_interrupted(self):
        if hasattr(self, 'file'):
            temp_location = self.file.temporary_file_path()
            try:
                self.file.close()
                os.remove(temp_location)
            except FileNotFoundError:
                pass

    def upload_complete(self):
        if hasattr(self, 'file'):
            self.file.upload_time = datetime.datetime.now() - self.file.start_upload_time
