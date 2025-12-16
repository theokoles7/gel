"""# gel.registration.decorators

Function annotation decorators for registration of components.
"""

__all__ =   [
                "register_command",
            ]

from typing             import Callable

from gel.configuration  import CommandConfig


def register_command(
    id:     str,
    config: CommandConfig
) -> Callable:
    """# Register Command.

    ## Args:
        * id        (str):      Name of command.
        * config    (Config):   Command's argument configuration.

    ## Returns:
        * Callable: Registration decorator.
    """
    # Define decorator.
    def decorator(
        entry_point:    Callable
    ) -> Callable:
        """# Agent Command Registration Decorator

        ## Args:
            * entry_point   (Callable): Command's main process entry point.
        """
        # Load registry.
        from gel.registration import COMMAND_REGISTRY
        
        # Register command.
        COMMAND_REGISTRY.register(
            id =            id,
            entry_point =   entry_point,
            config =        config,
            namespace =     "gel"
        )
        
        # Return entry point.
        return entry_point
    
    # Expose decorator.
    return decorator