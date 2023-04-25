from .abstracts.StorableProperty import StorableProperty
from .unreal_dt import AASettings, ConsoleSettings, HighResSettings, OutputSettings


class RenderSettings(StorableProperty):
    def __init__(
            self,
            output_types=None,
            render_types=None,
            aa_settings=None,
            console_settings=None,
            high_res_settings=None,
            output_settings=None
    ):
        self.aa_settings = aa_settings
        self.console_settings = console_settings
        self.high_res_settings = high_res_settings
        self.output_settings = output_settings
        self.output_types = [] if output_types is None else output_types
        self.render_types = [] if render_types is None else render_types

    @classmethod
    def from_dict(cls, data):
        aa_settings = AASettings.from_dict(data["aa_settings"]) if (data and data["aa_settings"]) else None
        console_settings = ConsoleSettings.from_dict(data["console_settings"]) if \
            (data and data["console_settings"]) else None
        high_res_settings = HighResSettings.from_dict(data["high_res_settings"]) if \
            (data and data["high_res_settings"]) else None
        output_settings = OutputSettings.from_dict(data["output_settings"]) if \
            (data and data["output_settings"]) else None
        output_types = data["output_types"] if (data and data["output_types"]) else []
        render_types = data["render_types"] if (data and data["render_types"]) else []

        return cls(
            aa_settings=aa_settings,
            console_settings=console_settings,
            high_res_settings=high_res_settings,
            output_settings=output_settings,
            output_types=output_types,
            render_types=render_types
        )

    def copy(self):
        return RenderSettings(
            aa_settings=self.aa_settings,
            console_settings=self.console_settings,
            high_res_settings=self.high_res_settings,
            output_settings=self.output_settings,
            output_types=self.output_types,
            render_types=self.render_types
        )

    def to_dict(self):
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
