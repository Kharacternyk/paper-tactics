{
  outputs = { self, nixpkgs, flake-utils }: flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs { inherit system; };
      disableTests = _: { doCheck = false; };
      getPythonPkgs = pythonPkgs: builtins.attrValues {
        inherit (pythonPkgs)
          websockets nest-asyncio pytest docker
          pytest-testmon hypothesis coverage boto3;
        moto = pythonPkgs.moto.overridePythonAttrs disableTests;
        bidict = pythonPkgs.bidict.overridePythonAttrs disableTests;
      };
      python = pkgs.python39.withPackages getPythonPkgs;
    in
    {
      devShells.default = pkgs.mkShell {
        packages = [ python ];
      };
    }
  );
}
