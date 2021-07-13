{ pkgs ? import <nixpkgs> { } }:

pkgs.python3Packages.buildPythonApplication {
  name = "paper-tactics";
  src = ./.;
  propagatedBuildInputs = with pkgs; [
    python3Packages.flask
  ];
  nativeBuildInputs = with pkgs; [
    python3Packages.pytest
    python3Packages.hypothesis
  ];
}
