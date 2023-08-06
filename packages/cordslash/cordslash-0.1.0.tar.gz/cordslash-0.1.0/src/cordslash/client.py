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

from __future__ import annotations

import re
from typing import Optional, Callable, List, Dict, Tuple

__all__ = "cordClient"

import corded as c
from .command import Command
from .context import Context


class FakeEvent(c.GatewayEvent):
    def __init__(self, name: str):
        super().__init__(0, 0, 0, 0, 0, name)


class cordClient(c.CordedClient):
    def __init__(self, /, token: str, app_id: int, intents: c.Intents, *args, **kwargs):
        super().__init__(token, intents, *args, **kwargs)
        self.gateway.listeners["interaction_create"].append(self.on_interaction_create)
        self.gateway.listeners["ready"].append(self._set_ready)

        self.commands: Dict[str, Command] = {}
        self.token = token
        self.app_id = app_id
        self._ready = 0

    async def _set_ready(self, ev):
        ev = FakeEvent("_register_commands")
        self._ready += 1
        await self.gateway.dispatch(ev)

    def command(
        self,
        /,
        name: Optional[str] = None,
        guild_ids: Optional[List[int]] = None,
        **kwargs,
    ):
        def wrapper(func: Callable) -> Command:
            if name and re.findall(r"[\s]", name):
                raise Exception(f"Command `{name}`` cannot have a space in the name")
            command = Command(self, func, name=name, guild_ids=guild_ids, **kwargs)
            self.commands[command.name] = command
            return command

        return wrapper

    async def get_context(self, payload):
        ctx = Context(self, payload)
        return ctx

    async def process_commands(self, payload: dict):
        ctx = await self.get_context(payload)
        await ctx.invoke()

    async def on_interaction_create(self, event: c.GatewayEvent) -> None:
        await self.process_commands(event.typed_data)
