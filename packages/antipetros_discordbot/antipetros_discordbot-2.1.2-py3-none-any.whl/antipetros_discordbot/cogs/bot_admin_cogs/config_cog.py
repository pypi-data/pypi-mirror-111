

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import os
import asyncio
from typing import List
from datetime import datetime, timezone
# * Third Party Imports --------------------------------------------------------------------------------->
import discord
from discord.ext import commands
from typing import TYPE_CHECKING
from asyncstdlib.builtins import map as amap
# * Gid Imports ----------------------------------------------------------------------------------------->
import gidlogger as glog

# * Local Imports --------------------------------------------------------------------------------------->
from antipetros_discordbot.utility.misc import delete_message_if_text_channel, loop_starter, make_other_source_code_images
from antipetros_discordbot.utility.checks import log_invoker, owner_or_admin
from antipetros_discordbot.utility.gidtools_functions import loadjson, pathmaker, readit
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper
from antipetros_discordbot.utility.enums import CogMetaStatus, UpdateTypus

from antipetros_discordbot.utility.converters import CommandConverter
from antipetros_discordbot.utility.discord_markdown_helper.special_characters import ListMarker, ZERO_WIDTH
from antipetros_discordbot.engine.replacements import AntiPetrosBaseCog, CommandCategory, RequiredFile, RequiredFolder, auto_meta_info_command, auto_meta_info_group

if TYPE_CHECKING:
    from antipetros_discordbot.engine.antipetros_bot import AntiPetrosBot

# endregion[Imports]

# region [TODO]


# TODO: get_logs command
# TODO: get_appdata_location command


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
THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))


# endregion[Constants]

# region [Helper]


# endregion [Helper]


class ConfigCog(AntiPetrosBaseCog, command_attrs={'hidden': True, 'categories': CommandCategory.META}):
    """
    Cog with commands to access and manipulate config files, also for changing command aliases.
    Almost all are only available in DM's

    commands are hidden from the help command.
    """
    # region [ClassAttributes]

    public = False
    meta_status = CogMetaStatus.OPEN_TODOS | CogMetaStatus.FEATURE_MISSING | CogMetaStatus.NEEDS_REFRACTORING
    required_config_data = {'base_config': {},
                            'cogs_config': {"notify_when_changed": "yes",
                                            "notify_via": "bot-testing",
                                            "notify_roles": 'call'}}
    config_dir = APPDATA['config']
    alias_file = pathmaker(APPDATA['fixed_data'], "documentation", "command_aliases.json")

    required_folder = [RequiredFolder(config_dir)]
    required_files = [RequiredFile(alias_file, {}, RequiredFile.FileType.JSON)]
    status_bool_string_map = {"1": "ENABLED",
                              "0": "DISABLED"}
# endregion[ClassAttributes]

# region [Init]

    def __init__(self, bot: "AntiPetrosBot"):
        super().__init__(bot)
        self.all_configs = [BASE_CONFIG, COGS_CONFIG]
        self.aliases = {}
        self.color = "orange"


# endregion[Init]

# region [Setup]

    async def on_ready_setup(self):
        """
        standard setup async method.
        The Bot calls this method on all cogs when he has succesfully connected.
        """
        await super().on_ready_setup()
        self.ready = True
        log.debug('setup for cog "%s" finished', str(self))

    async def update(self, typus: UpdateTypus):
        await super().update(typus=typus)
        log.debug('cog "%s" was updated', str(self))


# endregion [Setup]

# region [Properties]

    @property
    def existing_configs(self):
        existing_configs = {}
        for file in os.scandir(self.config_dir):
            if file.is_file() and file.name.endswith('.ini'):
                existing_configs[file.name.casefold().split('.')[0]] = pathmaker(file.path)
        return existing_configs

    @property
    def notify_when_changed(self):
        return COGS_CONFIG.retrieve(self.config_name, 'notify_when_changed', typus=bool, direct_fallback=False)

    @property
    def notify_via(self):
        return COGS_CONFIG.retrieve(self.config_name, 'notify_via', typus=str, direct_fallback='bot-testing')

    @property
    def notify_role_names(self):
        return COGS_CONFIG.retrieve(self.config_name, 'notify_roles', typus=List[str], direct_fallback=['admin'])

    @property
    def all_alias_names(self):
        _out = []
        for key, value in loadjson(self.alias_file).items():
            _out.append(key)
            _out += value
        return set(_out)
