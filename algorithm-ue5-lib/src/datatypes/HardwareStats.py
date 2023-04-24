from .abstracts.StorableProperty import StorableProperty


class HardwareStats(StorableProperty):
    def __init__(
            self,
            cpu='',
            gpu='',
            name='',
            ram='',
            vram=''
    ):
        self.cpu = cpu
        self.gpu = gpu
        self.name = name
        self.ram = ram
        self.vram = vram

    @classmethod
    def from_dict(cls, data):
        cpu = data["cpu"] if (data and data["cpu"]) else ''
        gpu = data["gpu"] if (data and data["gpu"]) else ''
        name = data["name"] if (data and data["name"]) else ''
        ram = data["ram"] if (data and data["ram"]) else ''
        vram = data["vram"] if (data and data["vram"]) else ''

        return cls(
            cpu=cpu,
            gpu=gpu,
            name=name,
            ram=ram,
            vram=vram
        )
