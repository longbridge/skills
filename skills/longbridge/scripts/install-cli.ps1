#!/usr/bin/env pwsh
# Longbridge Terminal CLI installer for Windows
# Bundled copy of https://open.longbridge.com/longbridge/longbridge-terminal/install.ps1
# so the plugin runs a local file instead of piping a remote script into iex.
# The archive's SHA-256 is checked against the .sha256 published on the GitHub
# release before anything is installed.
# Usage: pwsh -File install-cli.ps1   (or: powershell -ExecutionPolicy Bypass -File install-cli.ps1)

$ErrorActionPreference = 'Stop'

$repo        = 'longbridge/longbridge-terminal'
$binName     = 'longbridge'
$packageName = 'longbridge-terminal'
$installDir  = Join-Path $env:LOCALAPPDATA 'Programs\longbridge'

# ── Resolve latest release version ───────────────────────────────────────────

Write-Host "Fetching latest release..."

try {
    $version = (Invoke-WebRequest -Uri "https://assets.lbkrs.com/github/release/longbridge-terminal/latest" -UseBasicParsing -TimeoutSec 15).Content.Trim()
    if (-not $version) {
        throw "Failed to fetch the latest release."
    }
} catch {
    throw "Failed to fetch the latest release: $_"
}

Write-Host "Latest release: $version"

# ── Download ──────────────────────────────────────────────────────────────────

$archive     = "$packageName-windows-amd64.zip"
$downloadUrl = "https://assets.lbkrs.com/github/release/longbridge-terminal/$version/$archive"
$checksumUrl = "https://github.com/longbridge/longbridge-terminal/releases/download/$version/$archive.sha256"

Write-Host "Downloading $packageName@$version ..."
Write-Host $downloadUrl

$tmpDir  = Join-Path $env:TEMP ([System.IO.Path]::GetRandomFileName())
$zipPath = Join-Path $tmpDir "$binName.zip"

New-Item -ItemType Directory -Path $tmpDir | Out-Null

try {
    $wc = New-Object System.Net.WebClient
    $wc.DownloadFile($downloadUrl, $zipPath)
    $wc.Dispose()

    # ── Verify checksum ───────────────────────────────────────────────────────

    try {
        $expected = ((Invoke-WebRequest -Uri $checksumUrl -UseBasicParsing -TimeoutSec 15).Content.Trim() -split '\s+')[0]
    } catch {
        throw "Failed to fetch the checksum for ${archive}; aborting: $_"
    }
    $actual = (Get-FileHash -Path $zipPath -Algorithm SHA256).Hash
    if ($actual -ne $expected) {
        throw "Checksum mismatch for $archive (expected $expected, got $actual); aborting."
    }
    Write-Host "Checksum verified."

    # ── Extract ───────────────────────────────────────────────────────────────

    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::ExtractToDirectory($zipPath, $tmpDir)

    # ── Install ───────────────────────────────────────────────────────────────

    if (-not (Test-Path $installDir)) {
        New-Item -ItemType Directory -Path $installDir | Out-Null
    }

    $srcExe  = Join-Path $tmpDir "$binName.exe"
    $destExe = Join-Path $installDir "$binName.exe"
    Move-Item -Path $srcExe -Destination $destExe -Force

} finally {
    Remove-Item -Recurse -Force $tmpDir -ErrorAction SilentlyContinue
}

# ── Add to user PATH if needed ────────────────────────────────────────────────

$userPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
if ($userPath -notlike "*$installDir*") {
    $newPath = ($userPath.TrimEnd(';') + ";$installDir").TrimStart(';')
    [Environment]::SetEnvironmentVariable('PATH', $newPath, 'User')
    Write-Host ""
    Write-Host "Added $installDir to your PATH."
    Write-Host "Restart your terminal for the PATH change to take effect."
}

Write-Host ""
Write-Host "Longbridge CLI $version has been installed successfully."
Write-Host ""
Write-Host "Run 'longbridge auth login' to authenticate, then 'longbridge -h' for help."
Write-Host ""
