{
  outputs = { self, nixpkgs, flake-utils }: flake-utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs { inherit system; };
      get-python-pkgs = python-pkgs: with python-pkgs; [
        bidict
        websockets
        nest-asyncio
        pytest
        pytest-testmon
        hypothesis
        coverage
        boto3
      ];
    in
    {
      devShells.default = pkgs.mkShell {
        packages = [
          (pkgs.python39.withPackages get-python-pkgs)
        ];
      };
    }
  );
}
