# Copy to root as replit.nix if Chromium/system libraries are unavailable.
{ pkgs }: {
  deps = [ pkgs.chromium pkgs.nodejs_22 pkgs.python311 ];
}
