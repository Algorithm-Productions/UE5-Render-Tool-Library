import unreal


@unreal.uclass()
class CustomUnrealPreset(unreal.MoviePipelineMasterConfig):
    def __init__(self, preset):
        super(CustomUnrealPreset, self).__init__(preset)
        self.copy_from(preset)

    def update_properties(self, overrides, config):
        self.update_output(overrides["output_settings_flags"], config["output_settings"])
        self.update_high_res(overrides["high_res_settings_flags"], config["high_res_settings"])
        self.update_aa(overrides["aa_settings_flags"], config["aa_settings"])
        self.update_console(overrides["console_settings_flags"], config["console_settings"])

    def updateArrayProperty(self, settingKey, propertyKey, array):
        self.updateProperty(settingKey, propertyKey, buildArray(array))

    def updateMapProperty(self, settingKey, propertyKey, givenMap):
        self.updateProperty(settingKey, propertyKey, buildMap(givenMap))

    def updatePathProperty(self, settingKey, propertyKey, path):
        self.updateProperty(settingKey, propertyKey, unreal.DirectoryPath(path))

    def updateFrameRateProperty(self, settingKey, propertyKey, frameRate):
        self.updateProperty(settingKey, propertyKey, unreal.FrameRate(frameRate, 1))

    def updateResolutionProperty(self, settingKey, propertyKey, x=0, y=0):
        currRes = self.getSetting("output").output_resolution
        if y != 0:
            self.updateProperty(settingKey, propertyKey, unreal.IntPoint(currRes.x, int(y)))
        if x != 0:
            self.updateProperty(settingKey, propertyKey, unreal.IntPoint(int(y), currRes.y))

    def updateAAMethodProperty(self, settingKey, propertyKey, methodKey):
        method = unreal.AntiAliasingMethod.AAM_NONE
        if methodKey == "FXAA":
            method = unreal.AntiAliasingMethod.AAM_FXAA
        elif methodKey == "MSAA":
            method = unreal.AntiAliasingMethod.AAM_MSAA
        elif methodKey == "TEMPORAL_AA":
            method = unreal.AntiAliasingMethod.TEMPORAL_AA
        self.updateProperty(settingKey, propertyKey, method)

    def updateProperty(self, settingKey, propertyKey, val):
        currSettings = self.getSetting(settingKey)

        currSettings.set_editor_property(propertyKey, val)


def buildArray(array):
    returnArray = unreal.Array(str)
    for item in array:
        returnArray.append(item)

    return returnArray


def buildMap(givenMap):
    returnMap = {}
    for key, val in givenMap.items():
        returnMap[key] = float(val)

    return returnMap
