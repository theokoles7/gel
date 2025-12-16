"""# gel.configuration.protocol

Abstract configuration & argument parsing component.
"""

__all__ = ["Config"]

from abc        import ABC, abstractmethod
from argparse   import ArgumentParser, Namespace, _SubParsersAction
from typing     import List, Optional, Sequence, Tuple

class Config(ABC):
    """# Abstract Configuration"""

    def __init__(self):
        """# Instantiate Configuration."""
        # Initialize parser.
        self._parser_:          ArgumentParser =    ArgumentParser(
                                                        prog =          self.parser_id,
                                                        description =   self.parser_help
                                                    )
        
        # If sub-parser properties are defined...
        if self.subparser_title is not None:

            # Initialize sub-parser.
            self._subparser_:   _SubParsersAction = self._parser_.add_subparsers(
                                                        title =         self.subparser_title,
                                                        dest =          self.subparser_dest,
                                                        help =          self.subparser_help,
                                                        description =   self.subparser_help
                                                    )
        
        # Define arguments.
        self._define_arguments_(parser = self._parser_)

    # PROPERTIES ===================================================================================

    @property
    def parser(self) -> ArgumentParser:
        """# Configuration Argument Parser"""
        return self._parser_
    
    @property
    @abstractmethod
    def parser_help(self) -> str:
        """# Parser's Description"""
        pass

    @property
    @abstractmethod
    def parser_id(self) -> str:
        """# Parser's ID/Name"""
        pass

    @property
    def subparser_dest(self) -> str:
        """# Sub-Parser's Destination"""
        return self.subparser_title.replace("-", "_")
    
    @property
    @abstractmethod
    def subparser_help(self) -> str:
        """# Sub-Parser's Description"""
        pass

    @property
    @abstractmethod
    def subparser_title(self) -> str:
        """# Sub-Parser's Title"""
        pass

    # METHODS ======================================================================================

    def parse_arguments(self,
        args:       Optional[Sequence[str]] =   None,
        namespace:  Optional[Namespace] =       None
    ) -> Tuple[Namespace, List[str]]:
        """# Parse Defined Arguments.

        ## Args:
            * args      (Sequence[str] | None): Sequence of system arguments.
            * namespace (Namespace | None):     Previously parsed arguments name space.

        ## Returns:
            * Namespace:    Mapping of known arguments & their values.
            * List[str]:    Sequence of leftover argument strings not recognized by parser.
        """
        return self._parser_.parse_known_args(args = args, namespace = namespace)
    
    @staticmethod
    def register_parser(
        cls:        "Config",
        subparser:  _SubParsersAction
    ) -> Tuple[ArgumentParser, _SubParsersAction]:
        """# Register Configuration Parser.

        ## Args:
            * cls       (Config):               This onfiguration class, being registered as 
                                                sub-command under another.
            * subparser (_SubParsersAction):    Sub-parser group of parent under which this 
                                                configuration will be registered.

        ## Returns:
            * ArgumentParser:       New argument parser, representing new sub-command.
            * _SubParsersAction:    Corresponding sub-parser of new sub-command parser.
        """
        # Instantiate this configuration class.
        config:         Config =            cls()

        # Register this configuration as a sub-command under the sub-parser group provided.
        parser:         ArgumentParser =    subparser.add_parser(
                                                name =          config.parser_id,
                                                help =          config.parser_help,
                                                description =   config.parser_help
                                            )
        
        # If sub-parser properties are defined...
        if config.subparser_title is not None:

            # Initialize sub-parser.
            subparser:  _SubParsersAction = parser.add_subparsers(
                                                title =         config.subparser_title,
                                                dest =          config.subparser_dest,
                                                help =          config.subparser_help,
                                                description =   config.subparser_help
                                            )
            
        # Define this configuration's arguments under new parser.
        config._define_arguments_(parser = parser)

        # Expose new parser & sub-parser.
        return parser, subparser

    # HELPERS ======================================================================================

    @abstractmethod
    def _define_arguments_(self,
        parser: ArgumentParser
    ) -> None:
        """# Define Parser Arguments.

        ## Args:
            * parser    (ArgumentParser):   Parser to whom arguments will be attributed.
        """
        pass