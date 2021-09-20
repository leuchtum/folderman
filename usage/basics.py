from folderman import Folder
import pathlib

# Create a root folder and attach subfolders
root = Folder(pathlib.Path.home(), ".folderman")
data_path = Folder(root, "data")
data2_path = Folder(root, "data2")

# Make directory
root.mktree(force=True)

# Access subfolders by brackets
print(root["data"])

# Append files in pathlib style
print(root.path / "test1.txt")

# Discover unregistered folders and at to children
(root.path / "discover_test").mkdir()
(root["data"] / "discover_test2").mkdir()
root.discover()

# Iter over Files, Folders or both
(root["data"].path / "test.txt").touch()
(root.path / "test1.txt").touch()
(root.path / "test2.txt").touch()
(root.path / "andere.txt").touch()
for fname in root.iterdirs(specify="*"):
    print(fname)
for fname in root.iterfiles(specify="test*"):
    print(fname)
for fname in root.iterdirs():
    print(fname)

# Remove a tree
root.rmtree()


