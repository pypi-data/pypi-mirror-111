"""
[summary]

[extended_summary]
"""

# region [Imports]
from typing import Iterable, Callable, Optional, Any, AnyStr, Awaitable, Coroutine, ContextManager, TYPE_CHECKING, Union, Iterator
import gc
import os
import unicodedata
import discord
from discord.ext import commands, tasks
import gidlogger as glog
from .base_group import AntiPetrosBaseGroup
from .base_command import AntiPetrosBaseCommand

if TYPE_CHECKING:
    from antipetros_discordbot.engine.replacements import CommandCategory

# endregion[Imports]

# region [TODO]


# endregion [TODO]

# region [AppUserData]


# endregion [AppUserData]

# region [Logging]

log = glog.aux_logger(__name__)
log.info(glog.imported(__name__))

# endregion[Logging]

# region [Constants]

THIS_FILE_DIR = os.path.abspath(os.path.dirname(__file__))

# endregion[Constants]


def auto_meta_info_command(name=None,
                           cls=None,
                           aliases: Iterable[str] = None,
                           categories: list["CommandCategory"] = None,
                           only_debug: bool = None,
                           clear_invocation: bool = None,
                           experimental: bool = None,
                           confirm_command_received: bool = None,
                           logged: bool = None,
                           force_check_rate_limited: bool = None,
                           rest_is_raw: bool = None,
                           ** attrs):
    # TODO: check if the default values of the arguments really have to be None!
    """
    EXTENDED_BY_GIDDI
    -----------------
    Automatically gets the following attributes, if not provided or additional to provided:
    - creates default aliases and retrieves custom aliases.

    Base Docstring
    ---------------
    A decorator that transforms a function into a :class:`.Command`
    or if called with :func:`.group`, :class:`.Group`.

    By default the ``help`` attribute is received automatically from the
    docstring of the function and is cleaned up with the use of
    ``inspect.cleandoc``. If the docstring is ``bytes``, then it is decoded
    into :class:`str` using utf-8 encoding.

    All checks added using the :func:`.check` & co. decorators are added into
    the function. There is no way to supply your own checks through this
    decorator.

    Parameters
    -----------
    name: :class:`str`
        The name to create the command with. By default this uses the
        function name unchanged.
    cls
        The class to construct with. By default this is :class:`.Command`.
        You usually do not change this.
    attrs
        Keyword arguments to pass into the construction of the class denoted
        by ``cls``.

    Raises
    -------
    TypeError
        If the function is not a coroutine or is already a command.
    """
    if cls is None:
        cls = AntiPetrosBaseCommand
    if aliases is not None:
        attrs['aliases'] = aliases
    if categories is not None:
        attrs['categories'] = categories
    if only_debug is not None:
        attrs['only_debug'] = only_debug
    if clear_invocation is not None:
        attrs['clear_invocation'] = clear_invocation
    if experimental is not None:
        attrs['experimental'] = experimental
    if confirm_command_received is not None:
        attrs['confirm_command_received'] = confirm_command_received
    if logged is not None:
        attrs['logged'] = logged
    if force_check_rate_limited is not None:
        attrs['force_check_rate_limited'] = force_check_rate_limited
    if rest_is_raw is not None:
        attrs['rest_is_raw'] = rest_is_raw

    def decorator(func):

        return cls(func, name=name, **attrs)

    return decorator


def auto_meta_info_group(name=None, **attrs):
    """EXTENDED_BY_GIDDI
    -----------------
    A decorator that transforms a function into a :class:`.Group`.

    This is similar to the :func:`.command` decorator but the ``cls``
    parameter is set to :class:`Group` by default.

    .. versionchanged:: 1.1
        The ``cls`` parameter can now be passed.
    """

    attrs.setdefault('cls', AntiPetrosBaseGroup)
    return auto_meta_info_command(name=name, **attrs)
# region[Main_Exec]


if __name__ == '__main__':
    pass

# endregion[Main_Exec]
