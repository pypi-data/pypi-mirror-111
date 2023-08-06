from discord.ext.commands import Command
from antipetros_discordbot.init_userdata.user_data_setup import ParaStorageKeeper

import discord
from discord.ext import commands, tasks
from discord.ext.commands import MinimalHelpCommand


APPDATA = ParaStorageKeeper.get_appdata()
BASE_CONFIG = ParaStorageKeeper.get_config('base_config')
COGS_CONFIG = ParaStorageKeeper.get_config('cogs_config')


class AntiPetrosBaseHelp(MinimalHelpCommand):
    pass
