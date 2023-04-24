from .abstracts.StorableProperty import StorableProperty
from .overrides import AASettingsOverride, ConsoleSettingsOverride, HighResSettingsOverride, OutputSettingsOverride


class RenderSettingsOverride(StorableProperty):
    def __init__(
            self,
            output_types_flag=False,
            render_types_flag=False,
            aa_settings_flags=None,
            console_settings_flags=None,
            high_res_settings_flags=None,
            output_settings_flags=None
    ):
        self.output_types_flag = output_types_flag
        self.render_types_flag = render_types_flag
        self.aa_settings_flags = aa_settings_flags
        self.console_settings_flags = console_settings_flags
        self.high_res_settings_flags = high_res_settings_flags
        self.output_settings_flags = output_settings_flags

    @classmethod
    def from_dict(cls, data):
        output_types_flag = (data["output_types_flag"] or False) if (data and data['output_types_flag']) else False
        render_types_flag = (data["render_types_flag"] or False) if (data and data['render_types_flag']) else False
        aa_settings_flags = (AASettingsOverride.from_dict(data.get('aa_settings_flags')) if data.get(
            'aa_settings_flags') else None) if data else None
        console_settings_flags = (
            ConsoleSettingsOverride.from_dict(data.get('console_settings_flags')) if data.get(
                'console_settings_flags') else None) if data else None
        high_res_settings_flags = (
            HighResSettingsOverride.from_dict(data.get('high_res_settings_flags')) if data.get(
                'high_res_settings_flags') else None) if data else None
        output_settings_flags = (
            OutputSettingsOverride.from_dict(data.get('output_settings_flags')) if data.get(
                'output_settings_flags') else None) if data else None

        return cls(
            output_types_flag=output_types_flag,
            render_types_flag=render_types_flag,
            aa_settings_flags=aa_settings_flags,
            console_settings_flags=console_settings_flags,
            high_res_settings_flags=high_res_settings_flags,
            output_settings_flags=output_settings_flags
        )

    def copy(self):
        return RenderSettingsOverride(
            output_types_flag=self.output_types_flag,
            render_types_flag=self.render_types_flag,
            aa_settings_flags=self.aa_settings_flags,
            console_settings_flags=self.console_settings_flags,
            high_res_settings_flags=self.high_res_settings_flags,
            output_settings_flags=self.output_settings_flags
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
