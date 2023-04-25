from .abstracts.StorableProperty import StorableProperty
from .overrides import AASettingsOverride, ConsoleSettingsOverride, HighResSettingsOverride, OutputSettingsOverride


class RenderSettingsOverride(StorableProperty):
    def __init__(
            self,
            aa_settings_flags=None,
            console_settings_flags=None,
            high_res_settings_flags=None,
            output_settings_flags=None,
            output_types_flag=False,
            render_types_flag=False
    ):
        self.aa_settings_flags = aa_settings_flags
        self.console_settings_flags = console_settings_flags
        self.high_res_settings_flags = high_res_settings_flags
        self.output_settings_flags = output_settings_flags
        self.output_types_flag = output_types_flag
        self.render_types_flag = render_types_flag

    @classmethod
    def from_dict(cls, data):
        aa_settings_flags = AASettingsOverride.from_dict(data["aa_settings_flags"]) if \
            (data and data["aa_settings_flags"]) else None
        console_settings_flags = ConsoleSettingsOverride.from_dict(data["console_settings_flags"]) if \
            (data and data["console_settings_flags"]) else None
        high_res_settings_flags = HighResSettingsOverride.from_dict(data["high_res_settings_flags"]) if \
            (data and data["high_res_settings_flags"]) else None
        output_settings_flags = OutputSettingsOverride.from_dict(data["output_settings_flags"]) if \
            (data and data["output_settings_flags"]) else None
        output_types_flag = data["output_types_flag"] if (data and data["output_types_flag"]) else False
        render_types_flag = data["render_types_flag"] if (data and data["render_types_flag"]) else False

        return cls(
            aa_settings_flags=aa_settings_flags,
            console_settings_flags=console_settings_flags,
            high_res_settings_flags=high_res_settings_flags,
            output_settings_flags=output_settings_flags,
            output_types_flag=output_types_flag,
            render_types_flag=render_types_flag
        )

    def copy(self):
        return RenderSettingsOverride(
            aa_settings_flags=self.aa_settings_flags,
            console_settings_flags=self.console_settings_flags,
            high_res_settings_flags=self.high_res_settings_flags,
            output_settings_flags=self.output_settings_flags,
            output_types_flag=self.output_types_flag,
            render_types_flag=self.render_types_flag
        )

    def to_dict(self):
        copy = self.copy()
        if self.aa_settings_flags:
            copy.aa_settings_flags = self.aa_settings_flags.to_dict()
        if self.console_settings_flags:
            copy.console_settings_flags = self.console_settings_flags.to_dict()
        if self.high_res_settings_flags:
            copy.high_res_settings_flags = self.high_res_settings_flags.to_dict()
        if self.output_settings_flags:
            copy.output_settings_flags = self.output_settings_flags.to_dict()

        return copy.__dict__
