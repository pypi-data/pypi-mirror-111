
# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import os
import asyncio
import re
# * Third Party Imports --------------------------------------------------------------------------------->
from jinja2 import BaseLoader, Environment
import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
# * Gid Imports ----------------------------------------------------------------------------------------->
import gidlogger as glog
# * Local Imports --------------------------------------------------------------------------------------->
from antipetros_discordbot.utility.checks import allowed_channel_and_allowed_role
from antipetros_discordbot.utility.discord_markdown_helper.general_markdown_helper import CodeBlock
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
from antipetros_discordbot.utility.enums import CogMetaStatus, UpdateTypus
from antipetros_discordbot.engine.replacements import AntiPetrosBaseCog, CommandCategory
from antipetros_discordbot.auxiliary_classes.for_cogs.aux_faq_cog import FaqItem
from typing import TYPE_CHECKING, Union
from antipetros_discordbot.utility.enums import CogMetaStatus, UpdateTypus
from antipetros_discordbot.engine.replacements import AntiPetrosBaseCog, CommandCategory, RequiredFile, auto_meta_info_group
from antipetros_discordbot.utility.general_decorator import universal_log_profiler
from antipetros_discordbot.utility.gidtools_functions import pathmaker, writejson, loadjson
if TYPE_CHECKING:
    from antipetros_discordbot.engine.antipetros_bot import AntiPetrosBot


# endregion[Imports]

# region [TODO]


# endregion [TODO]

# region [AppUserData]

# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
glog.import_notification(log, __name__)

# endregion[Logging]

# region [Constants]

APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')
COGS_CONFIG = ParaStorageKeeper.get_config('cogs_config')
# location of this file, does not work if app gets compiled to exe with pyinstaller
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

# endregion[Constants]


class FaqCog(AntiPetrosBaseCog, command_attrs={"categories": CommandCategory.ADMINTOOLS, "hidden": True}):

    """
    Creates Embed FAQ items.

    """
# region [ClassAttributes]
    public = False
    meta_status = CogMetaStatus.UNTESTED | CogMetaStatus.FEATURE_MISSING | CogMetaStatus.DOCUMENTATION_MISSING | CogMetaStatus.WORKING
    long_description = ""
    extra_info = ""
    required_config_data = {'base_config': {},
                            'cogs_config': {"faq_channel_id": "673410398510383115"}}
    faq_name_data_file = pathmaker(APPDATA["json_data"], "faq_name_table.json")
    required_folder = []
    required_files = [RequiredFile(faq_name_data_file, {}, RequiredFile.FileType.JSON)]
    q_emoji = "🇶"
    a_emoji = "🇦"

    number_split_regex = re.compile(r"\s|,")

# endregion [ClassAttributes]

# region [Init]

    def __init__(self, bot: "AntiPetrosBot"):
        super().__init__(bot)
        self.faq_items = {}
        self.color = "honeydew"
        self.trigger_regex = re.compile(rf"\<#{self.faq_channel_id}\>\s*(?P<numbers>(?:\d+(?:[\s\,]|(?:\s*and\s*)|(?:\s*or\s*))*)+)", re.IGNORECASE)
        self._faq_message_trigger_enabled = None
# endregion [Init]

# region [Properties]

    @property
    def faq_channel_id(self) -> int:
        return COGS_CONFIG.retrieve(self.config_name, 'faq_channel_id', typus=int, direct_fallback=673410398510383115)

    @property
    def faq_channel(self):
        channel_id = self.faq_channel_id
        return self.bot.channel_from_id(channel_id)

    @property
    def faq_name_table(self) -> dict:
        return loadjson(self.faq_name_data_file)

    @property
    def faq_message_trigger_enabled(self):
        if self._faq_message_trigger_enabled is None:
            self._faq_message_trigger_enabled = COGS_CONFIG.retrieve(self.config_name, 'faq_message_trigger_enabled', typus=bool, direct_fallback=False)
        return self._faq_message_trigger_enabled

# endregion [Properties]

