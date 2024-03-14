# prints this menu
default:
    @just --list

# format source tree
fmt:
    treefmt

# run app
run:
    poetry run app
