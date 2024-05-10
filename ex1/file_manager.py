class FileManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        with open(self.file_path, 'r') as file:
            contents = file.read()
        return contents

    def write_file(self, content):
        with open(self.file_path, 'w') as file:
            file.write(content)
