import logging
import os
import pathlib
import sys
from typing import TypedDict

import click
import oss2

from yucebio_uploader.base import BaseUploader


class OSSConfig(TypedDict):
    access_key_id: str
    access_key_secret: str
    region: str
    bucket: str

class Uploader(BaseUploader):
    PLATFROM = 'ali'
    ALIAS_NAME = ['bcs', 'oss', 'ali']

    def __init__(self) -> None:
        super().__init__()
        self._auth = None
        self._bucket = None

    @property
    def config(self):
        return self._config('oss', {})

    def configure(self):
        access_id = click.prompt("Please Input ACCESS KEY ID")
        access_secrect = click.prompt("Please Input ACCESS KEY SECRECT")
        region = click.prompt("Please Input Region", default='cn-shenzhen')
        bucket = click.prompt("Please Input Bucket name", default='yucebio')
        endpoint = click.prompt("Please Input Endpoint", default=f"https://oss-{region}.aliyuncs.com")

        self._config['oss'] = {
            "access_key_id": access_id,
            "access_key_secret": access_secrect,
            "region": region,
            "bucket": bucket,
            "endpoint": endpoint
        }
        self._config.reload()

    @property
    def oss_config(self) -> OSSConfig:
        if not self.config:
            self.configure()
        return self.config

    @property
    def endpoint(self) -> str:
        return self.oss_config['endpoint'] or f"https://oss-{self.oss_config['region']}.aliyuncs.com"

    @property
    def auth(self) -> oss2.Auth:
        if not self._auth:
            self._auth = oss2.Auth(self.oss_config["access_key_id"], self.oss_config['access_key_secret'])
        return self._auth

    @property
    def bucket(self) -> oss2.Bucket:
        if not self._bucket:
            self._bucket = oss2.Bucket(self.auth, self.endpoint, self.oss_config['bucket'])
        return self._bucket

    def upload(self, local: str, remote: str, recursive: bool = False) -> str:
        if not os.path.exists(local):
            raise FileNotFoundError(local)

        def percentage(byte_size, total_bytes):
            if total_bytes:
                rate = int(100 * (float(byte_size) / float(total_bytes)))
                print(click.style(f'\rUploaded {rate}%:', fg='yellow') + click.style('#' * rate, fg='green'), end="")
                sys.stdout.flush()

        prefix = f"oss://{self.bucket.bucket_name}/"
        if remote.startswith(prefix):
            remote = remote[len(prefix):]

        key = '/'.join(pathlib.Path(remote).parts)
        click.secho(f"开始上传文件{local} ==> {remote} {key}", fg='green')

        # 检查文件是否存在
        logging.info(f"start upload file: {local} ==> {remote}")
        if self.bucket.object_exists(key):
            meta: oss2.models.GetObjectMetaResult = self.bucket.get_object_meta(key)
            if meta.etag.lower() == self.md5(local):
                logging.info(f"remote file [{remote}][md5: {meta.etag}] exists!! ")
                return f"oss://{self.bucket.bucket_name}/{key}"

        self.bucket.put_object_from_file(key, local, progress_callback=percentage)
        logging.info(f"oss://{self.bucket.bucket_name}/{key} file upload success.")

        return f"oss://{self.bucket.bucket_name}/{key}"
