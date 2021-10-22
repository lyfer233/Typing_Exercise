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
            with conn.cursor() as cur:
                # query word
                sql = r'SELECT * FROM word ORDER BY RAND() LIMIT 20'

                cur.execute(sql)
                data = cur.fetchall()
        except:
            conn.rollback()

        return data
