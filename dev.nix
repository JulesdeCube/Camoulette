
with import <nixpkgs> {};
let
  camoulette = (import ./.) { ocaml=pkgs.ocaml; pythonPackages=pkgs.python310Packages; };
in
mkShell {
  name = "camoulette-shell";
  buildInputs = [
    camoulette
    pkgs.python310Packages.autopep8
  ];
}
