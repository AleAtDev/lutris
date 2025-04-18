# Standard Library
from gettext import gettext as _

from lutris.exceptions import DirectoryNotFoundError
# Lutris Modules
from lutris.runners.runner import Runner
from lutris.util import system


class cemu(Runner):
    human_name = _("Cemu")
    platforms = [_("Wii U")]
    description = _("Wii U emulator")
    runnable_alone = True
    runner_executable = "cemu/Cemu"
    flatpak_id = "info.cemu.Cemu"
    game_options = [
        {
            "option": "main_file",
            "type": "directory",
            "label": _("Game directory"),
            "help": _(
                "The directory in which the game lives. "
                "If installed into Cemu, this will be in the mlc directory, such as mlc/usr/title/00050000/101c9500."
            ),
        },
        {
            "option": "wua_rom",
            "type": "file",
            "label": _("Compressed ROM"),
            "help": _("A game compressed into a single file (WUA format), only use if not using game directory"),
        },
    ]
    runner_options = [
        {
            "option": "fullscreen",
            "label": _("Fullscreen"),
            "type": "bool",
            "default": True,
        },
        {
            "option": "mlc",
            "label": _("Custom mlc folder location"),
            "type": "directory",
        },
        {
            "option": "ud",
            "label": _("Render in upside down mode"),
            "type": "bool",
            "default": False,
            "advanced": True,
        },
        {
            "option": "nsight",
            "label": _("NSight debugging options"),
            "type": "bool",
            "default": False,
            "advanced": True,
        },
        {
            "option": "legacy",
            "label": _("Intel legacy graphics mode"),
            "type": "bool",
            "default": False,
            "advanced": True,
        },
    ]

    def play(self):
        """Run the game."""
        arguments = self.get_command()

        fullscreen = self.runner_config.get("fullscreen")
        if fullscreen:
            arguments.append("-f")
        mlc = self.runner_config.get("mlc")
        if mlc:
            if not system.path_exists(mlc):
                raise DirectoryNotFoundError(directory=mlc)
            arguments += ["-m", mlc]
        ud = self.runner_config.get("ud")
        if ud:
            arguments.append("-u")
        nsight = self.runner_config.get("nsight")
        if nsight:
            arguments.append("--nsight")
        legacy = self.runner_config.get("legacy")
        if legacy:
            arguments.append("--legacy")
        gamedir = self.game_config.get("main_file") or self.game_config.get("wua_rom") or ""
        if not system.path_exists(gamedir):
            raise DirectoryNotFoundError(directory=gamedir)
        arguments += ["-g", gamedir]
        return {"command": arguments}
