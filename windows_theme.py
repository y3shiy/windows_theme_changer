import os
import subprocess
import time
import winreg
from ctypes import windll

REG_PERSONALIZE_PATH = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize'
SPIF_UPDATEINIFILE = 0x0001
SPIF_SENDWININICHANGE = 0x0002
SPI_SETDESKWALLPAPER = 0x0014

def change_apps_theme(theme: str):
    value = {'dark': 0, 'light': 1}[theme]
    set_registry_dword_key(REG_PERSONALIZE_PATH, 'AppsUseLightTheme', value)

def change_system_theme(theme: str):
    value = {'dark': 0, 'light': 1}[theme]
    set_registry_dword_key(REG_PERSONALIZE_PATH, 'SystemUsesLightTheme', value)

def change_wallpaper(wallpaper_path: str):
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
    subprocess.run(['taskkill', '/F', '/IM', 'explorer.exe'])
    time.sleep(1)
    subprocess.Popen(['explorer.exe'])

def set_registry_dword_key(path: str, key: str, value: int):
    domain = winreg.HKEY_CURRENT_USER
    reserved = 0
    access = winreg.KEY_SET_VALUE
    with winreg.OpenKey(domain, path, reserved, access) as reg_key:
        value_type = winreg.REG_DWORD
        reserved = 0
        winreg.SetValueEx(reg_key, key, reserved, value_type, value)

