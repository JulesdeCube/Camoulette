
with import <nixpkgs> {};
let
  camoulette = (import ./. ) {
    ocaml = pkgs.ocaml;
    pythonPackages = pkgs.python38Packages;
  };
in
pkgs.mkShell {
  name = "camoulette";

  buildInputs = [
    camoulette
    pkgs.python38Packages.autopep8
  ];
}
