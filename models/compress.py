

class CompressModel():
    def __init__(self, data) -> None:
            self.fileName = data["fileName"]
            self.power = data["power"]

    def get_json(self):
        return {"power": self.power, "fileName": self.fileName}
    
    def __str__(self) -> str:
        return str(self.get_json())


class CompressResponse():
    def __init__(self, ratio, final_size) -> None:
        self.ratio = ratio
        self.final_size = final_size

    def get_json(self):
        return {"compressionRatio": self.ratio, "finalSizeMB":self.final_size}