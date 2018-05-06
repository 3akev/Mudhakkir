import asyncio
import os
from dropbox import Dropbox, files

from statics import dropboxPath, parentDir


class DropBoxer:
    dbx: Dropbox = None
    loop: asyncio.AbstractEventLoop = None
    uploadBatch = {}

    @classmethod
    async def uploadLoop(cls):
        while True:
            while cls.uploadBatch:
                file, remotePath = cls.uploadBatch.popitem()
                await cls.loop.run_in_executor(None, cls.raw_upload, file, remotePath)
            await asyncio.sleep(1)

    @classmethod
    async def get(cls, path=dropboxPath + '/'):
        await cls.loop.run_in_executor(None, cls.raw_get, path)

    @classmethod
    def upload(cls, file):
        file = file.replace('\\', '/')
        remotePath = dropboxPath + file[file.find('/storage'):]
        cls.uploadBatch[file] = remotePath

    @classmethod
    def raw_upload(cls, file, remotePath):
        cls.setDbx()
        cls.dbx.files_upload(open(file, 'rb').read(), remotePath, files.WriteMode.overwrite)

    @classmethod
    def raw_get(cls, path):
        cls.setDbx()
        resp = cls.dbx.files_list_folder(path)
        for thingy in resp.entries:
            if isinstance(thingy, files.FolderMetadata):
                cls.raw_get(thingy.path_display)
            elif isinstance(thingy, files.FileMetadata):
                metadata, file = cls.dbx.files_download(thingy.path_display)
                realpath = path.replace(dropboxPath, '', 1)
                os.makedirs(parentDir + realpath, exist_ok=True)
                with open(os.path.join(parentDir + realpath, os.path.basename(thingy.path_display)), 'wb') as f:
                    f.write(file.content)

    @classmethod
    def setDbx(cls):
        if cls.dbx is None:
            cls.dbx = Dropbox(os.environ.get("DROPBOX_TOKEN"))

    @classmethod
    def setLoop(cls, loop):
        cls.loop = loop
