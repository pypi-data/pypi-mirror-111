from dataclasses import dataclass

from ..errors.ChannelErrors import *
from ..errors.MessageErrors import *
from ..errors.SessionErrors import *
from ..utils.Dict2Query import convert as d2q_converter
from ..utils.Request import Request
from ..utils.WrongType import raise_error


@dataclass
class ClientUser:
    # Attrs
    def __init__(self, json: dict, token: str, max_messages: int) -> None:
        self.__token: str = token
        self.max_messages = max_messages
        self.request_handler = Request()

        for key in json:
            setattr(self, key, json[key])

        self.cache: dict = {
            "message": [],
            "guild": []
        }

    async def add_message_cache(self, message):
        """Add message to cache"""

        self.cache['message'].append(message)

        if len(self.cache['message']) > self.max_messages:
            del self.cache['message'][0]

    async def remove_message_cache(self, packet):
        """Remove deleted message from cache"""

        for index, cache in enumerate(self.cache['message']):
            if cache.id == packet['id'] and cache.channel_id == packet['channel_id']:
                del self.cache['message'][index]
                break

    async def bulk_delete_message_cache(self, packet):
        """Remove Bulk-deleted message from cache"""

        shift = 0
        for index, cache in enumerate(self.cache['message'][:]):
            if cache.id in packet['ids'] and cache.channel_id == packet['channel_id']:
                del self.cache['message'][index - shift]
                shift += 1

    async def update_message_cache(self, message):
        """Update message from cache"""

        for index, cache in enumerate(self.cache['message']):
            if cache.id == message.id and cache.channel_id == message.channel_id:
                self.cache['message'][index] = message
                break

    async def add_guild_cache(self, guild):
        """Add a guild to cache."""

        self.cache["guild"].append(guild)

    async def update_guild_cache(self, guild):
        """Update a guild from cache."""

        for index, cache in enumerate(self.cache['guild']):
            if cache.id == guild.id:
                self.cache['guild'][index] = guild
                break

    async def remove_guild_cache(self, packet):
        """Remove a guild from cache."""

        for index, cache in enumerate(self.cache['guild'][:]):
            if cache.id == packet['id']:
                del self.cache['guild'][index]
                break

    async def add_guild_member(self, guild_id, member):
        """Add a guild member to guild cache."""

        for index, cache in enumerate(self.cache['guild']):
            if cache.id == guild_id:
                self.cache['guild'][index].members.append(member)
                break

    async def remove_guild_member(self, guild_id, user):
        """Remove a guild member from guild cache."""

        for index, cache in enumerate(self.cache['guild']):
            if cache.id == guild_id:
                for user_index, cache_user in enumerate(cache.members):
                    if cache_user.user.id == user.id:
                        self.cache['guild'][index].members.pop(user_index)
                        break
                break

    async def update_guild_member(self, guild_id, member):
        """Update a guild member from guild cache."""

        for index, cache in enumerate(self.cache['guild']):
            if cache.id == guild_id:
                for user_index, cache_user in enumerate(cache.members):
                    if cache_user.user.id == member.user.id:
                        self.cache['guild'][index].members[user_index] = member
                        break
                break

    async def add_guild_channel(self, channel):
        """Add a guild channel to guild cache."""

        for index, cache in enumerate(self.cache['guild']):
            if hasattr(channel, "guild_id") and cache.id == channel.guild_id:
                self.cache['guild'][index].channels.append(channel)
                break

    async def remove_guild_channel(self, channel):
        """Remove a guild channel from guild cache."""

        for index, cache in enumerate(self.cache['guild']):
            if hasattr(channel, "guild_id") and cache.id == channel.guild_id:
                for channel_index, cache_channel in enumerate(cache.channels):
                    if cache_channel.id == channel.id:
                        self.cache['guild'][index].channels.pop(channel_index)
                        break
                break

    async def update_guild_channel(self, channel):
        """Update a guild channel from guild cache."""

        for index, cache in enumerate(self.cache['guild']):
            if hasattr(channel, "guild_id") and cache.id == channel.guild_id:
                for channel_index, cache_channel in enumerate(cache.channels):
                    if cache_channel.id == channel.id:
                        self.cache['guild'][index].channels[channel_index] = channel
                        break
                break

    async def fetch_channel(self, channel_id: str):
        """Fetch channel with id."""
        raise_error(channel_id, "id", str)

        from .Channel import Channel

        atom, result = await self.request_handler.send_async_request(f"/channels/{channel_id}", "GET", self.__token)

        if atom == 0:
            return Channel(result, self.__token)
        else:
            raise GetChannelError(result)

    def get_guild_channel(self, channel_id: str):
        """Get channel with id. (from cache.)"""
        raise_error(channel_id, "channel_id", str)

        for guild in self.cache['guild']:
            for channel in guild.channels:
                if channel.id == channel_id:
                    return channel

    async def bulk_delete(self, channel_id: str, limit: int = 10):
        """Bulk-delete channel messages with channel id."""
        raise_error(channel_id, "id", str)
        raise_error(limit, "limit", int)

        from .Message import Message

        # filtered = [i.id for i in self.cache["message"] if i.channel_id == channel_id][::-1][:limit]

        # if len(filtered) < 2:
        query_format = f"/channels/{channel_id}/messages?limit={limit}"
        atom, result = await self.request_handler.send_async_request(query_format, "GET", self.__token)

        if atom == 0:
            filtered = [
                Message(i, self.__token).id for i in result][::-1][:limit]
        else:
            raise FetchChannelHistoryFailed(result)

        atom, result = await self.request_handler.send_async_request(f"/channels/{channel_id}/messages/bulk-delete", "POST",
                                                                     self.__token, {"messages": filtered})

        if atom == 0:
            return filtered
        else:
            raise BulkDeleteMessageFailed(result)

    async def say(self, channel_id: str, params=None):
        """Send message to the channel."""
        if params is None:
            params = {}
        raise_error(channel_id, "channel_id", str)

        if params is not None:
            raise_error(params, "params", dict)

        from .Message import Message

        atom, result = await self.request_handler.send_async_request(f"/channels/{channel_id}/messages", "POST", self.__token,
                                                                     params)

        if atom == 0:
            return Message(result, self.__token)
        else:
            raise SendMessageToChannelFailed(result)

    async def fetch_invite(self, code: str, options=None):
        """Get invite information with invite code (supports API params.)."""
        if options is None:
            options = {}
        raise_error(code, "code", str)

        if options is not None:
            raise_error(options, "options", dict)

        from .Invite import Invite

        atom, result = await self.request_handler.send_async_request(f"/invites/{code}{d2q_converter(options)}", "GET",
                                                                     self.__token)

        if atom == 0:
            return Invite(result, self.__token)
        else:
            raise FetchInviteFailedError(result)

    async def remove_invite(self, code: str):
        """Remove invite with invite code."""
        raise_error(code, "code", str)

        from .Invite import Invite

        atom, result = await self.request_handler.send_async_request(f"/invites/{code}", "DELETE", self.__token)

        if atom == 0:
            return Invite(result, self.__token)
        else:
            raise RemoveInviteFailedError(result)

    async def fetch_client_user(self):
        """Fetch information about client user."""
        from .User import User

        atom, result = await self.request_handler.send_async_request("/users/@me", "GET", self.__token)

        if atom == 0:
            return User(result, self.__token)
        else:
            raise FetchUserFailedError(result)

    async def fetch_user_profile(self, user_id: str):
        """Fetch user profile."""
        raise_error(user_id, "user_id", str)

        from .User import User

        atom, result = await self.request_handler.send_async_request(f"/users/{user_id}/profile", "GET", self.__token)

        if atom == 0:
            return User(result, self.__token)
        else:
            raise FetchUserFailedError(result)

    async def fetch_user(self, user_id: str):
        """Fetch information about an user."""
        raise_error(user_id, "user_id", str)

        from .User import User

        atom, result = await self.request_handler.send_async_request(f"/users/{user_id}", "GET", self.__token)

        if atom == 0:
            return User(result, self.__token)
        else:
            raise FetchUserFailedError(result)

    def get_guild(self, guild_id: str):
        """Get guild from cache."""
        raise_error(guild_id, "id", str)

        for guild in self.cache["guild"]:
            if guild.id == guild_id:
                return guild

    def get_message(self, message_id: str):
        """Get message from cache."""
        raise_error(message_id, "id", str)

        for message in self.cache["message"]:
            if message.id == message_id:
                return message

    async def fetch_guild(self, guild_id: str, options=None):
        """Fetch guild with API params."""
        if options is None:
            options = {}
        raise_error(guild_id, "id", str)
        raise_error(options, "options", dict)

        from .Guild import Guild

        atom, result = await self.request_handler.send_async_request(f"/guilds/{guild_id}{d2q_converter(options)}", "GET",
                                                                     self.__token)

        if atom == 0:
            return Guild(result, self.__token)
        else:
            raise FetchGuildFailedError(result)

    async def edit_user(self, params=None):
        """Modify current user with API params."""
        if params is None:
            params = {}
        raise_error(params, "params", dict)

        from .User import User

        atom, result = await self.request_handler.send_async_request("/users/@me", "PATCH", self.__token, params)

        if atom == 0:
            return User(result, self.__token)
        else:
            raise EditClientUserFailed(result)

    async def leave_guild(self, guild_id: str):
        """Leave a guild with id."""
        raise_error(guild_id, "guild_id", str)

        atom, result = await self.request_handler.send_async_request(f"/users/@me/guilds/{guild_id}", "DELETE", self.__token, {})

        if atom == 0:
            return True
        else:
            raise LeaveGuildFailed(result)

    async def fetch_guild_preview(self, guild_id: str):
        """Fetch guild preview with id."""
        raise_error(guild_id, "guild_id", str)

        from .GuildPreview import GuildPreview

        atom, result = await self.request_handler.send_async_request(f"/guilds/{guild_id}/preview", "GET", self.__token)

        if atom == 0:
            return GuildPreview(result, self.__token)
        else:
            raise FetchGuildPreviewFailed(result)

    async def create_guild(self, params: dict):
        """Create a new guild."""
        raise_error(params, "params", dict)

        from .Guild import Guild

        atom, result = await self.request_handler.send_async_request(f"/guilds", "POST", self.__token, params)

        if atom == 0:
            return Guild(result, self.__token)
        else:
            raise CreateGuildFailed(result)

    async def create_dm(self, user_id: str):
        """Create DM with user id."""

        from .Channel import Channel

        atom, result = await self.request_handler.send_async_request(f"/users/@me/channels", "POST", self.__token, {
            "recipient_id": user_id
        })

        if atom == 0:
            return Channel(result, self.__token)
        else:
            raise CreateDMFailed(result)

    async def fetch_webhook(self, webhook_id: str):
        """Fetch a webhook with ID."""

        from .Webhook import Webhook

        atom, result = await self.request_handler.send_async_request(f"/webhooks/{webhook_id}", "GET", self.__token)

        if atom == 0:
            return Webhook(result, self.__token)
        else:
            raise CreateWebhookFailed(result)
