#!python
import sys 
import windows_theme as windows
import programs_theme as programs 

WALLPAPER_DARK = r'C:\Users\y3shiy\Pictures\Desktop Backgrounds\marek-piwnicki-XrkML1U1J68-unsplash.jpg'
WALLPAPER_LIGHT = r'C:\Users\y3shiy\Pictures\Desktop Backgrounds\robin-noguier-3pC6oFadbF8-unsplash.jpg'

def apply_dark_theme():
    windows.change_apps_theme('dark')
    windows.change_system_theme('dark')
    windows.change_wallpaper(WALLPAPER_DARK)
    windows.restart_explorer()

    programs.change_alacritty_theme('catppuccin_frappe')
    programs.change_nvim_theme('dark')

def apply_light_theme():
    windows.change_apps_theme('light')
    windows.change_system_theme('light')
    windows.change_wallpaper(WALLPAPER_LIGHT)
    windows.restart_explorer()

    programs.change_alacritty_theme('alabaster')
    programs.change_nvim_theme('light')

def main(args: list[str]):
    if len(args) < 2:
        raise RuntimeError('Too few arguments')
    theme = args[1] 
    match theme:
        case 'dark':
            apply_dark_theme()
        case 'light':
            apply_light_theme()
        case _: 
            raise RuntimeError(f'Unknown theme name "{theme}"')

if __name__ == '__main__':
    main(sys.argv)
