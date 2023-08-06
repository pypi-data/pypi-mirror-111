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

import inspect
from typing import Optional, Callable, List, Mapping, TypeVar, TYPE_CHECKING

__all__ = "Command"

if TYPE_CHECKING:
    from .client import cordClient

P = TypeVar("P")

from corded import Route


class Option:
    def __init__(self, type: int, name: str, description: str, required: bool):
        self.type = type
        self.name = name
        self.description = description
        self.required = required

    def _to_dict(self) -> dict:
        payload = {
            "type": self.type,
            "name": self.name,
            "description": self.description,
            "required": self.required,
        }

        return payload

    # TODO: add subcommands and subgroups


class Command:
    def __init__(
        self,
        bot: cordClient,
        func: Callable,
        name: Optional[str],
        description: Optional[str],
        guild_ids: Optional[List[int]] = None,
        options: Optional[List[Option]] = None,
        **kwargs,
    ):
        bot.gateway.listeners["_register_commands"].append(self.register)
        self._bot: cordClient = bot
        self.app_id = bot.app_id
        self._id: Optional[int] = None
        self.options = options or []
        self.name = name or func.__name__
        self.description = description
        self.callback = func
        self.params = self._get_signature(func)
        self._header = {"Authorization": f"Bot {bot.token}"}

        if guild_ids:
            self.guild_ids = guild_ids

    def __repr__(self) -> str:
        return f"<Command id={self._id}, name={self.name}>"

    def _get_signature(self, func):
        params = inspect.signature(func)
        if not self.options:
            self._fill_options(params)
        return params

    def _fill_options(self, params, /, cls=Option):
        _types = {
            "str": 3,
            "int": 4,
            "bool": 5,
            "slice.models.User": 6,
            "slice.models.Channel": 7,
            "slice.models.Mentionable": 8,
        }

        for param in params.parameters:
            parameter = params.parameters[param]
            annotation = str(parameter).split(": ")
            if annotation[1] in _types:
                option = cls(
                    type=_types[annotation[1]],
                    name=annotation[0],
                    description="\u200b",
                    required=True,
                )
                self.options.append(option)

    async def register(self, _ev):
        if self._bot._ready <= 1:
            if self.guild_ids:
                await self._create_guild_command()
            else:
                await self._create_global_command()

    def _to_dict(self) -> dict:
        payload = {"name": self.name, "description": self.description}

        if self.options:
            payload["options"] = [option._to_dict() for option in self.options]

        return payload

    async def _create_global_command(self) -> None:
        payload = self._to_dict()
        route = Route("/applications/{app_id}/commands", app_id=self.app_id)
        data = await self._bot.http.session.request(
            "POST", self._bot.http.url + route, json=payload, headers=self._header
        )
        data = await data.json()
        self._bot.commands[data["name"]]._id = data["id"]

    async def _create_guild_command(self) -> None:
        payload = self._to_dict()
        for guild_id in self.guild_ids:
            route = f"/applications/{self.app_id}/guilds/{guild_id}/commands"
            data = await self._bot.http.session.request(
                "POST", self._bot.http.url + route, json=payload, headers=self._header
            )
            data = await data.json()
            self._bot.commands[data["name"]]._id = data["id"]

    # TODO: delete, get etc
