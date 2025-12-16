"""# gel.registration

Registration system & related utilities.
"""

__all__ =   [
                # Registries
                "COMMAND_REGISTRY",

                # Decorators
                "register_command",
            ]

from gel.registration.decorators    import *
from gel.registration.registries    import *

# Instantiate registries.
COMMAND_REGISTRY:   CommandRegistry =   CommandRegistry()