# region [Setup]

    async def on_ready_setup(self):
        await super().on_ready_setup()
        FaqItem.bot = self.bot
        FaqItem.faq_channel = self.faq_channel
        FaqItem.question_parse_emoji = self.q_emoji
        FaqItem.answer_parse_emoji = self.a_emoji
        FaqItem.config_name = self.config_name
        await asyncio.to_thread(FaqItem.set_background_image)
        asyncio.create_task(self.collect_raw_faq_data())
        self.ready = True
        log.debug('setup for cog "%s" finished', str(self))

    async def update(self, typus: UpdateTypus):
        await super().update(typus=typus)
        if UpdateTypus.RECONNECT in typus:
            FaqItem.faq_channel = self.faq_channel
            await asyncio.to_thread(FaqItem.set_background_image)
            asyncio.create_task(self.collect_raw_faq_data())
        if UpdateTypus.CONFIG in typus:
            self._faq_message_trigger_enabled = None
        log.debug('cog "%s" was updated', str(self))


# endregion [Setup]

# region [Loops]

# endregion [Loops]

# region [Listener]

    @commands.Cog.listener(name='on_message')
    async def faq_message_trigger_listener(self, message: discord.Message):
        if self.completely_ready is False:
            return
        if self.faq_message_trigger_enabled is False:
            return
        content = message.content

        content_match = self.trigger_regex.search(content)
        if content_match:
            numbers = [number for number in map(lambda x: x.strip(), self.number_split_regex.split(content_match.group("numbers"))) if number and number.casefold() not in {'and', 'or'}]
            for number in numbers:
                try:
                    faq_number = int(number)
                    faq_item = self.faq_items.get(faq_number, None)
                    embed_data = await faq_item.to_embed_data()
                    reference = None if message.reference is None else message.reference.resolved
                    await message.channel.send(**embed_data, reference=reference, allowed_mentions=discord.AllowedMentions.none())
                except ValueError:
                    log.debug('unable to transform the string "%s" to int for "faq_message_trigger_listener"', number)
                await asyncio.sleep(0)

    @commands.Cog.listener(name='on_message')
    async def faq_message_added_listener(self, message):
        if self.completely_ready is False:
            return
        channel = message.channel
        if channel is self.faq_channel:
            asyncio.create_task(self.collect_raw_faq_data())

    @commands.Cog.listener(name='on_raw_message_delete')
    async def faq_message_deleted_listener(self, payload):
        if self.completely_ready is False:
            return
        channel = self.bot.get_channel(payload.channel_id)
        if channel is self.faq_channel:
            asyncio.create_task(self.collect_raw_faq_data())

    @commands.Cog.listener(name='on_raw_message_edit')
    async def faq_message_edited_listener(self, payload):
        if self.completely_ready is False:
            return
        channel = self.bot.get_channel(payload.channel_id)
        if channel is self.faq_channel:
            asyncio.create_task(self.collect_raw_faq_data())


# endregion [Listener]

