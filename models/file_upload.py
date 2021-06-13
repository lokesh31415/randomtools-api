
class FileUploadResponse:

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def get_json(self):
        out = {"fileName": self.file_name}
        return out
