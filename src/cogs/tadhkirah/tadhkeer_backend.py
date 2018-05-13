import asyncio
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
        self._readying = False
        self.loop.create_task(self._wait_for_ready())

    def _authorize_client(self):
        self._client = pygsheets.authorize(service_file=self.google_creds_file)
        self._sheet = self._client.open(self.sheet_name).sheet1
        self._header_row = self._sheet.get_row(1)

    async def _wait_for_ready(self):
        if self._sheet is None:
            if not self._readying:
                self._readying = True
                await self.loop.run_in_executor(None, self._authorize_client)
                self._readying = False
            else:
                while self._readying:
                    await asyncio.sleep(50)

    def _make_embed(self, row):
        embed_dict = dict(zip(self._header_row, row))
        embed = get_embed(embed_dict)
        return embed

    async def _get(self, row_number):
        row = await self.loop.run_in_executor(None, self._sheet.get_row, row_number)
        embed = self._make_embed(row)
        return embed

    async def get_random(self):
        await self._wait_for_ready()
        random_row_number = random.randint(2, self._sheet.rows)
        return await self._get(random_row_number)

    async def get_from_category(self, category):
        await self._wait_for_ready()
        category_range = await self.loop.run_in_executor(None, self._sheet.get_named_range, 'category')
        await self.loop.run_in_executor(None, category_range.fetch)
        flattened_cells = [c[0] for c in category_range.cells][1:]  # exclude header
        curated_cells = [c for c in flattened_cells if c.value == category]

        random_cell = random.choice(curated_cells)
        return await self._get(random_cell.row)
