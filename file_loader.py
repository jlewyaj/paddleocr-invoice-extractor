from pathlib import Path


class FileLoader:

    SUPPORTED_EXTENSIONS  = [
        ".jpeg",
        ".jpg",
        ".png",
        ".pdf"
    ]

    def load(self, folder):
        folder = Path(folder)

        files = []

        for file in folder.iterdir():

            if file.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                files.append(file)

        return sorted(files)