# endregion[Properties]

# region [HelperMethods]

    async def get_notify_roles(self):
        return [self.bot.role_from_string(role_name) for role_name in self.notify_role_names]

    async def send_config_file(self, ctx, config_name):
        config_path = self.existing_configs.get(config_name)
        modified = datetime.fromtimestamp(os.stat(config_path).st_mtime).astimezone(timezone.utc)
        image = await make_other_source_code_images(readit(config_path), 'ini', 'dracula')

        embed_data = await self.bot.make_generic_embed(title=config_name.upper(),
                                                       footer={'text': "last modified:"},
                                                       timestamp=modified,
                                                       author='bot_author',
                                                       thumbnail='config',
                                                       image=image)
        await ctx.send(**embed_data)
        await ctx.send(file=discord.File(config_path))


# endregion [HelperMethods]

# region [Commands]


    @auto_meta_info_group(case_insensitive=True, categories=[CommandCategory.META], invoke_without_command=False)
    @owner_or_admin()
    async def change_prefix(self, ctx: commands.Context):
        """
        Group command to interact with Bot prefixes.

        Example:
            @AntiPetros change_prefix add -?-

        Info:
            Can not be invoked on its own and has to be used with one of the sub-commands
        """

    @change_prefix.command(name='add')
    @owner_or_admin()
    async def add_prefix(self, ctx: commands.Context, *, new_prefix: str):
        """
        Adds a new prefix to the bot, with which he can be invoked.

        Prefix can not be an duplicate of an already existing one.

        Args:
            new_prefix (str): The new prefix, can not contain spaces, but can be an std-emoji. No custom emojis.

        Example:
            @AntiPetros change_prefix add ??


        Info:
            It is best to only use lowercase letters if letters or words are used.
        """
        non_mention_prefixes = list(set(BASE_CONFIG.retrieve('prefix', 'command_prefix', typus=List[str], direct_fallback=[])))
        if ' ' in new_prefix:
            await ctx.send(embed=await self.bot.make_cancelled_embed(title='change_prefix add Error', msg='A prefix can not contain spaces!'))
            return

        if new_prefix in non_mention_prefixes:
            embed_extra_info = f"Current Prefixes:\n{ZERO_WIDTH}\n```diff\n" + ListMarker.make_list(non_mention_prefixes) + '\n```'
            await ctx.send(embed=await self.bot.make_cancelled_embed(title='change_prefix add Error', msg=f'Prefix `{new_prefix}` is already set as prefix for the bot!', extra=embed_extra_info))
            return

        new_prefixes = non_mention_prefixes + [new_prefix]
        BASE_CONFIG.set('prefix', 'command_prefix', ', '.join(new_prefixes))
        await ctx.send(f"Prefix `{new_prefix}` was added to the bots Prefixes\nCurrent Prefixes:\n```diff\n" + '\n'.join(new_prefixes) + '\n```')

    @change_prefix.command(name='remove')
    @owner_or_admin()
    async def remove_prefix(self, ctx: commands.Context, *, prefix_to_remove: str):
        """
        Removes an existing prefix from the bot and makes it so the bot cant be invoked by it anymore.


        Args:
            prefix_to_remove (str): The prefix to remove, has to be an existing prefix
        """
        non_mention_prefixes = list(set(BASE_CONFIG.retrieve('prefix', 'command_prefix', typus=List[str], direct_fallback=[])))
        if prefix_to_remove not in non_mention_prefixes:
            embed_extra_info = f"Current Prefixes:\n{ZERO_WIDTH}\n```diff\n" + ListMarker.make_list(non_mention_prefixes) + '\n```'
            await ctx.send(embed=await self.bot.make_cancelled_embed(title='change_prefix remove Error', msg=f"Prefix `{prefix_to_remove}` is not a Prefix of the bot", extra=embed_extra_info))
            return

        new_prefixes = non_mention_prefixes.copy()
        new_prefixes.remove(prefix_to_remove)
        BASE_CONFIG.set('prefix', 'command_prefix', ', '.join(new_prefixes))
        await ctx.send(f"Prefix `{prefix_to_remove}` was removed from the bot Prefixes\nCurrent Prefixes:\n```diff\n" + '\n'.join(new_prefixes) + '\n```')

    @auto_meta_info_command()
    @ owner_or_admin()
    @log_invoker(log, 'info')
    async def list_configs(self, ctx):
        """
        Provides a list of all existing configs-files.

        The names are without the extension, and show up like they are needed as input for other config commands.

        Example:
            @AntiPetros list_configs
        """
        embed_data = await self.bot.make_generic_embed(title=f'Configs for {self.bot.display_name}',
                                                       description='```diff\n' + '\n'.join(self.existing_configs.keys()) + '\n```',
                                                       author='bot_author',
                                                       thumbnail='config')
        await ctx.reply(**embed_data)

    @ auto_meta_info_command()
    @ owner_or_admin()
    async def config_request(self, ctx, config_name: str = 'all'):
        """
        Returns a Config file as and attachment, with additional info in an embed.

        Args:
            config_name (str, optional): Name of the config, or 'all' for all configs. Defaults to 'all'.

        Example:
            @AntiPetros config_request cogs_config
        """
        if '.' in config_name:
            config_name = config_name.split('.')[0]
        mod_config_name = config_name.casefold()
        if mod_config_name not in list(self.existing_configs) + ['all']:
            await ctx.send(f'No Config named `{config_name}`, aborting!')
            return

        if config_name == 'all':
            for name in self.existing_configs:
                await self.send_config_file(ctx, name)
                await asyncio.sleep(0.5)
        else:
            await self.send_config_file(ctx, config_name)

    @ auto_meta_info_command()
    @ owner_or_admin()
    @ log_invoker(log, 'critical')
    async def add_alias(self, ctx: commands.Context, command: CommandConverter, new_alias: str):
        """
        Adds an alias for a command.

        Alias has to be unique and not spaces.

        Args:
            command_name (str): name of the command
            alias (str): the new alias.

        Example:
            @AntiPetros add_alias flip_coin flip_it
        """
        new_alias = new_alias.casefold()
        if new_alias in self.all_alias_names:
            await ctx.send(f'Alias `{new_alias}` is already in use, either on this command or any other. Cannot be set as alias, aborting!')
            return
        add_success = await command.set_alias(new_alias)
        if add_success is True:
            await ctx.send(f"successfully added `{new_alias}` to the command aliases of `{command.name}`")
            await self.bot.creator.send(f"A new alias was set by `{ctx.author.name}`\n**Command:** `{command.name}`\n**New Alias:** `{new_alias}`")
        else:
            await ctx.send(f"error with adding alias `{new_alias}` to `{command.name}`, alias was **NOT** added!")

    @auto_meta_info_command()
    @commands.is_owner()
    async def toggle_config_access_logging(self, ctx: commands.Context):
        current = os.getenv('LOG_CONFIG_RETRIEVE')
        new = '0' if current == "1" else "1"
        os.environ['LOG_CONFIG_RETRIEVE'] = new
        as_text = 'OFF' if new == "0" else "ON"
        await ctx.send(f"Config access loggin was turned {as_text}", delete_after=30)
        await delete_message_if_text_channel(ctx)

# endregion [Commands]

# region [Helper]

    async def notify(self, event):
        roles = await self.get_notify_roles()
        embed_data = await event.as_embed_message()
        if self.notify_via.casefold() == 'dm':
            member_to_notify = list({role.members for role in roles})
            for member in member_to_notify:
                await member.send(**embed_data)

        else:
            channel = self.bot.channel_from_name(self.notify_via)
            await channel.send(content=' '.join(role.mention for role in roles), **embed_data)


# endregion[Helper]

# region [SpecialMethods]


    def __repr__(self):
        return f"{self.__class__.__name__}({self.bot.user.name})"

    def __str__(self):
        return self.__class__.__name__

    # def cog_unload(self):
    #     log.debug("Cog '%s' UNLOADED!", str(self))
# endregion [SpecialMethods]


def setup(bot):
    """
    Mandatory function to add the Cog to the bot.
    """
    bot.add_cog(ConfigCog(bot))
