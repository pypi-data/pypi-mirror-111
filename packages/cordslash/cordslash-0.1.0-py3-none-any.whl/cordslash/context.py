"""
The MIT License (MIT)

Copyright (c) 2021 an-dyy

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

__all__ = "Context"

from corded import Route
from .models import User, Channel, Mentionable


class Context:
    def __init__(self, bot, payload: dict):
        self.token = payload["token"]
        self.author = payload["member"]
        self.id = payload["id"]
        self.guild_id = payload["guild_id"]
        self.channel_id = payload["channel_id"]
        self.data = payload["data"]
        self.command = bot.commands[payload["data"]["name"]]
        self.bot = bot

    async def invoke(self):
        args = [self]
        for option in self.data["options"]:
            args.append(option["value"])

        ret = await self.command.callback(*args)
        return ret

    async def send(self, content):
        payload = {"type": 4, "data": {"content": content}}
        route = Route(
            "/interactions/{id}/{token}/callback", id=self.id, token=self.token
        )
        await self.bot.http.request("POST", route, json=payload)
