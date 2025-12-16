"""# gel.registration.core.entry

Abstract registration entry implementation.
"""

__all__ = ["Entry"]

from abc                                import ABC
from argparse                           import _SubParsersAction
from logging                            import Logger
from typing                             import List, Optional

from gel.configuration                  import Config
from gel.registration.core.exceptions   import ParserNotConfiguredError
from gel.utilities                      import get_logger

class Entry(ABC):
    """# Abstract Registration Entry."""

    def __init__(self,
        id:     str,
        config: Optional[Config] =  None,
        tags:   List[str] =         []
    ):
        """# Instantiate Registration Entry.

        ## Args:
            * id        (str):              Entry ID.
            * config    (Config | None):    Argument parser handler. Defaults to None.
            * tags      (List[str]):        Tags that describe entry's taxonomy. Defaults to [].
        """
        # Initialize logger.
        self.__logger__:    Logger =            get_logger(f"{id}-registration-entry")

        # Define properties.
        self._id_:          str =               id
        self._tags_:        List[str] =         tags
        self._config_:      Optional[Config] =  config

        # Debug registration.
        self.__logger__.debug(f"Registered {self}")

    # PROPERTIES ===================================================================================

    @property
    def id(self) -> str:
        """# Entry ID"""
        return self._id_
    
    @property
    def config(self) -> Optional[Config]:
        """# Entry Argument Parser Handler"""
        return self._config_
    
    @property
    def tags(self) -> List[str]:
        """# Entry Taxonomy Tags"""
        return self._tags_
    
    # METHODS ======================================================================================

    def contains_tag(self,
        tag:    str
    ) -> bool:
        """# Entry Contains Tag?

        ## Args:
            * tag   (str):  Taxonomy tag being queried.

        ## Returns:
            * bool: True if entry contains tag.
        """
        # Debug verification.
        self.__logger__.debug(f"{self} entry has tag {tag}? {tag in self._tags_}")

        # Query tag.
        return tag in self._tags_
    
    def register_parser(self,
        subparser:  _SubParsersAction
    ) -> None:
        """# Register Entry Argument Parser.

        ## Args:
            * subparser (_SubParsersAction):    Parent's sub-parser.
        """
        # If entry was not registered with parser handler, report error.
        if self._config_ is None: raise ParserNotConfiguredError(entry_id = self._id_)

        # Debug action.
        self.__logger__.debug(f"Registering {self} parser under {subparser.dest}")

        # Register parser.
        self._config_.register_parser(cls = self._config_, subparser = subparser)

    # DUNDERS ======================================================================================

    def __repr__(self) -> str:
        """# Entry Object Representation"""
        return f"""<{self._id_.capitalize()}Entry(tags = {",".join(self._tags_)})>"""