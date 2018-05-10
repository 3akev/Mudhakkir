import os
import random
from asyncio import AbstractEventLoop

import pygsheets
from pygsheets import Worksheet

from framework.embed import get_embed
from statics import storageDir


class TadhkeerBackend:
    google_creds_file = os.path.join(storageDir, 'google_creds.json')
    scope = ['https://spreadsheets.google.com/feeds']
    sheet_name = 'Reminders'

    def __init__(self, loop):
        self.loop: AbstractEventLoop = loop
        self._client = None
        self._sheet: Worksheet = None
        self.loop.create_task(self._ensure_client())

    def _authorize_client(self):
        self._client = pygsheets.authorize(service_file=self.google_creds_file)
        self._sheet = self._client.open(self.sheet_name).sheet1
        self._header_row = self._sheet.get_row(1)

    async def _ensure_client(self):
        if self._client is None:
            await self.loop.run_in_executor(None, self._authorize_client)

    def _make_embed(self, row):
        embed_dict = dict(zip(self._header_row, row))
        embed = get_embed(embed_dict)
        return embed

    async def get_random(self):
        await self._ensure_client()
        random_row_number = random.randint(2, self._sheet.rows)
        actual_row = await self.loop.run_in_executor(None, self._sheet.get_row, random_row_number)
        embed = self._make_embed(actual_row)
        return embed

