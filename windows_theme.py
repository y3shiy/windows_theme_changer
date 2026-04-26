import os
import re
import subprocess
import time
import winreg
from ctypes import windll

REG_PERSONALIZE_PATH = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
REG_DWM_PATH = r'SOFTWARE\Microsoft\Windows\DWM'
REG_EXPLORER_ACCENT_PATH = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Accent'

ACCENT_COLOR_PATTERN = re.compile(r'^#[0-9A-Fa-f]{6}$')
ACCENT_COLOR_ALPHA = 0xFF
ACCENT_PALETTE_COLOR_OFFSET = 0x14

# Constants from: https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-systemparametersinfoa
SPIF_UPDATEINIFILE = 0x0001
SPIF_SENDWININICHANGE = 0x0002
SPI_SETDESKWALLPAPER = 0x0014

def change_apps_theme(theme: str):
    """
        Changes the theme for all opened apps acting as 
        "Choose default app mode" setting from 'Personalization > Colors'.

        String `theme` should be either 'dark' or 'light'
    """
    value = {'dark': 0, 'light': 1}[theme]
    set_registry_dword_key(REG_PERSONALIZE_PATH, 'AppsUseLightTheme', value)

def change_system_theme(theme: str):
    """
        Changes the theme for Taskbar and Start menu acting as
        "Choose default app mode" setting from 'Personalization > Colors'.

        String `theme` should be either 'dark' or 'light'
    """
    value = {'dark': 0, 'light': 1}[theme]
    set_registry_dword_key(REG_PERSONALIZE_PATH, 'SystemUsesLightTheme', value)

def set_accent_color(color: str):
    """
        Sets the Windows accent color from a string in '#RRGGBB' format.
    """
    value = parse_accent_color(color)
    set_accent_palette_color(color)
    set_registry_dword_key(REG_EXPLORER_ACCENT_PATH, 'AccentColorMenu', value)

def set_accent_on_start_taskbar(enabled: bool):
    """ Controls accent color usage on Start and taskbar surfaces. """
    set_registry_bool_key(REG_PERSONALIZE_PATH, 'ColorPrevalence', enabled)

def set_accent_on_title_bars_and_borders(enabled: bool):
    """ Controls accent color usage on title bars and window borders. """
    set_registry_bool_key(REG_DWM_PATH, 'ColorPrevalence', enabled)

def set_transparency(enabled: bool):
    """ Controls Windows transparency effects. """
    set_registry_bool_key(REG_PERSONALIZE_PATH, 'EnableTransparency', enabled)

def change_wallpaper(wallpaper_path: str):
    """ Updates wallpapers with ones located by `wallpaper_path` """
    if not os.path.isfile(wallpaper_path):
        raise FileNotFoundError(f'Wallpapers not found "{wallpaper_path}"')
    ui_action = SPI_SETDESKWALLPAPER
    ui_param = 0
    pv_param = wallpaper_path
    flags = SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE
    is_ok = windll.user32.SystemParametersInfoW(ui_action, ui_param, pv_param, flags)
    if not is_ok:
        raise RuntimeError('Failed to put on the wallpapers')

def restart_explorer():
    """ Restarts the explorer process to apply made theme changes """
    subprocess.run(['taskkill', '/F', '/IM', 'explorer.exe'])
    time.sleep(1)
    subprocess.Popen(['explorer.exe'])

def restart_dwm():
    """ Restarts the Desktop Window Manager process if Windows allows it. """
    process = subprocess.run(['taskkill', '/F', '/IM', 'dwm.exe'], check=False)
    if process.returncode != 0:
        raise RuntimeError('Failed to restart dwm.exe')

def parse_accent_color(color: str) -> int:
    """ Converts '#RRGGBB' to the registry DWORD expected by DWM color values. """
    if ACCENT_COLOR_PATTERN.fullmatch(color) is None:
        raise ValueError(f'Accent color should have format "#RRGGBB", got "{color}"')

    red = int(color[1:3], 16)
    green = int(color[3:5], 16)
    blue = int(color[5:7], 16)
    return (ACCENT_COLOR_ALPHA << 24) | (blue << 16) | (green << 8) | red

def set_accent_palette_color(color: str):
    """ Updates the AccentPalette entry with the RRGGBB bytes used by Explorer. """
    palette = bytearray(get_registry_value(REG_EXPLORER_ACCENT_PATH, 'AccentPalette'))
    color_offset = ACCENT_PALETTE_COLOR_OFFSET
    if len(palette) < color_offset + 4:
        raise RuntimeError('AccentPalette is shorter than expected')

    palette[color_offset + 0] = int(color[1:3], 16)
    palette[color_offset + 1] = int(color[3:5], 16)
    palette[color_offset + 2] = int(color[5:7], 16)
    palette[color_offset + 3] = 0
    set_registry_binary_key(REG_EXPLORER_ACCENT_PATH, 'AccentPalette', bytes(palette))

def set_registry_bool_key(path: str, key: str, value: bool):
    """ Updates `key` located in registry at `path` with a boolean `value`. """
    set_registry_dword_key(path, key, int(value))

def get_registry_value(path: str, key: str):
    """ Returns the value stored for `key` at registry `path`. """
    domain = winreg.HKEY_CURRENT_USER
    reserved = 0
    access = winreg.KEY_QUERY_VALUE
    with winreg.OpenKey(domain, path, reserved, access) as reg_key:
        value, _ = winreg.QueryValueEx(reg_key, key)
        return value

def set_registry_binary_key(path: str, key: str, value: bytes):
    """ Updates `key` located in registry at `path` with binary `value`. """
    domain = winreg.HKEY_CURRENT_USER
    reserved = 0
    access = winreg.KEY_SET_VALUE
    with winreg.CreateKeyEx(domain, path, reserved, access) as reg_key:
        value_type = winreg.REG_BINARY
        reserved = 0
        winreg.SetValueEx(reg_key, key, reserved, value_type, value)

def set_registry_dword_key(path: str, key: str, value: int):
    """ Updates `key` located in registry at `path` with `value` """
    domain = winreg.HKEY_CURRENT_USER
    reserved = 0
    access = winreg.KEY_SET_VALUE
    with winreg.CreateKeyEx(domain, path, reserved, access) as reg_key:
        value_type = winreg.REG_DWORD
        reserved = 0
        winreg.SetValueEx(reg_key, key, reserved, value_type, value)
