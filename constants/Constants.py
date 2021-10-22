import os

WORK_PATH = os.getcwd()
QSSTOOL_PATH = os.path.join(WORK_PATH, 'QSSTool')
ICON_PATH = os.path.join(os.path.join(WORK_PATH, 'resource'), 'images')

class WindowConstants:
    '''
    TODO(lyfer): Adding the WindowConstants class comment
    Attributes:
    '''
    WINDOW_WORK_PATH = WORK_PATH
    WINDOW_QSS_FILE_PATH = os.path.join(QSSTOOL_PATH, 'window.qss')
    WINDOW_ICON_PATH = os.path.join(ICON_PATH, 'keyboard.svg')

    WINDOW_WELCOME_MESSAGE = 'Typing Exercise help you speed up! This is v0.1~'
    WINDOW_TITLE = 'Typing Exercise'

    # Window size is 1280 * 720 (this is fixed)
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720

class MainPageConstants:
    MAINPAGE_QSS_FILE_PATH = os.path.join(QSSTOOL_PATH, 'mainpage.qss')
    MAINPAGE_WELCOME = 'Welcome typing exercise!'

class WordsExercisePageConstants:
    WORDS_EXERCISE_PAGE_QSS_FILE_PATH = os.path.join(QSSTOOL_PATH, 'words_exercise_page.qss')
    WORDS_EXERCISE_PAGE_QSS_FILE_START_ICON_PATH = os.path.join(ICON_PATH, 'start.svg')
    WORDS_EXERCISE_PAGE_QSS_FILE_PAUSE_ICON_PATH = os.path.join(ICON_PATH, 'pause.svg')


