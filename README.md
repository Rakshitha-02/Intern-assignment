# Intern-assignment
#In-Memory File System Documentation


Introduction:
The provided Python implementation simulates an in-memory file system, offering essential functionalities for managing directories and files. It models a file system where users can create directories, navigate through paths, list directory contents, search for patterns in files (bonus grep functionality), display file contents (cat), create empty files (touch), write text to files (echo), move files or directories (mv), copy files or directories (cp), and remove files or directories (rm).


  # Example of Usage
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
