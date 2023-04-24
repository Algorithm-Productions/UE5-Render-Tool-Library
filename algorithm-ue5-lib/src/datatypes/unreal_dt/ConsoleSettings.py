from ..abstracts.UnrealDataType import UnrealDataType


class ConsoleSettings(UnrealDataType):
    def __init__(
            self,
            consoleVariables=None,
            endConsoleCommands=None,
            startConsoleCommands=None
    ):
        if not consoleVariables:
            consoleVariables = {}
        if not endConsoleCommands:
            endConsoleCommands = []
        if not startConsoleCommands:
            startConsoleCommands = []

        self.consoleVariables = consoleVariables
        self.endConsoleCommands = endConsoleCommands
        self.startConsoleCommands = startConsoleCommands

    @classmethod
    def from_dict(cls, data):
        consoleVariables = dict(data["consoleVariables"]) if (data and data["consoleVariables"]) else {}
        endConsoleCommands = list(data["endConsoleCommands"]) if (data and data["endConsoleCommands"]) else []
        startConsoleCommands = list(data["startConsoleCommands"]) if (data and data["startConsoleCommands"]) else []

        return cls(
            consoleVariables=consoleVariables,
            endConsoleCommands=endConsoleCommands,
            startConsoleCommands=startConsoleCommands
        )

    @classmethod
    def from_unreal(cls, unrealClass):
        return cls(
            consoleVariables=dict(unrealClass.console_variables),
            endConsoleCommands=list(unrealClass.end_console_commands),
            startConsoleCommands=list(unrealClass.start_console_commands)
        )
