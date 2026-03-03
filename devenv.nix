{ pkgs, lib, config, inputs, ... }:

{
    packages = with pkgs; [
        (python311.withPackages(p: with p; [
            pygame
        ]))
    ];
}
