class GetWord:
    """
    from database get word
    """
    @staticmethod
    def from_db(conn, page = 1):
        """
        :param conn: connect database object
        :param page: number of page, eight per page
        :return:
        """
        data = ()
        # error judge
        if isinstance(page, str):
            page = int(page)
        if not(isinstance(page, int)):
            return data

        try:
            cur = conn.cursor()
            sql = 'SELECT word, translation FROM word WHERE is_delete=0 AND ROWID>{} LIMIT 12'.format((page - 1) * 8)
            cur.execute(sql)
            data = tuple(cur.fetchall())

        except:
            conn.rollback()

        return data

    @staticmethod
    def all_count(conn):

        count = 0
        try:
            cur = conn.cursor()
            sql = 'select COUNT(*) FROM word WHERE is_delete=0'
            cur.execute(sql)
            count = cur.fetchone()[0]

        except:
            conn.rollback()

        return count

class UpdateMean:
    """
    update translation of the word
    """

    @staticmethod
    def update(conn, means, word):
        """
        :param conn: connect database object
        :param means: translation result
        :param word: word
        :return: int status
        """
        status = 0
        try:
            with conn.cursor() as cur:
                sql = 'UPDATE word SET translation={} where word={}'.format(means, word)
                status = cur.execute(sql)

            conn.commit()
        except:
            conn.rollback()

        return status

class DeleteWord:

    @staticmethod
    def delete(conn, word):
        status = 0

        try:
            with conn.cursor() as cur:
                sql = 'UPDATE word set is_delete=1 WHERE word={}'.format(word)
                status = cur.execute(sql)

            conn.commit()
        except:
            conn.rollback()

        return status

class QueryWord:
    """
    take the need word from db
    """

    @staticmethod
    def from_db(conn, number=0):
        '''

        :param conn: will connect database object
        :param number: will recite words
        :return:
        '''

        data = ()
        try:
            cur = conn.cursor()
            sql = 'SELECT word, translation FROM word WHERE is_delete=0 ORDER BY RANDOM() LIMIT 20'
            cur.execute(sql)
            data = cur.fetchall()
        except:
            conn.rollback()

        return data
