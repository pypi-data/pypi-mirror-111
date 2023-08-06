# * Third Party Imports -->
# * Third Party Imports --------------------------------------------------------------------------------->
from discord.ext.commands.errors import CommandError
import discord
from datetime import datetime
from typing import Any, TYPE_CHECKING, Union
from antipetros_discordbot.utility.misc import split_camel_case_string
from antipetros_discordbot.utility.discord_markdown_helper.general_markdown_helper import CodeBlock
from antipetros_discordbot.utility.discord_markdown_helper.special_characters import ListMarker
from discord.ext import commands
if TYPE_CHECKING:
    from antipetros_discordbot.engine.antipetros_bot import AntiPetrosBot
    from antipetros_discordbot.engine.replacements import AntiPetrosBaseContext


class AntiPetrosBaseError(Exception):
    pass


class ClassAttributesNotSetError(AntiPetrosBaseError):
    def __init__(self, missing_attr_name: str):
        self.missing_attr = missing_attr_name
        self.msg = f"mandatory class attribute '{self.missing_attr}' is None"
        super().__init__(self.msg)


class FaqParseError(AntiPetrosBaseError):
    pass


class FaqNumberParseError(FaqParseError):
    def __init__(self, raw_content: str, jump_url: str) -> None:
        self.raw_content = raw_content
        self.url = jump_url
        self.msg = f"unable to parse number from FAQ '{self.url}'"
        super().__init__(self.msg)


class FaqQuestionParseError(FaqParseError):
    def __init__(self, raw_content: str, jump_url: str) -> None:
        self.raw_content = raw_content
        self.url = jump_url
        self.msg = f"unable to parse question from FAQ '{self.url}'"
        super().__init__(self.msg)


class TeamMemberRoleNotFoundError(AntiPetrosBaseError):
    def __init__(self, team_name: str) -> None:
        self.team_name = team_name
        self.msg = f"No Member Role found for Team {self.team_name}"
        super().__init__(self.msg)


class FaqAnswerParseError(FaqParseError):
    def __init__(self, raw_content: str, jump_url: str) -> None:
        self.raw_content = raw_content
        self.url = jump_url
        self.msg = f"unable to parse answer from FAQ '{self.url}'"
        super().__init__(self.msg)


class NeededConfigValueMissing(AntiPetrosBaseError):
    def __init__(self, option_name, section_name, class_name) -> None:
        self.option_name = option_name
        self.section_name = section_name
        self.class_name = class_name
        self.msg = f"The option '{self.option_name}' was not set in section '{self.section_name}' and is needed for the class '{self.class_name}'"
        super().__init__(self.msg)


class NeededClassAttributeNotSet(AntiPetrosBaseError):
    def __init__(self, attr_name: str, class_name: str):
        self.attr_name = attr_name
        self.class_name = class_name
        self.msg = f"The class attribute '{self.attr_name}' was not set in the class '{self.class_name}'!"
        super().__init__(self.msg)


class MissingNeededAttributeError(AntiPetrosBaseError):
    def __init__(self, attr_name, cog) -> None:
        self.cog = cog
        self.attr_name = attr_name
        self.msg = f"Cog '{self.cog.qualified_name}' is missing the needed attribute '{self.attr_name}'"
        super().__init__(self.msg)


class CogNameNotCamelCaseError(AntiPetrosBaseError):
    pass


class FuzzyMatchError(AntiPetrosBaseError):
    def __init__(self, query, scorer, limit=None, data=None):
        self.query = query
        self.data = data
        self.scorer = scorer
        self.scorer_name = str(self.scorer).replace("<function ", "").split(' ')[0] if str(self.scorer).startswith('<') else str(self.scorer)
        self.limit = limit
        self.msg = f"Unable to fuzzy find a match for '{self.query}' with scorer '{self.scorer_name}'"
        if self.limit is not None:
            self.msg += f" and a limit of '{self.limit}'"
        super().__init__(self.msg)


class TokenError(AntiPetrosBaseError):
    __module__ = 'antipetros-discordbot'


class TokenMissingError(TokenError):
    def __init__(self, token_name):
        self.token_name = token_name
        self.msg = f"Token '{self.token_name}' is not set as env variable!"
        super().__init__(self.msg)


class DuplicateNameError(AntiPetrosBaseError):
    def __init__(self, name, container_name):
        self.msg = f"Name '{name}' is already in '{container_name}' and it does not allow duplicates."
        super().__init__(self.msg)


class BaseExtendedCommandError(CommandError):
    error_handler_name_prefix = '_handle'

    @classmethod
    @property
    def error_name(cls):
        return cls.__name__

    @classmethod
    @property
    def error_handler_name(cls):
        name = '_'.join([cls.error_handler_name_prefix, split_camel_case_string(cls.error_name, filler='_')]).casefold()
        return name


class MissingAttachmentError(BaseExtendedCommandError):

    def __init__(self, ctx, min_attachments: int):
        self.ctx = ctx
        self.command = self.ctx.command
        self.min_attachments = min_attachments
        self.attachments = self.ctx.message.attachments
        self.msg = f"This command requires at least '{str(self.min_attachments)}' attachments to work\nAmount attachments provided: '{str(len(self.attachments))}'."
        super().__init__(self.msg)


class WrongAttachmentTypeError(BaseExtendedCommandError):
    def __init__(self, ctx, attachment: discord.Attachment, allowed_content_types: set):
        self.ctx = ctx
        self.command = self.ctx.command
        self.attachment = attachment
        self.attachment_content_type = self.attachment.content_type
        self.allowed_content_types = allowed_content_types
        self.msg = f"The Attachment `{self.attachment.filename}` has the wrong content_type(`{self.attachment_content_type}`. Allowed content_types: {', '.join(self.allowed_content_types)}"
        super().__init__(self.msg)


