import unreal

from .utils.UnrealUtils import buildArray, buildMap


@unreal.uclass()
class CustomUnrealPreset(unreal.MoviePipelineMasterConfig):
    def __init__(self, preset):
        super(CustomUnrealPreset, self).__init__(preset)
        self.copy_from(preset)

    def updateAAMethodProperty(self, methodKey, propertyKey, settingKey):
        method = unreal.AntiAliasingMethod.AAM_NONE
        if methodKey == "FXAA":
            method = unreal.AntiAliasingMethod.AAM_FXAA
        elif methodKey == "MSAA":
            method = unreal.AntiAliasingMethod.AAM_MSAA
        elif methodKey == "TEMPORAL_AA":
            method = unreal.AntiAliasingMethod.TEMPORAL_AA
        self.updateProperty(method, propertyKey, settingKey)

    def updateArrayProperty(self, array, propertyKey, settingKey):
        self.updateProperty(buildArray(array), propertyKey, settingKey)

    def updateFrameRateProperty(self, frameRate, propertyKey, settingKey):
        self.updateProperty(unreal.FrameRate(frameRate, 1), propertyKey, settingKey)

    def updateMapProperty(self, givenMap, propertyKey, settingKey):
        self.updateProperty(buildMap(givenMap), propertyKey, settingKey)

    def updatePathProperty(self, directoryPath, propertyKey, settingKey):
        self.updateProperty(unreal.DirectoryPath(directoryPath), propertyKey, settingKey)

    def updateProperty(self, data, propertyKey, settingKey):
        currSettings = self.getSetting(settingKey)
        currSettings.set_editor_property(propertyKey, data)

    def updateResolutionProperty(self, propertyKey, settingKey, x=0, y=0):
        currRes = self.getSetting("output").output_resolution
        if y != 0:
            self.updateProperty(unreal.IntPoint(currRes.x, int(y)), propertyKey, settingKey)
        if x != 0:
            self.updateProperty(unreal.IntPoint(int(y), currRes.y), propertyKey, settingKey)
