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


def download_repos(root, repos):
    """Download provided repos from GitHub

    Arguments:
        root (str): Destination directory for downloaded files
        repos (iter): Names of repos to download

    Returns:
        list: Absolute paths to downloaded repos

    Example:
        >>> dirs = download_repos(
        ...   "c:\tempdir", ["pyblish-base", "pyblish-qml"])

    """

    dirnames = list()
    for package in repos:
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


def build(root, repos, clean=False):
    """Build distribution at `root` of `repos`

    Arguments:
        root (str): Directory into which to build distribution.
        repos (list): Packages to include
        clean (bool): Should `root` be erased before continuing?

    """

    tries = 3
    while os.path.exists(root):
        tries -= 1
        if tries == 0:
            return sys.stderr.write(
                    "ERROR: Could not clean \"%s\", retrying..\n" % root)

        if not clean:
            return sys.stderr.write(
                "ERROR: root directory already exists: %s\n" % root)
        else:
            try:
                print("Cleaning up..")
                shutil.rmtree(root)
            except OSError:
                sys.stderr.write(
                    "ERROR: Could not clean \"%s\", retrying..\n" % root)

    for dirname in download_repos(root=tempdir, repos=repos):
        sys.path.insert(0, dirname)

    modules = [package.replace("-", "_") for package in repos]

    try:
        # Special case, Python package for
        # "pyblish-base" is just "pyblish".
        modules.remove("pyblish_base")
        modules.append("pyblish")
    except ValueError:
        pass

    for src, dst in generate_filelist(*modules):
        abspath = os.path.join(root, dst)
        dirname = os.path.dirname(abspath)

        try:
            os.makedirs(dirname)
        except OSError:
            pass

        print("Writing \"%s\"" % abspath)
        shutil.copyfile(src, abspath)

    print("Done")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("root")
    parser.add_argument("repos")
    parser.add_argument("--clean", action="store_true")

    args = parser.parse_args()

    tempdir = tempfile.mkdtemp()
    repos = args.repos.split()

    print("Building %s @ \"%s\", clean=%s" % (
        repos, args.root, args.clean))

    build(root=args.root,
          repos=repos,
          clean=args.clean)
