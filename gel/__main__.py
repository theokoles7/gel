"""# gel.main

Primary application process.
"""

__all__ = ["gel_entry_point"]

from argparse           import Namespace
from logging            import Logger
from typing             import Any

def gel_entry_point(*args, **kwargs) -> Any:
    """# Execute GEL Application.

    ## Returns:
        * Any:  Data returned from subprocess(es).
    """
    from gel.__args__       import parse_gel_arguments
    from gel.registration   import COMMAND_REGISTRY
    from gel.utilities      import configure_logger

    # Parse arguments.
    arguments:  Namespace = parse_gel_arguments()

    # Initialize logger.
    logger:     Logger =    configure_logger(
                                logging_level = arguments.logging_level,
                                logging_path =  arguments.logging_path
                            )
    
    # Debug arguments.
    logger.debug(f"GEL arguments: {vars(arguments)}")

    try:# Dispatch command.
        COMMAND_REGISTRY.dispatch(command_id = arguments.gel_command, **vars(arguments))

    # Catch wildcard errors.
    except Exception as e:  logger.critical(f"Unexpected error: {e}", exc_info = True)

    # Exit gracefully.
    finally:                logger.debug("Exiting...")


if __name__ == "__main__": gel_entry_point()