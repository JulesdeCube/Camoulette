
with import <nixpkgs> {};
let camoulette = pkgs.python310Packages.buildPythonPackage rec {
  name = "camoulette";
  src = ./camoulette;
  propagatedBuildInputs = [
    pkgs.python310Packages.autopep8
    pkgs.ocaml
  ];
}:

