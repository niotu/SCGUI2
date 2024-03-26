"""STYLES"""

import platform

CONFIGURE = ''

OP_SYSTEM = platform.system()
if OP_SYSTEM == "Windows":
    CONFIGURE = "config/win_paths.json"
    SEPARATOR = "\\"
elif OP_SYSTEM == "Linux":
    CONFIGURE = "config/linux_paths.json"
    SEPARATOR = "/"

BG_COLOR = "252525"
ACCENT_COLOR = "A4C6D9"
STYLES_ROOT = "sources/styles/style.qss"

SPACING = 0
MAIN_ICON_ROOT = ""
COMMON_ICON_ROOT = "icons/states/common.png"
LOADING_ICON_ROOT = "icons/states/loading.png"
ERROR_ICON_ROOT = "icons/states/error.png"
DONE_ICON_ROOT = "icons/states/done.png"
SETTINGS_ICON_ROOT = "icons/buttons/settings.png"
UPDATE_ICON_ROOT = "icons/buttons/update.png"

ALFA = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'e',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'y',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': '',
    'ф': 'f',
    'х': 'h',
    'ц': 'ts',
    'ч': 'ch',
    'ш': 'sh',
    'щ': 'sch',
    'ъ': '',
    'ы': 'y',
    'ь': '',
    'э': 'e',
    'ю': 'y',
    'я': 'ya'
}

RUSSIAN = "абвгдеёжзиклмнопрстуфхчшщъыиэюя"
