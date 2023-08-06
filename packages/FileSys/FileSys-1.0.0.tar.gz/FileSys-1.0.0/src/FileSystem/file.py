class filesys():
    def create(self, filename, extension):
        self.filename = filename
        self.extension = extension
        f = open(self.filename+self.extension, "x")

    def delete(self, filename, extension):
        import os
        self.filename = filename
        self.extension = extension
        os.remove(self.filename+self.extension)

    def exists(self, filename, extension):
        self.filename = filename
        self.extension = extension
        import os
        if os.path.exists(self.filename+self.extension):
            print("The file exists")
        else:
            print("The file does not exist")

    def write(self, filename, extension, content):
        self.filename = filename
        self.extension = extension
        self.content = content
        f = open(self.filename+self.extension, "w")
        f.write(self.content)