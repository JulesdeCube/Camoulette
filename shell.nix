
with import <nixpkgs> {};
let
  camoulette = (import ./. ) {
    ocaml = pkgs.ocaml;
    pythonPackages = pkgs.python310Packages;
  };
in
pkgs.mkShell {
  name = "camoulette";

  buildInputs = [
    camoulette
    pkgs.python310Packages.autopep8
  ];
}