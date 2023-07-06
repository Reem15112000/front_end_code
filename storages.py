from storages.backends.s3boto3 import S3Boto3Storage, S3StaticStorage


class StaticRootS3Boto3Storage(S3StaticStorage):
    def __init__(self, *args, **kwargs):
        kwargs["location"] = "static"
        super().__init__(*args, **kwargs)
        self.file_overwrite = True


class MediaRootS3Boto3Storage(S3Boto3Storage):
    def __init__(self, *args, **kwargs):
        kwargs["location"] = "media"
        super().__init__(*args, **kwargs)
