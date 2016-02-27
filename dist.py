"""Build distribution of Pyblish

Usage:
    $ dist.py /root/dir "pyblish pyblish-qml pyblish-rpc" --clean

"""

import os
import sys
import imp
import shutil
import urllib
import tempfile
import zipfile


def download_packages(root, packages):
    """Download provided packages from GitHub

    Arguments:
        root (str): Destination directory for downloaded files
        packages (iter): Names of packages to download

    Returns:
        list: Absolute paths to downloaded packages

    Example:
        >>> dirs = download_packages(
        ...   "c:\tempdir", ["pyblish-base", "pyblish-qml"])

    """

    dirnames = list()
    for package in packages:
        url = "https://github.com/pyblish/%s/archive/master.zip" % package
        dst = os.path.join(root, package)

        try:
            print("Downloading %s.." % url)
            fname, _ = urllib.urlretrieve(url, dst + ".zip")
        except IOError:
            sys.stderr.write("Had trouble downloading %s\n" % package)
            return

        with zipfile.ZipFile(fname) as zf:
            zf.extractall(dst)

        dirnames.append(os.path.join(dst, package + "-master"))
    return dirnames


def generate_filelist(*packages):
    """Scan PYTHONPATH for package in `packages` and yield list of files.

    Arguments:
        packages (iter): Names of packages to include, e.g. ["pyblish_qml"]

    """

    for package in packages:
        _, dirname, _ = imp.find_module(package)

        exclude = (".pyc",)
        for base, dirs, files in os.walk(dirname):
            for fname in files:
                _, ext = os.path.splitext(fname)
                if ext in exclude:
                    continue

                # Output package/file.ext
                src = os.path.join(base, fname)
                dst = os.path.relpath(os.path.join(base, fname),
                                      os.path.dirname(dirname))
                yield src, dst


def build(root, packages, clean=False):
    """Build distribution at `root` of `packages`

    Arguments:
        root (str): Directory into which to build distribution.
        packages (str): Packages to include
        clean (bool): Should `root` be erased before continuing?

    """

    if os.path.exists(root):
        if not clean:
            return sys.stderr.write(
                "ERROR: root directory already exists: %s\n" % root)
        else:
            try:
                shutil.rmtree(root)
            except OSError:
                return sys.stderr.write(
                    "ERROR: Could not clean \"%s\"\n" % root)

    modules = [package.replace("-", "_") for package in packages]

    for module in list(modules):
        if module == "pyblish_base":
            modules.remove(module)
            modules.append("pyblish")

    for src, dst in generate_filelist(*packages):
        abspath = os.path.join(root, dst)
        dirname = os.path.dirname(abspath)

        try:
            os.makedirs(dirname)
        except OSError:
            pass

        print("Writing %s" % abspath)
        shutil.copyfile(src, abspath)

    print("Done.")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("root")
    parser.add_argument("packages")
    parser.add_argument("--clean", action="store_true")

    args = parser.parse_args()

    tempdir = tempfile.mkdtemp()
    packages = args.packages.split()

    for dirname in download_packages(root=tempdir, packages=packages):
        sys.path.insert(0, dirname)

    build(root=args.root,
          packages=args.packages.split(),
          clean=args.clean)
