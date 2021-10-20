import os

WORK_PATH = os.getcwd()

class WindowConstants:
    '''
    TODO(lyfer): Adding the WindowConstants class comment
    Attributes:
    '''
    WINDOW_WORK_PATH = WORK_PATH
    WINDOW_QSS_FILE_PATH = os.path.join(os.path.join(WORK_PATH, 'QSSTool'), 'windows.qss')
    WINDOW_ICON_PATH = os.path.join(os.path.join(os.path.join(WORK_PATH, 'resouce'), 'images'), 'my_icon.png')

    WINDOW_WELCOME_MESSAGE = 'Typing Exercise help you speed up! This is v0.1~'
    WINDOW_TITLE = 'Typing Exercise'

    # Window size is 1280 * 720 (this is fixed)
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720

