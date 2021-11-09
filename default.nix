{ ocaml, pythonPackages }:

pythonPackages.buildPythonPackage rec {
    name = "camoulette";
    src = ./.;

    propagatedBuildInputs = [
      ocaml
    ];
}