#!/usr/bin/env python3

import json
import tarfile
import logging
from glob import glob
from argparse import ArgumentParser
from pathlib import Path
from shutil import copyfile, copytree
from tempfile import TemporaryDirectory
from os import remove

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def save(project_dir: Path, action_target: Path):
    glob_nuget_cache_files = project_dir / Path("./*/obj/project.nuget.cache")
    logger.debug(
        f"Use glob string to retrieve nuget caches: '{glob_nuget_cache_files}'"
    )

    NUGET_CACHE_FILES = glob(glob_nuget_cache_files.as_posix())

    logger.debug(
        "Use for processing next found files: '" + "', '".join(NUGET_CACHE_FILES) + "'."
    )

    package_paths_to_save: list[Path] = []

    for cache_file in NUGET_CACHE_FILES:

        logger.debug(f"Processing '{cache_file}'...")

        with open(cache_file) as f:
            d = json.load(f)
            expectedPackageFiles: list = d["expectedPackageFiles"]

            if len(expectedPackageFiles) == 0:
                continue

            first_element = Path(expectedPackageFiles[0])

            package_path = first_element.parent.parent.parent

            logger.debug(f"Packages path: '{package_path}'")

            for package in expectedPackageFiles:
                package_path = Path(package)
                package_paths_to_save.append(package_path)

                pakage_name = package_path.parent.parent.name
                pakage_version = package_path.parent.name

                logger.debug(f"Package '{pakage_name}' version '{pakage_version}'")

    # Remove duplicates
    package_paths_to_save = set(package_paths_to_save)

    for package_path in package_paths_to_save:
        path_to_copy = package_path.parent

        package_name = path_to_copy.parent.name
        package_version = path_to_copy.name

        logger.info(
            f"Saving to '{action_target}' package '{package_name}' version '{package_version}'"
        )

        destination = Path(action_target) / Path(package_name) / Path(package_version)

        copytree(path_to_copy, destination, dirs_exist_ok=True, copy_function=copyfile)

        # Package cache contents, probably unpacked from this nupkg archive
        # Maybe no necessary to save it
        for nupkg_path in path_to_copy.rglob("*.nupkg"):
            remove(destination / Path(nupkg_path.name))

        # Remove archive related shasum too
        for nupkg_path in path_to_copy.rglob("*.nupkg.sha*"):
            remove(destination / Path(nupkg_path.name))


def backup(project_dir: Path, action_target: Path):

    with TemporaryDirectory() as tmpdirname:
        tmpdir = Path(tmpdirname)
        save(project_dir, tmpdir)

        archive_name = Path(action_target.with_suffix(".tgz"))

        logger.info(f"Compressing to '{archive_name}'...")

        with tarfile.open(archive_name, "w:gz") as tar:
            for file in tmpdir.rglob("*"):
                if file.is_dir():
                    continue

                def reset(tarinfo):
                    tarinfo.uid = tarinfo.gid = 0
                    tarinfo.uname = tarinfo.gname = "root"
                    return tarinfo

                tar.add(file, filter=reset, arcname=file.relative_to(tmpdir))


def main():
    parser = ArgumentParser(
        prog="nuget_pkgs_save_and_restore.py",
        description="Save and restore nuget packages",
    )

    parser.add_argument("action", choices=["save", "backup"]),
    parser.add_argument("projectdir", default=".", type=str)
    parser.add_argument("target", default="action_target", type=str)

    args = parser.parse_args()

    PROJECT_DIR = Path(args.projectdir)
    ACTION = args.action
    ACTION_TARGET = Path(args.target)

    logger.info(f"Do '{ACTION}' for '{PROJECT_DIR.absolute()}' to '{ACTION_TARGET}'")

    if ACTION == "save":
        save(PROJECT_DIR, ACTION_TARGET)

    if ACTION == "backup":
        backup(PROJECT_DIR, ACTION_TARGET)


if __name__ == "__main__":
    main()
