class QSSTool:
    @staticmethod
    def qss(widget, file_path = None, file_path_list = None):
        '''
        To process widget qss
        :param widget: your widget
        :param file_path: file path
        :param file_path_list: your file
        :return: None
        '''

        if file_path is not None:
            try:
                with open(str(file_path), "r", encoding='utf-8') as qss:
                    widget.setStyleSheet(qss.read())
            except:
                print(file_path, 'This qss file not found!')

        elif file_path_list is not None:
            for path in file_path_list:
                try:
                    with open(str(path), "r", encoding='utf-8') as qss:
                        widget.setStyleSheet(qss.read())
                except:
                    print(path, 'This qss file not found!')

        else:
            print("You don't typing correct file name or file is not exist!")