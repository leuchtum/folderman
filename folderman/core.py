import pathlib
import shutil

_PATHLIB_CLASSES = [pathlib.Path, pathlib.PosixPath, pathlib.PurePosixPath,
                    pathlib.WindowsPath, pathlib.PurePath, pathlib.PureWindowsPath]


class Folder:
    """
    Class that represents a folder. 
    """
    def __init__(self, parent_folder, name):
        # Assert types
        assert type(name) in [str, *_PATHLIB_CLASSES]
        assert type(parent_folder) in [Folder, *_PATHLIB_CLASSES]

        # Init
        self.name = name if type(name) == str else name.name
        self.is_root = False
        self.path = None
        self.parent = None
        self.children = []

        # Set
        if type(parent_folder) == Folder:
            self.parent = parent_folder
            self.parent._add_child(self)
        else:
            self.is_root = True
        self.path = parent_folder / name

    def _add_child(self, child):
        assert type(child) == Folder
        assert child not in self.children
        self.children.append(child)

    def discover(self):
        """
        Iterate recursively through all folders and their subfolders.
        Add the found folders to the children.
        """
        for path in self.iterdirs():
            if path not in [c.path for c in self.children]:
                _ = Folder(self, path)

        for child in self.children:
            child.discover()

    def mkdir(self, force=False):
        """
        Make this folder.

        Args:
            force (bool, optional): Delete folder before creating it
                                    from scratch. Defaults to False.
        """
        if self.parent is not None:
            assert self.parent.exists()

        if force:
            self.rmtree()
            self.mkdir()
        else:
            self.path.mkdir()

    def mktree(self, force=False):
        """
        Make this folder and all registered subfolders (children)

        Args:
            force (bool, optional): Delete folder before creating it
                                    from scratch. Defaults to False.
        """
        self.mkdir(force=force)
        for child in self.children:
            child.mktree(force=force)

    def rmtree(self):
        """
        Delete this folder and all contained files and subfolders.
        """
        if self.path.exists():
            shutil.rmtree(self.path)

    def exists(self):
        """Check if this folder exists

        Returns:
            bool: Folder exists
        """
        return self.path.exists()

    def iterfiles(self, specify="*"):
        """
        Iterate over all files specified by 'specify'.

        Args:
            specify (str, optional): Filename has to match this. Defaults to "*".

        Yields:
            pathlib.Path: Path of of the matching file
        """
        for path in self.path.glob(specify):
            if path.is_dir():
                continue
            yield path

    def iterdirs(self, specify="*"):
        """
        Iterate over all folders specified by 'specify'.

        Args:
            specify (str, optional): Foldername has to match this. Defaults to "*".

        Yields:
            pathlib.Path: Path of of the matching folder
        """
        for path in self.path.glob(specify):
            if path.is_dir():
                yield path

    def iter(self, specify="*"):
        """
        Iterate over all files and folders specified by 'specify'.

        Args:
            specify (str, optional): Foldername or filename has to match this.
                                     Defaults to "*".

        Yields:
            pathlib.Path: Path of of the matching folder or file
        """
        yield from self.path.glob(specify)

    def graph(self):
        """
        Get strings representing the structure of this folder.

        Returns:
            str: String that represents the structure of this folder.
        """
        strings = self._recursive_graph()
        return "\n".join(strings)

    def _recursive_graph(self):
        strings = [self.name]
        for fname in self.iterfiles():
            strings.append(f"  {fname.name}")
        for child in self.children:
            child_strings = child._recursive_graph()
            child_strings = [f"  {child}" for child in child_strings]
            strings.extend(child_strings)
        return strings

    def __truediv__(self, other):
        return self.path / other

    def __getitem__(self, i):
        for child in self.children:
            if child.name == i:
                return child
            else:
                raise KeyError(f"No subfolder with name '{i}' found.")

    def __str__(self):
        return str(self.path)

    def __repr__(self):
        return f"Folder: {self}"
