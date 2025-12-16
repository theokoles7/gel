"""# gel.registration.registries.command_registry

Command registry system implementation.
"""

__all__ = ["CommandRegistry"]

from argparse                   import ArgumentParser, _SubParsersAction
from typing                     import Any, Dict, Optional, override

from gel.configuration          import CommandConfig
from gel.registration.core      import EntryPointNotConfiguredError, Registry
from gel.registration.entries   import CommandEntry

class CommandRegistry(Registry):
    """# Command Registry System"""

    def __init__(self):
        """# Instantiate Command Registry."""
        super(CommandRegistry, self).__init__(id = "commands")

    # PROPERTIES ===================================================================================

    @override
    @property
    def entries(self) -> Dict[str, CommandEntry]:
        """# Registered Command Entries"""
        return self._entries_.copy()
    
    # METHODS ======================================================================================

    def dispatch(self,
        command_id: str,
        *args,
        **kwargs
    ) -> Any:
        """# Dispatch to Command Entry Point.

        ## Args:
            * command_id    (str):  Command to whom arguments are being dispatched.

        ## Raises:
            * EntryPointNotConfiguredError: If command entry was not configured with an entry point.

        ## Returns:
            * Any:  Data returned from command process.
        """
        # Query command entry.
        entry:  CommandEntry =  self.get_entry(key = command_id)

        # If entry was not registered with an entry point...
        if entry.entry_point is None:

            # Report error.
            raise EntryPointNotConfiguredError(entry_id = entry.id)
        
        # Debug action.
        self.__logger__.debug(f"Dispatching to {command_id} command: {kwargs}")

        # Dispatch to command entry point.
        return entry.entry_point(*args, **kwargs)
    
    @override
    def register_parsers(self,
        subparser:  _SubParsersAction,
        namespace:  Optional[str] =     None
    ) -> None:
        """# Register Argument Parsers.

        ## Args:
            * subparser (_SubParsersAction):    Command sub-parser of parent parser.
            * namespace (str | None):           If provided, only register parsers attributed to 
                                                this module namespace.
        """
        # Ensure that registry is loaded.
        self._ensure_loaded_()

        # For each registered command...
        for entry in self.entries.values():

            # If namespace is specified and entry is not attributed to it, skip it.
            if namespace is not None and entry.namespace != namespace: continue

            # If entry was registered with a parser handler...
            if entry.config is not None:

                # Debug action.
                self.__logger__.debug(f"Registering arguments for {entry.id}")
        
                # Create config instance (builds its full parser with all arguments).
                config: CommandConfig =             entry.config()
                
                # Create a new parser.
                parser: ArgumentParser =            subparser.add_parser(
                                                        name =          config.parser_id,
                                                        help =          config.parser_help,
                                                        description =   config.parser_help
                                                    )
                
                # Copy ALL the internals from the pre-built parser
                parser._actions =                   config.parser._actions
                parser._action_groups =             config.parser._action_groups
                parser._mutually_exclusive_groups = config.parser._mutually_exclusive_groups
                parser._defaults =                  config.parser._defaults
                parser._subparsers =                config.parser._subparsers
                parser._option_string_actions =     config.parser._option_string_actions

    # HELPERS ======================================================================================

    @override
    def _create_entry_(self, **kwargs) -> CommandEntry:
        """# Create Command Entry.

        ## Returns:
            * CommandEntry: New command entry instance.
        """
        return CommandEntry(**kwargs)
    
    # DUNDERS ======================================================================================

    @override
    def __getitem__(self,
        key:    str
    ) -> CommandEntry:
        """# Get Command Entry.

        ## Args:
            * key   (str):  ID of command whose entry is being queried.
            
        ## Raises:
            * KeyError: If entry is not registered.

        ## Returns:
            * CommandEntry: Command entry queried.
        """
        return self.get_entry(key = key)