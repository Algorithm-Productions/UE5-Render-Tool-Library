from ..abstracts.UnrealOverride import UnrealOverride


class ConsoleSettingsOverride(UnrealOverride):
    UNREAL_MAPPINGS = {
        "consoleVariables": ["console_variables", "map"],
        "endConsoleCommands": ["end_console_commands", "array"],
        "startConsoleCommands": ["start_console_commands", "array"]
    }
    UNREAL_SETTING_KEY = "console"

    def __init__(
            self,
            consoleVariablesFlag=False,
            endConsoleCommandsFlag=False,
            startConsoleCommandsFlag=False
    ):
        self.consoleVariablesFlag = consoleVariablesFlag
        self.endConsoleCommandsFlag = endConsoleCommandsFlag
        self.startConsoleCommandsFlag = startConsoleCommandsFlag

    @classmethod
    def from_dict(cls, data):
        consoleVariablesFlag = data["consoleVariablesFlag"] if (data and data["consoleVariablesFlag"]) else False
        endConsoleCommandsFlag = data["endConsoleCommandsFlag"] if (data and data["endConsoleCommandsFlag"]) else False
        startConsoleCommandsFlag = data["startConsoleCommandsFlag"] if \
            (data and data["startConsoleCommandsFlag"]) else False

        return cls(
            consoleVariablesFlag=consoleVariablesFlag,
            endConsoleCommandsFlag=endConsoleCommandsFlag,
            startConsoleCommandsFlag=startConsoleCommandsFlag
        )
