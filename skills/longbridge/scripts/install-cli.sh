#!/usr/bin/env sh
# Install the Longbridge CLI (longbridge-terminal) on macOS / Linux.
# Bundled copy of https://open.longbridge.com/longbridge/longbridge-terminal/install
# so the plugin runs a local file instead of piping a remote script into sh.
#
# Usage: sh install-cli.sh
# Installs to /usr/local/bin when writable (or via sudo when a TTY is available),
# otherwise to ~/.local/bin. Override with LONGBRIDGE_INSTALL_DIR=/some/dir.
set -eu
type curl > /dev/null || { echo "curl: not found"; exit 1; }

bin_name='longbridge'
package_name='longbridge-terminal'
release_base='https://assets.lbkrs.com/github/release/longbridge-terminal'

version=$(curl --silent --fail "$release_base/latest") || version=''
if [ -z "$version" ]; then
  echo "Failed to fetch the latest release." >&2
  exit 1
fi
echo "Latest release: $version"

platform="$(uname | tr "[A-Z]" "[a-z]")"  # Linux => linux
arch="$(uname -m)"  # x86_64, arm64, aarch64, etc.
case "$arch" in
  x86_64) arch="amd64" ;;
  aarch64|arm64) arch="arm64" ;;
esac

# Always use the musl build on Linux – it is statically linked and works on any
# Linux system regardless of the glibc version.
libc=''
if [ "$platform" = "linux" ]; then
  libc='-musl'
fi

download_url="$release_base/$version/$package_name-$platform$libc-$arch.tar.gz"
echo "Downloading $package_name@$version ..."
echo "$download_url"

tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT

curl --fail -Lo "$tmp_dir/$bin_name.tar.gz" "$download_url"
tar zxf "$tmp_dir/$bin_name.tar.gz" -C "$tmp_dir"

install_dir="${LONGBRIDGE_INSTALL_DIR:-/usr/local/bin}"
if [ -z "${LONGBRIDGE_INSTALL_DIR:-}" ] && [ "$(id -u)" -ne 0 ] && [ ! -w "$install_dir" ]; then
  if [ -t 0 ] && command -v sudo > /dev/null; then
    sudo mv "$tmp_dir/$bin_name" "$install_dir/$bin_name"
    install_dir=''
  else
    install_dir="$HOME/.local/bin"
  fi
fi
if [ -n "$install_dir" ]; then
  mkdir -p "$install_dir"
  mv "$tmp_dir/$bin_name" "$install_dir/$bin_name"
  case ":$PATH:" in
    *":$install_dir:"*) ;;
    *) echo "Note: $install_dir is not on your PATH. Add it, e.g. export PATH=\"$install_dir:\$PATH\"" ;;
  esac
fi

echo "Longbridge CLI $version has installed successfully."
echo ""
echo "Run \`longbridge auth login\` to authenticate, then \`longbridge -h\` for help."
