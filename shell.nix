{ nixpkgs ? import <nixpkgs> {} }:

nixpkgs.mkShell {
  packages = [nixpkgs.poetry];

  nativeBuildInputs = with nixpkgs; [
    python310Packages.poetry-core
    python310
  ];


  LD_LIBRARY_PATH = "${nixpkgs.stdenv.cc.cc.lib}/lib";
}
