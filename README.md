# dicostapres

`di`s`co`rd `sta`tus `pre`sence `s`ystem is a minimal presence system for discord.

dicostapres is a tiny and lightweight Python script that allows you to:

1. Set a custom online status for your Discord account
2. Display a custom status message
3. Keep your Discord account online 24/7

## What This Project Is Not

- A bot
- A Python app which uses the discord.py library
- Free from possible abandonment
- Anything other than a toy project

## Prerequisites

- Python `3.11`+
- Poetry
- Discord Token

### Nix

This project is [nix flakes](./flake.nix) ready. Just hook into the shell and
install the dependencies using `poetry`.

## Installation

1. `git clone` & `cd` into the repository

   ```sh
   git clone https://github.com/anntnzrb/dicostapres
   cd dicostapres/
   ```

2. Install dependencies using `poetry`
   ```sh
   poetry install
   ```
3. Create the `.env` file by `cp`-ing the `.env.example` file

   ```sh
   cp ./.env.example ./.env
   ```

4. Modify the `.env` file accordingly

## Usage

The `3` environment variables that are required to set are:

- `DISCORD_TOKEN` - The user's Discord token
- `DISCORD_STATUS` - The status of the user. Can be `online`, `idle`, `dnd`
- `DISCORD_STATUS_MSG` - The custom status message

### Running

Simply execute `just run`:

```sh
just run
```

[Installation](#Installation) steps #3 and #4 may be omitted if the environment
variables are set manually. However, the `.env` method is preferred for less
verbosity.

```
DISCORD_TOKEN=Ujg5NzI3Nz... DISCORD_STATUS=online DISCORD_STATUS_MSG='Playing with dicostapres' just run
```

## COPYING

Refer to the [COPYING](./COPYING) file for licensing information.

Unless otherwise noted, all code herein is distributed under the terms of the
[GNU General Public License Version 3 or later](https://www.gnu.org/licenses/gpl-3.0.en.html).
