{
  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = inputs@{ nixpkgs, self, flake-parts, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [ "x86_64-linux" "aarch64-linux" "aarch64-darwin" "x86_64-darwin" ];

      perSystem = { config, self', inputs', pkgs, lib, system, ... }: rec {
        packages.psycopg2-pool = pkgs.python3Packages.buildPythonPackage rec {
          pname = "psycopg2-pool";
          version = "1.2";
          dontCheckRuntimeDeps = true;
          nativeBuildInputs = with pkgs.python3Packages; [
            wheel
            setuptools
          ];
          propagatedBuildInputs = with pkgs.python3Packages; [
            psycopg2
          ];
          pyproject = true;
          src = pkgs.fetchPypi {
            inherit pname version;
            hash = "sha256-6ew41a8Vt871VGRSeXk1EpyZSCslZG8liiF4a/uCa/M";
          };
          pythonImportsCheck = [
            "psycopg2_pool"
          ];
        };

        packages.django-rest = pkgs.python3Packages.buildPythonPackage rec {
          dontCheckRuntimeDeps = true;
          pname = "django-rest";
          version = "0.8.7";
          nativeBuildInputs = with pkgs.python3Packages; [
            wheel
            setuptools
          ];
          propagatedBuildInputs = with pkgs.python3Packages; [
          ];
          pyproject = true;
          src = pkgs.fetchPypi {
            inherit pname version;
            hash = "sha256-JKDspqpThkr/yrWogBc/cB5Th61OWIXhLIEYRDLW4Vs=";
          };
          pythonImportsCheck = [
            "django_rest"
          ];
        };

        packages.postgres = pkgs.python3Packages.buildPythonPackage rec {
          dontCheckRuntimeDeps = true;
          pname = "postgres";
          version = "4.0";
          nativeBuildInputs = with pkgs.python3Packages; [
            wheel
            setuptools
          ];
          propagatedBuildInputs = with pkgs.python3Packages; [
            psycopg2
            packages.psycopg2-pool
          ];
          pyproject = true;
          src = pkgs.fetchPypi {
            inherit pname version;
            hash = "sha256-Z8V94QwNOc1eNDfu96yJWytTdHYDs+3NJh3t7FrATUw";
          };
          pythonImportsCheck = [
            "postgres"
          ];
        };

        packages.python-for-cars = pkgs.python3.withPackages (p: with p; [
          asgiref
          certifi
          charset-normalizer
          django
          djangorestframework
          djangorestframework-simplejwt
          docker
          drf-yasg
          idna
          packages.django-rest
          packages.postgres
          packaging
          psycopg2
          pyjwt
          pytz
          requests
          setuptools
          six
          sqlparse
          pyyaml
          urllib3
        ]);

        packages.cars = pkgs.runCommandLocal "cars-server" { } ''
          cp ${self}/cars build -r
          chmod +w --recursive build
          sed -i -e '/PASSWORD.:/d' ./build/cars/settings.py
          sed -i -e '/PORT.:/d' ./build/cars/settings.py
          sed -i -e '/HOST.:/d' ./build/cars/settings.py
          sed -i -e 's/cars_admin/cars/' ./build/cars/settings.py
          cp build $out -r
        '';

        packages.manage = (pkgs.writeScriptBin "manage" ''
          ${lib.getExe packages.python-for-cars} ${packages.cars}/manage.py ''${1:-help}
        '');

        checks.default = nixpkgs.lib.nixos.runTest {
          name = "cars-server-start-test";

          nodes.machine = self.nixosModules.default;

          hostPkgs = pkgs;

          testScript = ''
            start_all()
            machine.wait_for_unit("cars.service")
            machine.wait_for_open_port(8000)
            machine.succeed("curl 127.0.0.1:8000")
          '';
        };
      };

      flake = {
        nixosModules.default = { pkgs, lib, ... }: {
          networking.firewall.allowedTCPPorts = [ 8000 ];

          users.users.cars = {
            isNormalUser = true;
            group = "cars";
            password = "cars";
          };
          users.groups.cars = { };

          services = {
            postgresql = {
              enable = true;
              ensureUsers = [{
                name = "cars";
                ensureDBOwnership = true;
              }];
              ensureDatabases = [ "cars" ];
            };
          };

          systemd.services.cars = {
            enable = true;

            description = "Cars API";
            wants = [ "postgresql.target" "network-online.target" ];
            after = [ "postgresql.target" "network-online.target" ];
            wantedBy = [ "multi-user.target" ];

            preStart = "${lib.getExe self.packages.${pkgs.stdenv.system}.manage} migrate";

            serviceConfig = {
              User = "cars";
              Group = "cars";
              WorkingDirectory = "/tmp";
              ExecStart = "${lib.getExe pkgs.bash} -c '${lib.getExe self.packages.${pkgs.stdenv.system}.manage} runserver'";
            };
          };
        };

        nixosConfigurations.container = nixpkgs.lib.nixosSystem {
          system = "x86_64-linux";
          modules =
            [
              self.nixosModules.default
              ({ pkgs, ... }: {
                boot.isContainer = true;

                networking.useDHCP = false;
                networking.firewall.enable = false;

                environment.systemPackages = [
                  self.packages.${pkgs.stdenv.system}.python-for-cars
                  self.packages.${pkgs.stdenv.system}.manage
                  pkgs.shadow
                ];
              })
            ];
        };
      };
    };
}
