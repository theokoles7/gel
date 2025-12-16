"""# gel.registration.core.registry

Abstract registry implementation.
"""

__all__ = ["Registry"]

from abc                                import ABC, abstractmethod
from argparse                           import ArgumentParser, _SubParsersAction
from logging                            import Logger
from typing                             import Dict, List

from gel.configuration                  import Config
from gel.registration.core.entry        import Entry
from gel.registration.core.exceptions   import DuplicateEntryError, EntryNotFoundError
from gel.registration.core.types        import EntryType
from gel.utilities                      import get_logger

class Registry(ABC):
    """# Abstract Registry"""

    def __init__(self,
        id: str
    ):
        """# Instantiate Registry.

        ## Args:
            * id    (str):  Registry ID.
        """
        # Initialize logger.
        self.__logger__:    Logger =            get_logger(f"{id}-registry")

        # Define properties.
        self._id_:          str =               id
        self._entries_:     Dict[str, Entry] =  {}
        self._loaded_:      bool =              False

    # PROPERTIES ===================================================================================

    @property
    def entries(self) -> Dict[str, Entry]:
        """# Registry Entries"""
        return self._entries_.copy()
    
    @property
    def id(self) -> str:
        """# Registry ID"""
        return self._id_
    
    @property
    def is_loaded(self) -> bool:
        """# Registry has been Loaded?"""
        return self._loaded_
    
    # METHODS ======================================================================================

    def get_entry(self,
        key:    str
    ) -> Entry:
        """# Get Entry.

        ## Args:
            * key   (str):  ID of entry being queried.

        ## Raises:
            * EntryNotFoundError:   If entry is not registered.

        ## Returns:
            * Entry:    Entry queried.
        """
        # Ensure that registry is loaded.
        self._ensure_loaded_()

        # If key is not registered...
        if key not in self._entries_:

            # Report error.
            raise EntryNotFoundError(entry_id = key, registry_id = self._id_)
        
        # Debug action.
        self.__logger__.debug(f"Entry queried: {key}")

        # Provide requested entry.
        return self._entries_[key]
    
    def list(self,
        filter_by:  List[str] = []
    ) -> List[str]:
        """# List Entries.

        ## Args:
            * filter_by (List[str]):    Tags by which entries will be filtered. Defaults to [].

        ## Returns:
            * List[str]:    List of [filtered] entries.
        """
        # Ensure that registry is loaded.
        self._ensure_loaded_()

        # Debug action.
        self.__logger__.debug(f"Listing {self._id_} entries filtered by {filter_by}")

        # If no filter is provided, return all entries.
        if len(filter_by) == 0: return list(self._entries_.keys())

        # Otherwise, return filtered entries.
        return  [
                    id 
                    for id, entry
                    in self._entries_.items()
                    if  all(
                            tag in entry.tags
                            for tag
                            in filter_by
                        )
                ]
    
    def load_all(self) -> None:
        """# Load All Registered Modules."""
        # If registry is already loaded, no-op.
        if self.is_loaded: return

        # Otherwise, import all modules.
        self._import_all_modules_()

        # Debug action.
        self.__logger__.debug(f"{self._id_} registry has been loaded")

        # Update status.
        self._loaded_:  bool =  True

    def register(self,
        id: str,
        **kwargs
    ) -> None:
        """# Register Entry.

        ## Args:
            * id    (str):  ID of entry.

        ## Raises:
            * DuplicateEntryError:  If entry is already registered.
        """
        # If entry is already registered...
        if id in self._entries_:

            # Report error.
            raise DuplicateEntryError(entry_id = id, registry_id = self._id_)
        
        # Debug action.
        self.__logger__.debug(f"Registering {id} with arguments: {kwargs}")

        # Create & register entry.
        self._entries_[id] = self._create_entry_(id = id, **kwargs)

    def register_parsers(self,
        subparser:  _SubParsersAction
    ) -> None:
        """# Register Argument Parsers.

        ## Args:
            * subparser (_SubParsersAction):    Command sub-parser of parent parser.
        """
        # Ensure registry is loaded.
        self._ensure_loaded_()

        # For each registered entry...
        for entry in self._entries_.values():

            # If entry was registered with a parser handler...
            if entry.config is not None:

                # Debug action.
                self.__logger__.debug(f"Registering arguments for {entry.id}")
        
                # Create config instance (builds its full parser with all arguments).
                config: Config =                    entry.config()
                
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

    @abstractmethod
    def _create_entry_(self, **kwargs) -> EntryType:
        """# Create Entry.
        
        Factory method to create the appropriate entry type for this registry.

        ## Returns:
            * EntryType:    New entry instance.
        """
        pass

    def _ensure_loaded_(self) -> None:
        """# Ensure Registry is Loaded."""
        if not self.is_loaded: self.load_all()

    def _import_all_modules_(self) -> None:
        """# Import All Modules."""
        from importlib  import import_module
        from pkgutil    import walk_packages
        from types      import ModuleType
        
        try:# Import the main package to get its path.
            package:    ModuleType =    import_module(f"gel.{self._id_}")
        
        # If import error occurs...
        except ImportError as e:
            
            # Warn of complications.
            self.__logger__.warning(f"Could not import package gel.{self._id_}: {e}")
            return
        
        # Debug action.
        self.__logger__.debug(f"Walking package: {package}")
        
        try:# For each module within package...
            for _, module, _ in walk_packages(
                path =      package.__path__,
                prefix =    f"gel.{self._id_}.",
                onerror =   lambda x: None
            ):
                try:# Attempt import of module.
                    import_module(name = module)
                    
                    # Debug action.
                    self.__logger__.debug(f"Walk of {module} complete")
                    
                # If import error occurs.
                except ImportError as e:
                    
                    # Warn of complications.
                    self.__logger__.warning(f"Error importing {module} module: {e}")
                    
        # If a package cannot be imported...
        except ImportError as e:
            
            # Warn of error.
            self.__logger__.warning(f"Error importing {package} package: {e}")

    # DUNDERS ======================================================================================

    def __contains__(self,
        key:    str
    ) -> bool:
        """# Registry Contains Entry?

        True if entry key is registered.
        """
        return key in self._entries_
    
    def __getitem__(self,
        key:    str
    ) -> Entry:
        """# Get Entry.

        ## Args:
            * key   (str):  Key of entry being queried.
            
        ## Raises:
            * KeyError: If entry is not registered.

        ## Returns:
            * Entry:    Entry queried.
        """
        return self.get_entry(key = key)
    
    def __len__(self) -> int:
        """# Number of Registered Entries"""
        return len(self._entries_)
    
    def __repr__(self) -> str:
        """# Registry Object Representation"""
        return f"""<{self._id_.capitalize()}Registry({len(self._entries_)} entries)>"""