class NotAllowedChannelError(BaseExtendedCommandError):
    def __init__(self, ctx, allowed_channels):
        self.ctx = ctx
        self.command_name = ctx.command
        self.alias_used = ctx.invoked_with
        self.channel_name = self.ctx.channel.name
        self.allowed_channels = allowed_channels
        self.msg = f"Sorry {ctx.author.name} I can't let you do that.\n\nThe command '{self.command_name}' (alias used: '{self.alias_used}') is not allowed in channel '{self.channel_name}'"
        super().__init__(self.msg)


class NotNecessaryRole(BaseExtendedCommandError):
    def __init__(self, ctx, allowed_roles):
        self.ctx = ctx
        self.allowed_roles = allowed_roles
        self.command_name = self.ctx.command
        self.alias_used = self.ctx.invoked_with
        self.channel_name = self.ctx.channel.name
        self.msg = f"You do not have the necessary Role to invoke the command '{self.command_name}' (alias used: '{self.alias_used}')"
        super().__init__(self.msg)


class IsNotTextChannelError(BaseExtendedCommandError):
    def __init__(self, ctx, channel_type):
        self.ctx = ctx
        self.command = self.ctx.command
        self.channel_type = channel_type
        self.msg = f"The command '{self.command.name}' is not allowed in DM's"
        super().__init__(self.msg)


class IsNotDMChannelError(BaseExtendedCommandError):
    def __init__(self, ctx, channel_type):
        self.ctx = ctx
        self.command = self.ctx.command
        self.channel_type = channel_type
        self.msg = f"The command '{self.command.name}' is not allowed outside of DM's"
        super().__init__(self.msg)


class NotNecessaryDmId(BaseExtendedCommandError):
    def __init__(self, ctx):
        self.ctx = ctx
        self.command_name = ctx.command
        self.alias_used = ctx.invoked_with
        self.msg = f"You do not have the necessary Permission to invoke the Dm command '{self.command_name}' (alias used: '{self.alias_used}')!"
        super().__init__(self.msg)


class NotAllowedMember(BaseExtendedCommandError):
    def __init__(self, allowed_member_ids: list):
        self.allowed_member_ids = allowed_member_ids
        self.msg = "You are not in the list of members that are allowed to use this command"
        super().__init__(self.msg)


class ParameterError(BaseExtendedCommandError):
    def __init__(self, parameter_name: str = None, parameter_value=None, error=None) -> None:
        self.parameter_name = parameter_name
        self.parameter_value = parameter_value
        self._error = error
        self.msg = f"'{self.parameter_value}' is not a valid input"
        if self.name is not None:
            self.msg += f" for '{self.parameter_name}'"
        super().__init__(self.msg)

    @property
    def error(self):
        if self._error is None:
            return self
        return self._error


class ParameterErrorWithPossibleParameter(BaseExtendedCommandError):
    def __init__(self, parameter_name: str, parameter_value, possible_parameter: list):
        self.parameter_name = parameter_name
        self.parameter_value = parameter_value
        self.possible_parameter = possible_parameter
        self.error_embed_title = f"'{self.parameter_value}' is not a valid input for '{self.parameter_name}'"
        self.error_embed_description = f"Possible values are:\n\n{CodeBlock(ListMarker.make_list([f'{item}' for item in self.possible_parameter], indent=1), 'python')}"
        self.msg = f"'{self.parameter_value}' is not a valid input for '{self.parameter_name}'\nPossible values are:\n" + "\n".join(f"\t{item}" for item in self.possible_parameter)
        super().__init__(self.msg)

    async def to_embed(self, ctx: Union[commands.Context, "AntiPetrosBaseContext"], bot: "AntiPetrosBot"):
        embed_data = await bot.make_generic_embed(title=self.error_embed_title, description=self.error_embed_description, thumbnail="error", author=ctx.author)
        return embed_data


class ParseDiceLineError(BaseExtendedCommandError):
    def __init__(self, statement) -> None:
        self.statement = statement
        self.msg = f"Unable to parse dice input '{self.statement}'"
        super().__init__(self.msg)


class CustomEmojiError(BaseExtendedCommandError):
    def __init__(self, custom_emoji_name: str, problem: str):
        self.custom_emoji_name = custom_emoji_name
        self.problem = problem
        self.msg = f"Error with custom emoji '{self.custom_emoji_name}': {self.problem}"
        super().__init__(self.msg)


class NameInUseError(BaseExtendedCommandError):
    def __init__(self, name: str, typus: str):
        self.name = name
        self.typus = typus
        self.msg = f"The Name {self.name} is already in use for {self.typus} items"
        super().__init__(self.msg)


class GithubRateLimitUsedUp(BaseExtendedCommandError):
    def __init__(self, reset_time: datetime):
        self.reset_time = reset_time
        self.msg = "Rate Limit for github is used up, this action is not usable until " + self.reset_time.strftime("%Y-%m-%d %H:%M:%S UTC") + ", as the rate-limit resets at that time!"
        super().__init__(self.msg)


class AskCanceledError(BaseExtendedCommandError):
    def __init__(self, ask_object, answer):
        self.ask_object = ask_object
        self.answer = answer
        self.msg = "Question was canceled by User"
        super().__init__(self.msg)


class AskTimeoutError(BaseExtendedCommandError):
    def __init__(self, ask_object):
        self.ask_object = ask_object
        self.msg = "No Answer received"
        super().__init__(self.msg)
