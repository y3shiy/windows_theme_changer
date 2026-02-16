## Description

This is a simple Python script which I pesonally use for quickly changing the Windows theme.
It alters the theme even if you can't do it directly from the settings (that is, if you have unactivated Windows).
Currently, it can change only the light/dark mode of apps and system UI, and the wallpapers.

## Usage

You should define your config in an imperative way by modifying the `change_theme.py` source code.
I have provided an example of how I orgranize such config for switching between light and dark styles.
To apply a style I simply run `change_theme.py` providing 'light' or 'dark' as the first argument.

<b>!!! IMPORTANT !!!</b> <br>
Before running anything first read and make sure you understand what `change_theme.py` script does.
Prior to changing configs of other programs (such as Neovim or Alacritty) for the first time
I highly recommend you locate those manually and make backups, so that you won't lose anything accidentally.

## Examples

Here are the examples of Neovim and Alacritty configs for `change_theme.py` code.

### Neovim ("init.lua" file)
``` lua
require('plugins')

vim.o.compatible = false

require('onenord').setup({
--    theme = "light", --TAG:light
    theme = "dark", --TAG:dark
    transparent = true
})
```

### Alacritty ("alacritty.toml" file)
``` toml
[general]
import = [
#     #TAG:default
    "./themes/alacritty-theme/themes/catppuccin_frappe.toml" #TAG:catppuccin_frappe
#    "./themes/alacritty-theme/themes/alabaster.toml" #TAG:alabaster
]
```
