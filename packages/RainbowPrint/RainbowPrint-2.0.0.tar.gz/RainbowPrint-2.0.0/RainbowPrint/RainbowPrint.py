# 0	终端默认设置
# 1	高亮显示
# 4	使用下划线
# 5	闪烁
# 7	反白显示
# 8	不可见

from enum import Enum, unique
from datetime import datetime


@unique
class TextColor(Enum):
    Default = 0
    BlACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37


@unique
class BackgroundColor(Enum):
    Default = 0
    BlACK = 40
    RED = 41
    GREEN = 42
    YELLOW = 43
    BLUE = 44
    MAGENTA = 45
    CYAN = 46
    WHITE = 47


@unique
class DisplayMode(Enum):
    TERMINAL_DEFAULT_SETTINGS = 0
    HIGHLIGHT = 1
    USE_UNDERLINE = 4
    BLINK = 5
    BACKWHITE_DISPLAY = 7
    INVISIBLE = 8



base_str = '\033[{};{};{}m{}\033[0m'


def rainbow_print(data, display_mode=DisplayMode.HIGHLIGHT, text_color=TextColor.YELLOW,
                  background=BackgroundColor.BLUE):
    """
    Output color text in the terminal

    Args:
        data: Text that needs to be printed.
        display_mode:
        text_color: the color of text.
        background: the color of background.
    """
    print(base_str.format(display_mode.value, text_color.value, background.value, data))


def rich(data, display_mode=DisplayMode.HIGHLIGHT, text_color=TextColor.BlACK,
         background=BackgroundColor.BLUE):
    return base_str.format(display_mode.value, text_color.value, background.value, data)


def get_time():
    return '[{}]'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])


def info(string_data):
    print(get_time(),
          base_str.format(DisplayMode.HIGHLIGHT.value, TextColor.WHITE.value, BackgroundColor.GREEN.value, ' INFO  '),
          green(string_data))


def error(string_data):
    print(get_time(),
          base_str.format(DisplayMode.HIGHLIGHT.value, TextColor.WHITE.value, BackgroundColor.RED.value, ' ERROR '),
          red(string_data))


def debug(string_data):
    print(get_time(),
          base_str.format(DisplayMode.HIGHLIGHT.value, TextColor.WHITE.value, BackgroundColor.MAGENTA.value, ' DEBUG '),
          magenta(string_data))


def red(data):
    base_str = '\033[{}m{}\033[0m'
    return base_str.format(TextColor.RED.value, data)


def black(data):
    base_str = '\033[{}m{}\033[0m'
    return base_str.format(TextColor.BlACK.value, data)


def green(data):
    base_str = '\033[{}m{}\033[0m'
    return base_str.format(TextColor.GREEN.value, data)


def yellow(data):
    base_str = '\033[{}m{}\033[0m'
    return base_str.format(TextColor.YELLOW.value, data)


def blue(data):
    base_str = '\033[{}m{}\033[0m'
    return base_str.format(TextColor.BLUE.value, data)


def magenta(data):
    base_str = '\033[{}m{}\033[0m'
    return base_str.format(TextColor.MAGENTA.value, data)


def cyan(data):
    base_str = '\033[{}m{}\033[0m'
    return base_str.format(TextColor.CYAN.value, data)


def white(data):
    base_str = '\033[{}m{}\033[0m'
    return base_str.format(TextColor.WHITE.value, data)

def default(data):
    base_str = '\033[{}m{}\033[0m'
    return base_str.format(TextColor.Default.value, data)

def rainbow():
    t = [i for i in range(30, 38)]
    b = [i for i in range(40, 48)]
    for tc in t:
        for bc in b:
            print('\033[1;{};{}m{} [textcolor:{}, background:{}]\033[0m'.format(tc, bc, 'RainBow', TextColor(tc).name,
                                                                                BackgroundColor(bc).name))

@unique
class Theme(Enum):
    DEFAULT = (default,default)
    BLUE = (blue,default)
    GREEN = (green, default)
    RED_BLACK = (red,black)
    RED_WHITE = (red,white)
    GREEN_WHITE = (green, white)
    WHITE_RED = (default, red)
    BLUE_YELLOW = (blue, yellow)


def print_table(table, title,theme=Theme.GREEN,rich_mode=False,hilight=[]):
    if hilight != []:
        assert max(hilight) < len(title), "hilight index must < the len of row"
    cloum_max = []
    for cloum in range(0, len(table[0])):
        max_len = max([len(str(data[cloum])) for data in table])
        cloum_max.append(max_len)

    def print_spilt_line(start='|', end='╣', line='-', mid='═',row_color=default):
        print()
        print(row_color(start), end='')
        for index,str_len in enumerate(cloum_max):
            if index!=len(cloum_max)-1:
                print(row_color(line*(str_len+3)+mid),end='')
            else:
                print(row_color(line * (str_len + 3) + end), end='')
        print()

    def print_row(row, row_color, rich_mode=False, is_title=False,hilight=[]):
        for index, data in enumerate(row):
            str_len = cloum_max[index]
            data_len = len(str(data))
            if index in hilight and not is_title:
                data = red(data)
            if rich_mode and index != len(row)-1:
                print(rich(' ' + str(data) + ' ' * (str_len - data_len)+'  ') + '║', end='')
            elif rich_mode and index == len(row)-1:
                print(rich(' ' + str(data) + ' ' * (str_len - data_len)+'  ') + '║', end='')
            else:
                # if is_title:
                print(row_color(' ' + str(data) + ' ' * (str_len - data_len)+'  ║'), end='')
                # else:
                #     print(row_color(' ' + str(data) + ' ' * (str_len - len(str(data)))) + '  |', end='')


    print_spilt_line(start='╔',line='═', end='╗',mid='╦',row_color=theme.value[0])
    for index, row in enumerate(table):
        if index == 0:
            print(theme.value[0]('║'), end='')
            print_row(row, theme.value[0], rich_mode,is_title=True)
            print_spilt_line(start='╠', mid='╬',line='═',end='╣', row_color=theme.value[0])
        elif index == len(table) - 1:
            # last split line
            print(theme.value[1]('║'), end='')
            print_row(row, theme.value[1],hilight=hilight)
            print_spilt_line(start='╚',line='═',mid='╩',end='╝',row_color=theme.value[1])
        else:
            print(theme.value[1]('║'), end='')
            print_row(row, theme.value[1],hilight=hilight)
            print_spilt_line(start='╠',mid='╬',line='═',row_color=theme.value[1])


def help():
    dispaly_mode = '''
     0	终端默认设置
     1	高亮显示
     4	使用下划线
     5	闪烁
     7	反白显示
     8	不可见
    '''
    print(dispaly_mode)



