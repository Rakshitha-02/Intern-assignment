import os
import re


class FileSystem:
    def __init__(self):
        self.root = Directory("/")
        self.current_directory = self.root

    def mkdir(self, directory_name):
        new_directory = Directory(directory_name)
        self.current_directory.add_directory(new_directory)

    def cd(self, path):
        if path == "/":
            self.current_directory = self.root
        elif path == "..":
            if self.current_directory.parent:
                self.current_directory = self.current_directory.parent
        elif path.startswith("/"):
            target_directory = self.root.find_directory_by_path(path)
            if target_directory:
                self.current_directory = target_directory
        else:
            target_directory = self.current_directory.find_directory_by_path(path)
            if target_directory:
                self.current_directory = target_directory

    def ls(self, path="."):
        if path == ".":
            target_directory = self.current_directory
        elif path.startswith("/"):
            target_directory = self.root.find_directory_by_path(path)
        else:
            target_directory = self.current_directory.find_directory_by_path(path)

        if target_directory:
            return target_directory.list_contents()
        return []

    def grep(self, pattern, file_path):
        target_file = self.find_file_by_path(file_path)
        if target_file:
            return target_file.search_pattern(pattern)
        return "File not found."

    def cat(self, file_path):
        target_file = self.find_file_by_path(file_path)
        if target_file:
            return target_file.get_contents()
        return "File not found."

    def touch(self, file_name):
        new_file = File(file_name)
        self.current_directory.add_file(new_file)

    def echo(self, text, file_path):
        target_file = self.find_file_by_path(file_path)
        if target_file:
            target_file.write_text(text)
        else:
            self.touch(file_path)
            target_file = self.find_file_by_path(file_path)
            target_file.write_text(text)

    def mv(self, source_path, destination_path):
        source_file = self.find_file_by_path(source_path)
        source_directory = self.find_directory_by_path(source_path)

        if source_file:
            destination_directory = self.find_directory_by_path(destination_path)
            if destination_directory:
                destination_directory.add_file(source_file)
                source_directory.remove_file(source_file)
            else:
                print("Destination directory not found.")
        elif source_directory:
            destination_directory = self.find_directory_by_path(destination_path)
            if destination_directory:
                destination_directory.add_directory(source_directory)
                source_directory.parent.remove_directory(source_directory)
            else:
                print("Destination directory not found.")
        else:
            print("Source not found.")

    def cp(self, source_path, destination_path):
        source_file = self.find_file_by_path(source_path)
        source_directory = self.find_directory_by_path(source_path)

        if source_file:
            destination_directory = self.find_directory_by_path(destination_path)
            if destination_directory:
                new_file = source_file.copy()
                destination_directory.add_file(new_file)
            else:
                print("Destination directory not found.")
        elif source_directory:
            destination_directory = self.find_directory_by_path(destination_path)
            if destination_directory:
                new_directory = source_directory.copy()
                destination_directory.add_directory(new_directory)
            else:
                print("Destination directory not found.")
        else:
            print("Source not found.")

    def rm(self, path):
        target_file = self.find_file_by_path(path)
        target_directory = self.find_directory_by_path(path)

        if target_file:
            self.current_directory.remove_file(target_file)
        elif target_directory:
            self.current_directory.remove_directory(target_directory)
        else:
            print("File or directory not found.")

    def find_directory_by_path(self, path):
        if path.startswith("/"):
            current_directory = self.root
            path_parts = path.split("/")[1:]
        else:
            current_directory = self.current_directory
            path_parts = path.split("/")

        for part in path_parts:
            if part == "..":
                current_directory = current_directory.parent
            else:
                current_directory = current_directory.find_directory_by_name(part)
                if not current_directory:
                    return None

        return current_directory

    def find_file_by_path(self, path):
        directory_path, file_name = path.rsplit("/", 1) if "/" in path else ("", path)

        target_directory = self.find_directory_by_path(directory_path)
        if target_directory:
            return target_directory.find_file_by_name(file_name)

        return None


class Directory:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.subdirectories = []
        self.files = []

    def add_directory(self, directory):
        self.subdirectories.append(directory)
        directory.parent = self

    def remove_directory(self, directory):
        self.subdirectories.remove(directory)
        directory.parent = None

    def add_file(self, file):
        self.files.append(file)

    def remove_file(self, file):
        self.files.remove(file)

    def list_contents(self):
        return [directory.name + "/" for directory in self.subdirectories] + [file.name for file in self.files]

    def find_directory_by_name(self, name):
        for directory in self.subdirectories:
            if directory.name == name:
                return directory
        return None

    def find_file_by_name(self, name):
        for file in self.files:
            if file.name == name:
                return file
        return None


class File:
    def __init__(self, name):
        self.name = name
        self.contents = ""

    def copy(self):
        new_file = File(self.name)
        new_file.contents = self.contents
        return new_file

    def write_text(self, text):
        self.contents = text

    def get_contents(self):
        return self.contents

    def search_pattern(self, pattern):
        lines = self.contents.split('\n')
        result = [line for line in lines if re.search(pattern, line)]
        return result


# Example usage:
fs = FileSystem()
fs.mkdir("documents")
fs.cd("documents")
fs.touch("file1.txt")
fs.echo('I am "Finding" difficult to write this to file', "file1.txt")
print(fs.ls())  # Output: ['file1.txt']
print(fs.cat("file1.txt"))  # Output: 'I am "Finding" difficult to write this to file'
fs.cd("..")
print(fs.ls())  # Output: ['documents']
fs.cp("documents/file1.txt", "file2.txt")
print(fs.ls())  # Output: ['documents', 'file2.txt']
fs.cd("documents")
print(fs.ls())  # Output: ['file1.txt', 'file2.txt']
fs.rm("file1.txt")
print(fs.ls())  # Output: ['file2.txt']
