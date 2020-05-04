import ctypes
import time
from sys import platform, stdout
from KeyGetter import KeyGetter

keyGetter = None

class Ansi():

    ESC = 27
    ENTER = 13

    ARROWDOWN = 57424
    ARROWUP = 57416
    ARROWLEFT = 57419
    ARROWRIGHT = 57421

    PAGEUP = 57417
    PAGEDOWN = 57425

    HOME = 57415
    END = 57423

    DEL = 57427
    INSERT = 57426

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

    @staticmethod
    def CursorToColumn(column: int) -> str:
        return Ansi.ToColumn % column

    @staticmethod
    def MoveUp(count: int = 1) -> str:
        return Ansi.Up % count

    @staticmethod
    def MoveDown(count: int = 1) -> str:
        return Ansi.Down % count

    @staticmethod
    def MoveLeft(count: int = 1) -> str:
        return Ansi.Left % count

    @staticmethod
    def MoveRight(count: int = 1) -> str:
        return Ansi.Right % count

    @staticmethod
    def MoveCursor(column: int, line: int) -> str:
        return Ansi.Move % (line, column)

    @staticmethod
    def Flush():
        stdout.flush()

    @staticmethod
    def Init():
        if platform== "linux" or platform == "linux2":
            # linux
            pass

        elif platform == "darwin":
            # OS X
            pass

        elif platform == "win32":
            import msvcrt
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    @staticmethod
    def GetKey():
        global keyGetter

        if keyGetter == None:
            keyGetter = KeyGetter()
        
        try:
            if keyGetter.kbhit():
                ch = keyGetter.getch(False)
                ch1 = ord(ch)

                if ch1 == 224:
                    ch = keyGetter.getch(False)
                    ch2 = ord(ch)
                    
                    return (ch1 << 8) | ch2

                return ch1

            return None
        except KeyboardInterrupt:
            pass
        

# https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
# https://en.wikipedia.org/wiki/ANSI_escape_code

####################################################################################
####################################################################################
####################################################################################

if __name__ == "__main__":

    Ansi.Init()

    print(Ansi.Clear + Ansi.HideCursor, end = "")

    print(Ansi.Red + " Red " + Ansi.Reset, end = "")
    print(Ansi.BrightRed + " Bright Red " + Ansi.Reset, end = "")
    print(Ansi.RedBackground + " Red Background " + Ansi.Reset, end = "")

    print(Ansi.MoveDown(2) + Ansi.BrightYellow + Ansi.CursorToColumn(1) + "Press ESC ", end = "")

    Ansi.Flush()

    while True:
        ch = Ansi.GetKey()
        if ch != None:
            print(ch, repr(ch))
        time.sleep(0.2)

    print(Ansi.MoveDown(2) + Ansi.BrightGreen + Ansi.CursorToColumn(1) + "Done ", end = "")

    print(Ansi.ShowCursor, end = "")

