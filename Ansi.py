import ctypes
import time
from sys import platform

ESC = 27
ENTER = 13
ARROWDOWN = 1000
ARROWUP = 1001
ARROWLEFT = 1002
ARROWRIGHT = 1003

def dummyGetCh():
    return None

ReadChar = dummyGetCh

def InitAnsi():
    if platform== "linux" or platform == "linux2":
        # linux
        pass

    elif platform == "darwin":
        # OS X
        pass

    elif platform == "win32":
        import msvcrt
        global ReadChar

        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

        keycode = 0

        def GetCh():
            keycode = 0
            if msvcrt.kbhit():
                keycode = ord(msvcrt.getch())
                if keycode == 27: # ESC
                    return ESC
                elif keycode == 13: # Enter
                    return ENTER
                elif keycode == 224: # Special keys (arrows, f keys, ins, del, etc.)
                    keycode = ord(msvcrt.getch())
                    if keycode == 80: # Down arrow
                        return ARROWDOWN
                    elif keycode == 72: # Up arrow
                        return ARROWUP
                    elif keycode == 75: # Left arrow
                        return ARROWLEFT
                    elif keycode == 77: # Up arrow
                        return ARROWRIGHT
                    else:
                        return keycode
                else:
                    return keycode
            else:
                return None

        ReadChar = GetCh


# https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
# https://en.wikipedia.org/wiki/ANSI_escape_code


Black =   u"\u001b[30m"
Red =     u"\u001b[31m"
Green =   u"\u001b[32m"
Yellow =  u"\u001b[33m"
Blue =    u"\u001b[34m"
Magenta = u"\u001b[35m"
Cyan =    u"\u001b[36m"
White =   u"\u001b[37m"

BrightBlack =   u"\u001b[30;1m"
BrightRed =     u"\u001b[31;1m"
BrightGreen =   u"\u001b[32;1m"
BrightYellow =  u"\u001b[33;1m"
BrightBlue =    u"\u001b[34;1m"
BrightMagenta = u"\u001b[35;1m"
BrightCyan =    u"\u001b[36;1m"
BrightWhite =   u"\u001b[37;1m"

BlackBackground =   u"\u001b[40m"
RedBackground =     u"\u001b[41m"
GreenBackground =   u"\u001b[42m"
YellowBackground =  u"\u001b[43m"
BlueBackground =    u"\u001b[44m"
MagentaBackground = u"\u001b[45m"
CyanBackground =    u"\u001b[46m"
WhiteBackground =   u"\u001b[47m"

BrightBlackBackground =   u"\u001b[100;1m"
BrightRedBackground =     u"\u001b[101;1m"
BrightGreenBackground =   u"\u001b[102;1m"
BrightYellowBackground =  u"\u001b[103;1m"
BrightBlueBackground =    u"\u001b[104;1m"
BrightMagentaBackground = u"\u001b[105;1m"
BrightCyanBackground =    u"\u001b[106;1m"
BrightWhiteBackground =   u"\u001b[107;1m"

Bold = u"\u001b[1m"
Dim = u"\u001b[2m"
Underline = u"\u001b[4m"
Reversed = u"\u001b[7m"

Up = u"\u001b[%dA"
Down = u"\u001b[%dB"
Right = u"\u001b[%dC"
Left = u"\u001b[%dD"

NextLine = u"\u001b[1E"
PreviousLine = u"\u001b[1F"

ToColumn = u"\u001b[%dG"

Move = u"\u001b[%d;%dH"

Clear = u"\u001b[2J"
ClearLine = u"\u001b[2K"

Reset = u"\u001b[0m"

HideCursor = u"\u001b[?25l"
ShowCursor = u"\u001b[?25h"

def CursorToColumn(column: int) -> str:
    return ToColumn % column

def MoveUp(count: int = 1) -> str:
    return Up % count

def MoveDown(count: int = 1) -> str:
    return Down % count

def MoveLeft(count: int = 1) -> str:
    return Left % count

def MoveRight(count: int = 1) -> str:
    return Right % count

def MoveCursor(column: int, line: int) -> str:
    return Move % (line, column)

####################################################################################
####################################################################################
####################################################################################

if __name__ == "__main__":
    InitAnsi()
    print(Clear + HideCursor)

    delay = 0.02
    offset = 0
    for i in range(1, 20):
        print(MoveCursor(i + offset, i) + Red + "Red" + Reset)
        time.sleep(delay)

    offset += 4
    for i in reversed(range(1, 20)):
        print(MoveCursor(i + offset, i) + Green + "Green" + Reset)
        time.sleep(delay)

    offset += 6
    for i in range(1, 20):
        print(MoveCursor(i + offset, i) + Yellow + "Yellow" + Reset)
        time.sleep(delay)

    offset += 7
    for i in reversed(range(1, 20)):
        print(MoveCursor(i + offset, i) + Blue + "Blue" + Reset)
        time.sleep(delay)

    offset += 5
    for i in range(1, 20):
        print(MoveCursor(i + offset, i) + Magenta + "Magenta" + Reset)
        time.sleep(delay)

    offset += 8
    for i in reversed(range(1, 20)):
        print(MoveCursor(i + offset, i) + Cyan + "Cyan" + Reset)
        time.sleep(delay)

    offset += 5
    for i in range(1, 20):
        print(MoveCursor(i + offset, i) + White + "White" + Reset)
        time.sleep(delay)

    offset += 6
    for i in reversed(range(1, 20)):
        print(MoveCursor(i + offset, i) + BrightRed + "Red" + Reset)
        time.sleep(delay)

    offset += 4
    for i in range(1, 20):
        print(MoveCursor(i + offset, i) + BrightGreen + "Green" + Reset)
        time.sleep(delay)

    offset += 6
    for i in reversed(range(1, 20)):
        print(MoveCursor(i + offset, i) + BrightYellow + "Yellow" + Reset)
        time.sleep(delay)

    offset += 7
    for i in range(1, 20):
        print(MoveCursor(i + offset, i) + BrightBlue + "Blue" + Reset)
        time.sleep(delay)

    offset += 5
    for i in reversed(range(1, 20)):
        print(MoveCursor(i + offset, i) + BrightMagenta + "Magenta" + Reset)
        time.sleep(delay)

    offset += 8
    for i in range(1, 20):
        print(MoveCursor(i + offset, i) + BrightCyan + "Cyan" + Reset)
        time.sleep(delay)

    offset += 5
    for i in reversed(range(1, 20)):
        print(MoveCursor(i + offset, i) + BrightWhite + "White" + Reset)
        time.sleep(delay)

    print(MoveCursor(1, 18) + ShowCursor)

