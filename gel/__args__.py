"""# gel.args

Argument definitions & parsing for GEL application.
"""

__all__ = ["parse_gel_arguments"]

from argparse           import _ArgumentGroup, ArgumentParser, Namespace, _SubParsersAction

from gel.registration   import COMMAND_REGISTRY

def parse_gel_arguments() -> Namespace:
    """# Parse GEL Arguments.

    ## Returns:
        * Namespace:    Mapping of arguments and their values.
    """
    # Initialize parser.
    parser:     ArgumentParser =    ArgumentParser(
                                        prog =          "gel",
                                        description =   """Gabriel's Everything Library"""
                                    )
    
    # Initialize sub-parser.
    subparser:  _SubParsersAction = parser.add_subparsers(
                                        title =         "gel-command",
                                        dest =          "gel_command",
                                        help =          """GEL command being executed.""",
                                        description =   """GEL command being executed."""
                                    )
    
    # +============================================================================================+
    # | BEGIN ARGUMENTS                                                                            |
    # +============================================================================================+

    # LOGGING ======================================================================================
    logging:    _ArgumentGroup =    parser.add_argument_group(
                                        title =             "Logging",
                                        description =       "Logging configuration."    
                                    )

    logging.add_argument(
        "--logging-level",
        dest =              "logging_level",
        type =              str,
        choices =           ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "NOTSET"],
        default =           "INFO",
        help =              """Minimum logging level (DEBUG < INFO < WARNING < ERROR < CRITICAL). 
                            Defaults to "INFO"."""
    )

    logging.add_argument(
        "--logging-path",
        dest =              "logging_path",
        type =              str,
        default =           "logs",
        help =              """Path at which logs will be written. Defaults to "./logs/"."""
    )
    
    # +============================================================================================+
    # | END ARGUMENTS                                                                              |
    # +============================================================================================+

    # Register GEL commands.
    COMMAND_REGISTRY.register_parsers(subparser = subparser, namespace = "gel")

    # Parse arguments.
    return parser.parse_args()