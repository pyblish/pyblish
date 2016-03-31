import os
import re
import shutil
import subprocess


def collect(base):
    """Collect files for distribution

    Arguments:
        base (str): Path to source

    """

    paths = list()
    for root, dirs, files in os.walk(base):

        # Exclude Directories
        relpath = os.path.relpath(root, base)
        if any(d.lower() in relpath.lower() for d in (
                ".git",
                "dist",
                "build",
                "lib\\python-qt5\\src",
                "lib\\python27\\tcl",
                "lib\\python27\\doc",
                "lib\\python27\\include"
                "lib\\python27\\tools",
                "lib\\python-qt5\\pyqt5\examples",
                "lib\\python-qt5\\pyqt5\include",
                "lib\\python-qt5\\pyqt5\mkspecs",
                "lib\\python-qt5\\pyqt5\qsci",
                "lib\\python-qt5\\pyqt5\sip",
                "lib\\python-qt5\\pyqt5\translations",
                "lib\\python-qt5\\pyqt5\uic",
                )):
            continue

        for fname in files:

            # Exclude files
            if any(f in fname for f in (
                    ".pyc",
                    "Qt5Web",
                    "QtWeb",
                    "Qt5Multimedia",
                    "QtMultimedia",
                    "icudt53",
                    "opengl32sw",
                    "qtdesigner.dll",
                    "d3dcompiler_47.dll",
                    "QtXmlPatterns.dll",
                    "Qt5Declarative.dll"
                    )):
                continue

            path = os.path.join(root, fname)
            relpath = os.path.relpath(path, base)

            if any(re.match(p, relpath) for p in (
                    "^.*(PyQt5).*(.exe)$",
                    "^(build.bat)$",
                    "^(install.bat)$",
                    "^(reset.bat)$",
                    "^(test.bat)$",
                    "^(subshell.bat)$",
                    "^(update.bat)$",
                    "^(setup.iss)$",
                    "^(appveyor.yml)$",
                    "^[.]",
                    )):
                continue

            paths.append(relpath)

    return paths


def bundle(src, dst):
    """Bundle files from `src` into `dst`

    Arguments:
        src (str): Source directory of files to bundle, e.g. /
        dst (str): Output directory in which to copy files /build

    """

    print("Collecting files..")

    paths = collect(src)

    print("Copying files into /build")
    for fname in paths:
        out = os.path.join(dst, fname)

        try:
            os.makedirs(os.path.dirname(out))
        except WindowsError:
            pass

        shutil.copyfile(src=fname, dst=out)

    print("Build finished successfully.")

    return dst


def exe(src, dst):
    """Create installer using Inno Setup

    Arguments:
        src (str): Path to bundle, e.g. /build
        dst (str): Output directory in which to compile installer, e.g. /dist

    """

    print("Creating installer..")
    try:
        iscc = subprocess.check_output(["where", "iscc"]).strip()
    except subprocess.CalledProcessError:
        print("Could not find Inno Setup")
        return 1

    setup = os.path.join(os.getcwd(), "setup.iss")

    print("Compiling \"%s\" using \"%s\"" % (setup, iscc))
    BUILD = os.environ.get("APPVEYOR_BUILD_NUMBER", "0")
    VERSION = os.path.join(__file__, "..", "..", "lib", "pyblish", "VERSION")
    with open(VERSION) as f:
        VERSION = f.read()

    subprocess.call([iscc,
                     "/dMyVersion=%s-build%s" % (VERSION, BUILD),
                     "/dMyOutputDir=%s" % dst,
                     setup])

    print("Successfully created installer")


if __name__ == '__main__':
    import sys
    import argparse

    # Expose local libraries
    sys.path.insert(0, os.path.dirname(__file__))

    import dist

    parser = argparse.ArgumentParser()
    parser.add_argument("target")
    parser.add_argument("--clean", action="store_true")

    kwargs = parser.parse_args()

    base = kwargs.target
    build = os.path.join(base, "build")

    if kwargs.clean and os.path.exists(build):
        print("Cleaning build directory..")

        try:
            shutil.rmtree(build)
        except:
            raise Exception("Could not remove build directory")

    win = dist.download(["pyblish-win"])[0]
    win = os.path.join(win, "static")

    bundle(src=base, dst=build)
    bundle(src=win, dst=build)

    # Replace with a light-weight version
    shutil.copy(src=os.path.join(win, "icudt53.dll"),
                dst=os.path.join(build, "lib", "python-qt5", "PyQt5"))

    # exe(src=build, dst="dist")
