# prints this menu
default:
    @just --list

# format source tree
fmt:
    treefmt

# run app
run:
    poetry run app

# update flake inputs
update-flake:
    nix flake update --commit-lock-file --option commit-lockfile-summary 'chore(flake): update lockfile'

# update python dependencies
update-python:
    poetry update
    git add poetry.lock && git commit -m 'chore(python): update lockfile'