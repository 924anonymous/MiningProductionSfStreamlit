import snowflake.connector as snow


class GetDataFromSnowflake:
    def __init__(self, **kwargs):
        self.creds = kwargs
        self.conn = snow.connect(**self.creds)

    def execute_query(self, query):
        """
        This Function Can Fetch Data From Snowflake And Return Pandas DataFrame Of That Data.

        :return: Pandas DataFrame
        """
        cur = self.conn.cursor()
        cur.execute(query)
        df = cur.fetch_pandas_all()
        return df