# region [Commands]

    @auto_meta_info_group(aliases=['faq'], invoke_without_command=True, case_insensitive=True)
    @commands.cooldown(1, 5, commands.BucketType.channel)
    async def post_faq_by_number(self, ctx: commands.Context, faq_numbers: commands.Greedy[Union[int, str]]):
        """
        Posts an FAQ as an embed on request.

        Either as an normal message or as an reply, if the invoking message was also an reply.

        Args:
            faq_numbers (commands.Greedy[int]): minimum one faq number, no maximum,each seperated by one space (ie 14 12 3)

        Example:
            @AntiPetros post_faq_by_number 4 8 12

        Info:
            Deletes invoking message.
        """

        for faq_number in faq_numbers:
            if isinstance(faq_number, str):
                faq_number = faq_number.casefold()
                if faq_number not in self.faq_name_table:
                    await ctx.send(f'No FAQ Entry with the name {faq_number}')
                    continue
                faq_number = self.faq_name_table.get(faq_number)
            if faq_number not in self.faq_items:
                await ctx.send(f'No FAQ Entry with the number {faq_number}')
                continue
            faq_item = self.faq_items.get(faq_number)
            embed_data = await faq_item.to_embed_data()
            if ctx.message.reference is not None:
                try:
                    reference = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                    await ctx.send(**embed_data, reference=reference, allowed_mentions=discord.AllowedMentions.none())
                except discord.errors.InvalidArgument:
                    await ctx.send(**embed_data, allowed_mentions=discord.AllowedMentions.none())
                except discord.errors.HTTPException:
                    await ctx.send(**embed_data, allowed_mentions=discord.AllowedMentions.none())
            else:
                await ctx.send(**embed_data, allowed_mentions=discord.AllowedMentions.none())
        await ctx.message.delete()

    @post_faq_by_number.command(name="add_name")
    @allowed_channel_and_allowed_role()
    async def add_faq_name(self, ctx: commands.Context, faq_number: int, *, name: str):
        """
        Associates a name with an faq-number, so you can call the faq by name and not only by number.

        Args:
            faq_number (int): The faq-number you want to associate with the name.
            name (str): The name to give the faq-number, numbers can have multiple names.!NO SPACES ALLOWED!. Some names are restricted and names can't be only numbers.


        Example:
            @AntiPetros faq add_faq_name 1 myname
        """
        parent_command = self.bot.get_command("post_faq_by_number")
        name = name.casefold()
        if faq_number not in self.faq_items:
            await ctx.send(f'No FAQ Entry with the number {faq_number}')
            return

        if name in parent_command.aliases + [parent_command.name] or any(name in subcommand.aliases or name in subcommand.name for subcommand in parent_command.commands) or name.isnumeric() or ' ' in name:
            await ctx.send(f"name `{name}` is not allowed")
            return

        if name in self.faq_name_table:
            await ctx.send(f"name `{name}` is already assigned, please choose a different one")
            return

        faq_name_table_data = self.faq_name_table.copy()
        faq_name_table_data[name] = faq_number
        writejson(faq_name_table_data, self.faq_name_data_file)
        await ctx.send(f"name `{name}` was assigned to faq number `{faq_number}` succesfully")

    @post_faq_by_number.command(name="remove_name")
    @allowed_channel_and_allowed_role()
    async def remove_faq_name(self, ctx: commands.Context, name_to_remove: str):
        name_to_remove = name_to_remove.casefold()
        if name_to_remove not in self.faq_name_table:
            await ctx.send(f"name `{name_to_remove}` is not set to any faq item")
            return
        faq_name_table_data = self.faq_name_table.copy()
        del faq_name_table_data[name_to_remove]
        writejson(faq_name_table_data, self.faq_name_data_file)

        await ctx.send(f"name `{name_to_remove}` was removed as name for an faq item")

    @post_faq_by_number.command(name='list_names')
    @allowed_channel_and_allowed_role()
    async def list_faq_names(self, ctx: commands.Context):
        if self.faq_name_table:
            # TODO Important, make as paginated embed to user DM.
            text = '\n'.join([f"{key} -> {value}" for key, value in sorted(self.faq_name_table.items(), key=lambda x: x[1])])
            text = CodeBlock(text, 'fix')
        else:
            text = "No stored FAQ Names"
        await ctx.send(text, delete_after=120, allowed_mentions=discord.AllowedMentions.none())

# endregion [Commands]

# region [DataStorage]


# endregion [DataStorage]

# region [Embeds]


# endregion [Embeds]

# region [HelperMethods]

    async def collect_raw_faq_data(self):
        channel = self.faq_channel
        self.faq_items = {}
        async for message in channel.history(limit=None, oldest_first=True):
            while self.bot.is_ws_ratelimited() is True:
                await asyncio.sleep(5)
            content = message.content
            created_at = message.created_at
            jump_url = message.jump_url
            image = None
            if len(message.attachments) > 0:
                image = message.attachments[0]
            faq_item = FaqItem(content, created_at, jump_url, image)
            _ = await faq_item.get_number_thumbnail()
            self.faq_items[faq_item.number] = faq_item
            await asyncio.sleep(0)

        max_faq_number = max(self.faq_items)
        if all(_num in self.faq_items for _num in range(1, max_faq_number + 1)):
            log.info('FAQ items collected: %s', max_faq_number)
        else:
            raise KeyError(f"Not all FAQ Items where collected, missing: {', '.join(str(_num) for _num in range(1,max_faq_number+1) if _num not in self.faq_items)}")


# endregion [HelperMethods]

# region [SpecialMethods]


    def cog_check(self, ctx):
        return True

    async def cog_command_error(self, ctx, error):
        pass

    async def cog_before_invoke(self, ctx):
        pass

    async def cog_after_invoke(self, ctx):
        pass

    # def cog_unload(self):
    #     log.debug("Cog '%s' UNLOADED!", str(self))

    def __repr__(self):
        return f"{self.__class__.__name__}({self.bot.__class__.__name__})"

    def __str__(self):
        return self.__class__.__name__


# endregion [SpecialMethods]


def setup(bot):
    """
    Mandatory function to add the Cog to the bot.
    """
    bot.add_cog(FaqCog(bot))
