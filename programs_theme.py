import os
from pathlib import Path

def change_alacritty_theme(theme: str):
    """
        Modifies the Alacritty config file at its default location
        calling `flip_comments_based_on_tag` function with `theme`
    """
    config_path = Path(os.getenv('APPDATA')) / 'alacritty' / 'alacritty.toml'
    text = list(config_path.read_text().split('\n'))

    text = flip_comments_based_on_tag(text, '#', theme)
    with open(config_path, 'w') as config:
        config.write('\n'.join(text))

def change_nvim_theme(theme: str):
    """
        Modifies the Neovim config file at its default location
        calling `flip_comments_based_on_tag` function with `theme`
    """
    config_path = Path(os.getenv('APPDATA')) / '..' / 'Local' / 'nvim' / 'init.lua' 
    text = list(config_path.read_text().split('\n'))

    text = flip_comments_based_on_tag(text, '--', theme)
    with open(config_path, 'w') as config:
        config.write('\n'.join(text))

def flip_comments_based_on_tag(lines: list[str], comment: str, tag: str):
    """
        Modifies `lines` by prepending `comment` for each line that does
        not match the specified `tag` and uncommenting matching lines.
        A line matches `tag` if it contains string f'{comment}TAG:{tag}.

        Any repeating `comment` strings at the beginning of a line are
        removed.

        Returns the modified list `lines`
    """
    try:
        contains = lambda substr: lambda tup: substr in tup[1]

        tagged_lines = filter(contains(f'{comment}TAG'), enumerate(lines))
        for i, line in tagged_lines:
            lines[i] = comment + remove_repeating_prefix(line, comment)

        target_tagged_lines = filter(contains(f'{comment}TAG:{tag}'), enumerate(lines))
        target_ind, target_line = next(target_tagged_lines)
        lines[target_ind] = remove_repeating_prefix(target_line, comment)
        return lines
    except StopIteration:
        raise RuntimeError(f'The pattern "TAG:{tag}" not found in any of the lines')

def remove_repeating_prefix(string: str, prefix: str) -> str:
    """
        Returns `string` without sequence of repeating `prefix` at the
        beginning.
    """
    while string.startswith(prefix):
        string = string[len(prefix):]
    return string

    
