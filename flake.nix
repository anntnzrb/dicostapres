{
  description = "dicostapres";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    # src tree formatter
    treefmt-nix.url = "github:numtide/treefmt-nix/main";
    treefmt-nix.inputs.nixpkgs.follows = "nixpkgs";

    # poetry + nix
    poetry2nix.url = "github:nix-community/poetry2nix/master";
    poetry2nix.inputs.nixpkgs.follows = "nixpkgs";

    # => devenv
    devenv.url = "github:cachix/devenv/main";
    devenv.inputs.nixpkgs.follows = "nixpkgs";
    nix2container.url = "github:nlewo/nix2container/master";
    nix2container.inputs.nixpkgs.follows = "nixpkgs";
    mk-shell-bin.url = "github:rrbutani/nix-mk-shell-bin/main";
  };

  nixConfig = {
    extra-trusted-public-keys = [ "devenv.cachix.org-1:w1cLUi8dv3hnoSPGAuibQv+f9TZLr6cv/Hm9XgU50cw=" ];
    extra-substituters = [ "https://devenv.cachix.org" ];
  };

  outputs = inputs@{ flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = with inputs; [
        devenv.flakeModule
        treefmt-nix.flakeModule
      ];
      systems = [ "x86_64-linux" "i686-linux" "x86_64-darwin" "aarch64-linux" "aarch64-darwin" ];

      perSystem = { config, self', inputs', pkgs, system, ... }: {
        devenv.shells.default = {
          languages = {
            nix.enable = true;
            python = {
              enable = true;
              poetry = {
                enable = true;
                activate.enable = true;
                install.enable = true;
              };
            };
          };

          dotenv.enable = true;

          packages = with pkgs; [
            just
            config.treefmt.build.wrapper

            # python
            isort
            nodePackages_latest.pyright
          ];

          enterShell = ''
            cat <<EOF

              📡 Get started: 'just <recipe>'
              `just`

            EOF
          '';
        };

        treefmt.config = {
          projectRootFile = "flake.nix";
          programs = {
            nixpkgs-fmt.enable = true;
            black.enable = true;
          };
          settings.formatter.isort = {
            command = pkgs.isort;
            includes = [ "*.py" ];
          };
        };
      };
    };
}
