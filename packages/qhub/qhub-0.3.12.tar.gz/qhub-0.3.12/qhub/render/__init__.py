import pathlib
import collections
import json
import os
from shutil import copyfile
from gitignore_parser import parse_gitignore

from ruamel import yaml
from cookiecutter.generate import generate_files
from ..version import __version__
from ..constants import TERRAFORM_VERSION
from ..utils import pip_install_qhub, QHUB_GH_BRANCH


def patch_dask_gateway_extra_config(config):
    """Basically the current dask_gateway helm chart only allows one
    update to extraContainerConfig and extraPodConfig for the workers
    and scheduler. Thus we need to copy the configuration done in
    these settings. The only critical one is mounting the conda store
    directory.

    """
    conda_store_volume = {
        "name": "conda-store",
        "persistentVolumeClaim": {"claimName": "conda-store-dev-share"},
    }
    extra_pod_config = {"volumes": [conda_store_volume]}

    merge_config_for = ["worker_extra_pod_config", "scheduler_extra_pod_config"]

    if "profiles" in config and "dask_worker" in config["profiles"]:
        for worker_name, worker_config in config["profiles"]["dask_worker"].items():
            for config_name in merge_config_for:
                if config_name in worker_config:
                    worker_config[config_name] = deep_merge(
                        worker_config[config_name], extra_pod_config
                    )


def patch_versioning_extra_config(config):
    """
    Set defaults for qhub_version and pip install command
    because they depend on __version__ so cannot be static in cookiecutter.json
    """
    if "qhub_version" not in config:
        config["qhub_version"] = __version__

    config["pip_install_qhub"] = pip_install_qhub

    config["QHUB_GH_BRANCH"] = QHUB_GH_BRANCH

    if "terraform_version" not in config:
        config["terraform_version"] = TERRAFORM_VERSION


def deep_merge(d1, d2):
    """Deep merge two dictionaries.
    >>> value_1 = {
    'a': [1, 2],
    'b': {'c': 1, 'z': [5, 6]},
    'e': {'f': {'g': {}}},
    'm': 1,
    }

    >>> value_2 = {
        'a': [3, 4],
        'b': {'d': 2, 'z': [7]},
        'e': {'f': {'h': 1}},
        'm': [1],
    }

    >>> print(deep_merge(value_1, value_2))
    {'m': 1, 'e': {'f': {'g': {}, 'h': 1}}, 'b': {'d': 2, 'c': 1, 'z': [5, 6, 7]}, 'a': [1, 2, 3,  4]}
    """
    if isinstance(d1, dict) and isinstance(d2, dict):
        d3 = {}
        for key in d1.keys() | d2.keys():
            if key in d1 and key in d2:
                d3[key] = deep_merge(d1[key], d2[key])
            elif key in d1:
                d3[key] = d1[key]
            elif key in d2:
                d3[key] = d2[key]
        return d3
    elif isinstance(d1, list) and isinstance(d2, list):
        return [*d1, *d2]
    else:  # if they don't match use left one
        return d1


def render_template(output_directory, config_filename, force=False):
    import qhub

    input_directory = pathlib.Path(qhub.__file__).parent / "template"

    # would be nice to remove assumption that input directory
    # is in local filesystem
    input_directory = pathlib.Path(input_directory)
    if not input_directory.is_dir():
        raise ValueError(f"input directory={input_directory} is not a directory")

    output_directory = pathlib.Path(output_directory).resolve()
    # due to cookiecutter requiring a template directory folder
    # we take the output directory and split into two components
    repo_directory = output_directory.name
    output_directory = output_directory.parent

    # mkdir all the way down to repo dir so we can copy .gitignore into it in remove_existing_renders
    (output_directory / repo_directory).mkdir(exist_ok=True, parents=True)

    filename = pathlib.Path(config_filename)

    if not filename.is_file():
        raise ValueError(f"cookiecutter configuration={filename} is not filename")

    with filename.open() as f:
        config = yaml.safe_load(f)
        config["repo_directory"] = repo_directory
        patch_dask_gateway_extra_config(config)

    with (input_directory / "cookiecutter.json").open() as f:
        config = collections.ChainMap(config, json.load(f))

    patch_versioning_extra_config(config)

    remove_existing_renders(
        source_repo_dir=input_directory / "{{ cookiecutter.repo_directory }}",
        dest_repo_dir=output_directory / repo_directory,
    )

    generate_files(
        repo_dir=str(input_directory),
        context={"cookiecutter": config},
        output_dir=str(output_directory),
        overwrite_if_exists=force,
    )


def remove_existing_renders(source_repo_dir, dest_repo_dir):
    """
    Remove existing folder structure in output_dir apart from:
    Files matching gitignore entries from the source template
    Anything the user has added to a .qhubignore file in the output_dir (maybe their own github workflows)

    No FILES in the dest_repo_dir are deleted.

    The .git folder remains intact

    Inputs must be pathlib.Path
    """
    copyfile(str(source_repo_dir / ".gitignore"), str(dest_repo_dir / ".gitignore"))

    gitignore_matches = parse_gitignore(dest_repo_dir / ".gitignore")

    if (dest_repo_dir / ".qhubignore").is_file():
        qhubignore_matches = parse_gitignore(dest_repo_dir / ".qhubignore")
    else:

        def qhubignore_matches(_):
            return False  # Dummy blank qhubignore

    for root, dirs, files in os.walk(dest_repo_dir, topdown=False):
        if (
            root.startswith(f"{str(dest_repo_dir)}/.git/")
            or root == f"{str(dest_repo_dir)}/.git"
        ):
            # Leave everything in the .git folder
            continue

        root_path = pathlib.Path(root)

        if root != str(
            dest_repo_dir
        ):  # Do not delete top-level files such as qhub-config.yaml!
            for file in files:

                if not gitignore_matches(root_path / file) and not qhubignore_matches(
                    root_path / file
                ):

                    os.remove(root_path / file)

        for dir in dirs:
            if (
                not gitignore_matches(root_path / dir)
                and not (dir == ".git" and root_path == dest_repo_dir)
                and not qhubignore_matches(root_path / dir)
            ):
                try:
                    os.rmdir(root_path / dir)
                except OSError:
                    pass  # Silently fail if 'saved' files are present so dir not empty
