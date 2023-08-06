from typing import List, SupportsAbs, overload
from .tools import jsonifyMessage, V8Route
from .receive import Message, getResponseMessage

import discord
from discord.ext import commands


class Buttons():
    """A button instance for using buttons
    
    - - -

    Attributes
    ----------------
    send: `function`
        Sends a message to a `discord.TextChannel`
    
    """
    def __init__(self, client: commands.Bot):
        """This will create a new button intearction Listener

        For receiving the button event, scroll down to the bottom and take a look at the example

        - - -

        Parameters
        ------------------
        client: `commands.Bot`
            The discord bot client

        - - -

        Example
        ------------------
        Here's an example for using the button listener
        ```py
        # Your bot declaration should be here
        ...
        client.buttons = Buttons(client)

        @client.event("on_button_press")
        async def on_button(pressedButton, message):
            pass
        ```
        """
        self._discord = client
        self._discord.add_listener(self.on_socket_response)
    
    async def on_socket_response(self, msg):
        """Will be executed if the bot receives a socket response"""
        if msg["t"] != "INTERACTION_CREATE":
            return
        data = msg["d"]

        if data["type"] != 3:
            return
        
        guild = await self._discord.fetch_guild(data["guild_id"])
        user = discord.Member(data=data["member"], guild=guild, state=self._discord._connection)
        
        msg = await getResponseMessage(self._discord, data, user, True)

        self._discord.dispatch("button_press", msg.pressedButton, msg)
    

    async def send(self, channel: discord.TextChannel, content: str = None, *, tts: bool = False,
            embed: discord.Embed = None, embeds: List[discord.Embed] = None, file: discord.File = None, 
            files: List[discord.File] = None, delete_after: float = None, nonce: int = None,
            allowed_mentions: discord.AllowedMentions = None, reference: discord.MessageReference or discord.Message = None, 
            mention_author: bool = None, buttons: List[Button] = None
        ) -> Message:
        """[summary]

        Parameters
        ----------
        channel : discord.TextChannel
            [description]
        content : str, optional
            [description], by default None
        tts : bool, optional
            [description], by default False
        embed : discord.Embed, optional
            [description], by default None
        embeds : List[discord.Embed], optional
            [description], by default None
        file : discord.File, optional
            [description], by default None
        files : List[discord.File], optional
            [description], by default None
        delete_after : float, optional
            [description], by default None
        nonce : int, optional
            [description], by default None
        allowed_mentions : discord.AllowedMentions, optional
            [description], by default None
        reference : discord.MessageReferenceordiscord.Message, optional
            [description], by default None
        mention_author : bool, optional
            [description], by default None
        buttons : List[Button], optional
            [description], by default None

        Returns
        -------
        Message
            [description]

        Raises
        ------
        discord.InvalidArgument
            [description]
        """

        if type(channel) != discord.TextChannel:
            raise discord.InvalidArgument("Channel must be of type discord.TextChannel")

        payload = jsonifyMessage(content, tts=tts, embed=embed, embeds=embeds, nonce=nonce, allowed_mentions=allowed_mentions, reference=reference, mention_author=mention_author, buttons=buttons)
        

        route = V8Route("POST", f"/channels/{channel.id}/messages")
        
        r = await self._discord.http.request(route, json=payload)
        msg = await getResponseMessage(self._discord, r, response=False)
            
        if delete_after is not None:
            await msg.delete(delay=delete_after)
        
        return msg