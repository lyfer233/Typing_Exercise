import os

WORK_PATH = os.getcwd()
QSSTOOL_PATH = os.path.join(WORK_PATH, 'QSSTool')
ICON_PATH = os.path.join(os.path.join(WORK_PATH, 'resource'), 'images')
DATABASE_PATH = os.path.join(os.path.join(WORK_PATH, 'resource'), 'database')

class WindowConstants:
    """
    TODO(lyfer): Adding the WindowConstants class comment
    Attributes:
    """
    WINDOW_WORK_PATH = WORK_PATH
    WINDOW_QSS_FILE_PATH = os.path.join(QSSTOOL_PATH, 'window.qss')
    WINDOW_ICON_PATH = os.path.join(ICON_PATH, 'keyboard.svg')
    WORDLIST_PATH = os.path.join(DATABASE_PATH, 'wordlist.db')

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


class WordsTableConstants:
    TABLE_QSS_FILE_PATH = os.path.join(QSSTOOL_PATH, 'wordstable.qss')

    TABLE_DATA_SHOW_COUNT = 10  # it show data on the per page.
    TABLE_DEFAULT_ROW = 10
    TABLE_DEFAULT_COLUMN = 3

    TABLE_HEADER_LIST = ['Word', 'translation', 'operate']

    TABLE_HEADER_HEIGHT = 56
    TABLE_ROW_HEIGHT = 60


class SearchConstants:
    UPDATE_OK_MESSAGE = 'Translation has updated successful!'
    UPDATE_NO_MESSAGE = 'Translation has updated failed'
    DELETE_OK_MESSAGE = 'Delete successful!'
    DELETE_NO_MESSAGE = 'Delete Failed'
    COPY_OK_MESSAGE = "Copied to clipboard!"
    COPY_NO_MESSAGE = 'Copied failed'
