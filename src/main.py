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
        print("Running legacy index fix command.")
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
        command.handle()

        super().activate(application=application)
