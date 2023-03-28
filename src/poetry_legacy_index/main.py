from __future__ import annotations

from typing import TYPE_CHECKING

from poetry.console.commands.group_command import GroupCommand
from poetry.plugins.application_plugin import ApplicationPlugin

if TYPE_CHECKING:
    from poetry.console.application import Application
    from poetry.console.commands.command import Command


class LegacyIndexFixCommand(GroupCommand):
    name = "legacy-index-fix"
    description = "Fixes legacy index wheel downloads during metadata collection."
    options = []

    def handle(self) -> int:
        import importlib.util
        import inspect
        from pathlib import Path

        # get the path to the poetry package
        repo_spec = importlib.util.find_spec("poetry.repositories.http_repository")
        patch_file_path = Path(repo_spec.origin).resolve()

        # prepare the file content
        with patch_file_path.open("r") as f:
            content = f.read()

        # check if the file is already patched
        if FILTER_WHEELS_CALL in content:
            self.line("Legacy repository patch already applied.", "debug")
            return

        # append the filter_wheels function
        content += "\n\n"
        content += inspect.getsource(filter_wheels)

        # replace the function call
        content = content.replace(FILTER_WHEELS_CALL_TO_REPLACE, FILTER_WHEELS_CALL)

        # write the patched file
        with patch_file_path.open("w") as f:
            f.write(content)

        self.line(f"Successfully patched {patch_file_path}", "success")
        self.line_error("Please clear the poetry cache and try again.", "warning")

        return 0


class ExportApplicatioLegacyIndexFixPlugin(ApplicationPlugin):
    @property
    def commands(self) -> list[type[Command]]:
        return [LegacyIndexFixCommand]

    def activate(self, application: Application) -> None:
        # Running the command automatically without explicitly being called.
        # This is because the author always needs this fix to be applied.

        # If you're checking this code out to get inspiration
        # for your own plugins: DON'T DO THIS!
        command = LegacyIndexFixCommand()
        command.set_application(application)
        command.execute(io=application._io)

        super().activate(application=application)


# filter wheels func to be appended at the end of the file
def filter_wheels(wheels):
    """Filter out wheels that are not compatible with the current platform."""
    import sys
    from pathlib import Path

    from poetry.utils.env import SystemEnv

    env = SystemEnv(Path(sys.executable))
    markers = env.get_marker_env()
    filtered_wheels = wheels
    platform_wheels = [
        w for w in filtered_wheels if markers.get("sys_platform", "") in w
    ]
    if platform_wheels:
        filtered_wheels = platform_wheels
    machine_wheels = [
        w for w in filtered_wheels if markers.get("platform_machine", "") in w
    ]
    if machine_wheels:
        filtered_wheels = machine_wheels

    return filtered_wheels


# The function call to filter the wheels
FILTER_WHEELS_CALL = "first_wheel = filter_wheels(platform_specific_wheels)[0]"

# The code to be replaced by the filter_wheels_call
FILTER_WHEELS_CALL_TO_REPLACE = "first_wheel = platform_specific_wheels[0]"
