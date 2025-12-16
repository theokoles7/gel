"""# gel.registration.entries.command_entry

Defines structure & utility of command registration entry.
"""

__all__ = ["CommandEntry"]

from typing                 import Callable

from gel.configuration      import CommandConfig
from gel.registration.core  import Entry

class CommandEntry(Entry):
    """# Command Registration Entry"""

    def __init__(self,
        id:             str,
        entry_point:    Callable,
        config:         CommandConfig,
        namespace:      str
    ):
        """# Instantiate Comand Registration Entry.
        
        ## Args:
            * id            (str):              Name of command.
            * entry_point   (Callable):         Command's main process entry point.
            * config        (CommandConfig):    Command's argument configuration.
            * namespace     (str):              Module whose entities command will be registered to.
        """
        # Initialize entry.
        super(CommandEntry, self).__init__(id = id, config = config, tags = [])

        # Define properties.
        self._entry_point_: Callable =  entry_point
        self._namespace_:   str =       namespace

    # PROPERTIES ===================================================================================

    @property
    def entry_point(self) -> Callable:
        """# Main Process Entry Point"""
        return self._entry_point_
    
    @property
    def namespace(self) -> str:
        """# Command's Namespace"""
        return self._namespace_