"""# gel.configuration.command_config

Configuration & argument parsing component for commands.
"""

__all__ = ["CommandConfig"]

from typing                     import Optional, override

from gel.configuration.protocol import Config

class CommandConfig(Config):
    """# Abstract Command Configuration"""

    def __init__(self,
        name:               str,
        help:               str,
        subparser_title:    Optional[str] = None,
        subparser_help:     Optional[str] = None
    ):
        """# Instantiate Command Configuration.

        ## Args:
            * name              (str):          Command identifier.
            * help              (str):          Description of command's purpose.
            * subparser_help    (str | None):   Description of sub-command purpose.
            * subparser_title   (str | None):   Name attributed to sub-command objects.
        """
        # Define properties.
        self._name_:            str =           name
        self._help_:            str =           help
        self._subparser_help_:  Optional[str] = subparser_help
        self._subparser_title_: Optional[str] = subparser_title
        
        # Initialize configuration.
        super(CommandConfig, self).__init__()
        
    # PROPERTIES ===================================================================================
    
    @override
    @property
    def parser_help(self) -> str:
        """# Command Description"""
        return self._help_
    
    @override
    @property
    def parser_id(self) -> str:
        """# Command Identifier"""
        return self._name_.lower()
    
    @override
    @property
    def subparser_help(self) -> Optional[str]:
        """# Sub-Parser's Description"""
        return self._subparser_help_
    
    @override
    @property
    def subparser_title(self) -> Optional[str]:
        """# Sub-Parser's Title"""
        return self._subparser_title_