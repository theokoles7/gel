"""# gel.commands.version.main

Main process for `gel version` command.
"""

__all__ = ["version_entry_point"]

from gel.commands.version.__args__  import VersionConfig
from gel.registration               import register_command

@register_command(
    id =        "version",
    config =    VersionConfig
)
def version_entry_point(*args, **kwargs) -> None:
    """# Display Version Information."""
    # Import banner.
    from gel.utilities  import BANNER

    # Display banner.
    print(BANNER[1:])