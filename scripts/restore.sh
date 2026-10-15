#!/usr/bin/env bash
set -Eeuo pipefail

REPO="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG_DIR="$REPO/config"
BACKUP="$HOME/.config/dotfiles-backup-$(date +%Y%m%d-%H%M%S)"

APPS=(
    hypr waybar rofi dunst waypaper wlogout fastfetch
    fish ghostty gtk-3.0 gtk-4.0 nwg-look qt6ct xsettingsd
)

if [[ $EUID -eq 0 ]]; then
    echo "Run as your normal user, not root."
    exit 1
fi

echo "Repository: $REPO"
echo "This will link selected configs into ~/.config."
echo "Existing configs will be backed up to: $BACKUP"
read -r -p "Continue? [y/N] " answer
[[ "$answer" =~ ^[Yy]$ ]] || exit 0

mkdir -p "$HOME/.config"

for app in "${APPS[@]}"; do
    source_dir="$CONFIG_DIR/$app"
    target="$HOME/.config/$app"

    [[ -d "$source_dir" ]] || continue

    if [[ -L "$target" ]]; then
        echo "Skipping existing symlink: $target"
        continue
    fi

    if [[ -e "$target" ]]; then
        mkdir -p "$BACKUP"
        mv -- "$target" "$BACKUP/"
        echo "Backed up: $target"
    fi

    ln -s -- "$source_dir" "$target"
    echo "Linked: $target"
done

echo "Restore complete."
echo "Backup location: $BACKUP"
