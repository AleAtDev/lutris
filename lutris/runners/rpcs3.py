# Standard Library
from gettext import gettext as _

from lutris.exceptions import MissingGameExecutableError
# Lutris Modules
from lutris.runners.runner import Runner
from lutris.util import system


class rpcs3(Runner):
    human_name = _("RPCS3")
    description = _("PlayStation 3 emulator")
    platforms = [_("Sony PlayStation 3")]
    runnable_alone = True
    runner_executable = "rpcs3/rpcs3"
    flatpak_id = "net.rpcs3.RPCS3"
    game_options = [
        {
            "option": "main_file",
            "type": "file",
            "default_path": "game_path",
            "label": _("Path to EBOOT.BIN"),
        }
    ]
    runner_options = [{"option": "nogui", "type": "bool", "label": _("No GUI"), "default": False}]

    # RPCS3 currently uses an AppImage, no need for the runtime.
    system_options_override = [{"option": "disable_runtime", "default": True}]

    def play(self):
        arguments = self.get_command()

        if self.runner_config.get("nogui"):
            arguments.append("--no-gui")

        eboot = self.game_config.get("main_file") or ""
        if not system.path_exists(eboot):
            raise MissingGameExecutableError(filename=eboot)
        arguments.append(eboot)
        return {"command": arguments}
