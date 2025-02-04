import sys
import os
import subprocess

if __name__ == "__main__":
    contrib = sys.argv[1]
    headless = sys.argv[2]
    ci_build = sys.argv[3]

    opencv_version = ""
    # dig out the version from OpenCV sources
    version_file_path = "opencv/modules/core/include/opencv2/core/version.hpp"

    with open(version_file_path, "r") as f:
        for line in f:
            words = line.split()

            if "CV_VERSION_MAJOR" in words:
                opencv_version += words[2]
                opencv_version += "."

            if "CV_VERSION_MINOR" in words:
                opencv_version += words[2]
                opencv_version += "."

            if "CV_VERSION_REVISION" in words:
                opencv_version += words[2]
                break

    # used in local dev releases
    git_hash = (
        subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
        .splitlines()[0]
        .decode()
    )
    # this outputs the annotated tag if we are exactly on a tag, otherwise <tag>-<n>-g<shortened sha-1>
    try:
        tag = (
            subprocess.check_output(
                ["git", "describe", "--tags"], stderr=subprocess.STDOUT
            )
            .splitlines()[0]
            .decode()
            .split("-")
        )
    except subprocess.CalledProcessError as e:
        # no tags reachable (e.g. on a topic branch in a fork), see
        # https://stackoverflow.com/questions/4916492/git-describe-fails-with-fatal-no-names-found-cannot-describe-anything
        if e.output.rstrip() == b"fatal: No names found, cannot describe anything.":
            tag = []
        else:
            print(e.output)
            raise

    if len(tag) == 1:
        # tag identifies the build and should be a sequential revision number
        version = tag[0]
        opencv_version += ".{}".format(version)
    else:
        # local version identifier, not to be published on PyPI
        version = git_hash
        opencv_version += "+{}".format(version)

    with open("cv2/version.py", "w") as f:
        f.write('opencv_version = "{}"\n'.format("4.6.0"))
        f.write("contrib = {}\n".format(contrib))
        f.write("headless = {}\n".format(headless))
        f.write("ci_build = {}".format(ci_build))
