__all__ = []

import asyncio
from typing import Any, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import Message


class AlbumMiddleware(BaseMiddleware):
    def __init__(
        self,
        latency: Union[int, float] = 0.5,
        max_wait: Union[int, float] = 1.0,
    ):
        self.latency = latency
        self.max_wait = max_wait
        self.album_data = (
            {}
        )
        self.pending_albums = (
            {}
        )

    async def __call__(self, handler, event: Message, data: Dict[str, Any]):
        if not event.media_group_id:
            return await handler(event, data)

        first_media_group = None
        for mg_id, messages in self.album_data.items():
            if messages[-1].message_id + 1 == event.message_id:
                first_media_group = mg_id
                break

        if first_media_group:
            self.album_data[first_media_group].append(event)
            self.pending_albums[event.media_group_id] = (
                asyncio.get_event_loop().time()
            )
        else:
            first_media_group = event.media_group_id
            self.album_data[first_media_group] = [event]
            self.pending_albums[event.media_group_id] = (
                asyncio.get_event_loop().time()
            )

        wait_time = (
            self.max_wait
            if len(self.album_data[first_media_group]) >= 10
            else self.latency
        )
        await asyncio.sleep(wait_time)

        if first_media_group not in self.album_data:
            return

        last_message = self.album_data[first_media_group][-1]
        if event.message_id != last_message.message_id:
            return

        album_messages = self.album_data.pop(first_media_group, [])
        for mg_id in list(self.pending_albums.keys()):
            if any(m.media_group_id == mg_id for m in album_messages):
                self.pending_albums.pop(mg_id, None)

        if not album_messages:
            return

        album_messages.sort(key=lambda x: x.message_id)
        data['album'] = album_messages
        await handler(event, data)
