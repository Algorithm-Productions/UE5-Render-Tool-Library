from .abstracts.StorableProperty import StorableProperty
from .unreal_dt import AASettings, ConsoleSettings, HighResSettings, OutputSettings


class RenderSettings(StorableProperty):
    """
        Property Object Class to keep the all Render Settings used for a Job.

        :type: StorableProperty.
        :author: vitor@bu.edu.
    """

    def __init__(
            self,
            output_types=None,
            render_types=None,
            aa_settings=None,
            console_settings=None,
            high_res_settings=None,
            output_settings=None
    ):
        """
            Class Constructor.
            Takes in every Parameter as an Optional, allowing for the creation of Empty Objects.

            :param output_types: List of Selected Output File Types.
            :type output_types: List of Strings.
            :param render_types: List of all Active Render Passers.
            :type render_types: List of Strings.
            :param aa_settings: AA Settings being used in the Render.
            :type aa_settings: AASettings.
            :param console_settings: Console Settings being used in the Render.
            :type console_settings: ConsoleSettings.
            :param high_res_settings: High Res Settings being used in the Render.
            :type high_res_settings: HighResSettings.
            :param output_settings: Output Settings being used in the Render.
            :type output_settings: OutputSettings.
        """
        if not output_types:
            output_types = []
        if not render_types:
            render_types = []

        self.output_types = output_types
        self.render_types = render_types
        self.aa_settings = aa_settings
        self.console_settings = console_settings
        self.high_res_settings = high_res_settings
        self.output_settings = output_settings

    @classmethod
    def from_dict(cls, data):
        """
            @inheritDoc - StorableProperty
        """
        output_types = (data["output_types"] or []) if data else []
        render_types = (data["render_types"] or []) if data else []
        aa_settings = (AASettings.from_dict(data.get('aa_settings')) if data.get(
            'aa_settings') else None) if data else None
        console_settings = (ConsoleSettings.from_dict(data.get('console_settings')) if data.get(
            'console_settings') else None) if data else None
        high_res_settings = (HighResSettings.from_dict(data.get('high_res_settings')) if data.get(
            'high_res_settings') else None) if data else None
        output_settings = (OutputSettings.from_dict(data.get('output_settings')) if data.get(
            'output_settings') else None) if data else None

        return cls(
            output_types=output_types,
            render_types=render_types,
            aa_settings=aa_settings,
            console_settings=console_settings,
            high_res_settings=high_res_settings,
            output_settings=output_settings
        )

    def copy(self):
        """
            Helper Method to Create a Copy of the Property Object.

            :return: Property Object with same Fields as Self.
        """
        return RenderSettings(
            output_types=self.output_types,
            render_types=self.render_types,
            aa_settings=self.aa_settings,
            console_settings=self.console_settings,
            high_res_settings=self.high_res_settings,
            output_settings=self.output_settings
        )

    def to_dict(self):
        """
            @inheritDoc - StorableProperty

            Custom Implementation to account for Complex Fields.
        """
        copy = self.copy()
        if self.aa_settings:
            copy.aa_settings = self.aa_settings.to_dict()
        if self.console_settings:
            copy.console_settings = self.console_settings.to_dict()
        if self.high_res_settings:
            copy.high_res_settings = self.high_res_settings.to_dict()
        if self.output_settings:
            copy.output_settings = self.output_settings.to_dict()

        return copy.__dict__
