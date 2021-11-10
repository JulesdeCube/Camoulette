{ ocaml, pythonPackages }:
pythonPackages.buildPythonPackage rec {
    name = "camoulette";
    version = "1.0.0";
    src = ./.;

    propagatedBuildInputs = [
      ocaml
    ];
}