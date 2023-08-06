import pymssql

class fnsql:

    def __init__(self, config):
        self.conn = None
        self.config = config
        self.get_sql_connection()
        return

    def get_sql_connection(self):
        if self.conn is None:
            self.conn = pymssql.connect(server=self.config['server'],
                                        user=self.config['user'],
                                        password=self.config['password'],
                                        database=self.config['database'],
                                        appname='Sharepoint List Sync/1.0',
                                        autocommit=self.config['autocommit'],
                                        as_dict=self.config['as_dict']
                                        )

    def truncate_stage(self):
        self.get_sql_connection()
        stmt = "TRUNCATE TABLE " + self.config['stageTable'] + ';'
        cursor = self.conn.cursor()
        cursor.execute(stmt)
        self.conn.commit()

    def insert_data(self, row):
        self.get_sql_connection()
        #mkvals = ','.join("?" * len(row))
        mkvals = "%(" + ")s,%(".join(row.keys()) + ")s"
        #cols = "'" + "','".join(row.keys()) + "'"
        cols = ",".join(row.keys())
        stmt = "INSERT INTO %s (%s) VALUES (%s)" % (self.config['stageTable'], cols, mkvals)

        cursor = self.conn.cursor()
        cursor.execute(stmt, row)
        self.conn.commit()

    def sync_tables(self):
        stmt = """
        
            DECLARE @SOURCE nvarchar(255) = '%s';
            DECLARE @TARGET nvarchar(255) = '%s';
            DECLARE @ON NVARCHAR(MAX) = 'TARGET.[Id] = SOURCE.[Id]';
            
            SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
            
            DECLARE @SOURCE_DB NVARCHAR(255) = (SELECT [value] FROM STRING_SPLIT(@SOURCE, '.') ORDER BY (SELECT 0) OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY);
            DECLARE @SOURCE_SH NVARCHAR(255) = (SELECT [value] FROM STRING_SPLIT(@SOURCE, '.') ORDER BY (SELECT 0) OFFSET 1 ROWS FETCH NEXT 1 ROWS ONLY);
            DECLARE @SOURCE_TB NVARCHAR(255) = (SELECT [value] FROM STRING_SPLIT(@SOURCE, '.') ORDER BY (SELECT 0) OFFSET 2 ROWS FETCH NEXT 1 ROWS ONLY);
            
            
            DECLARE @TARGET_DB NVARCHAR(255) = (SELECT [value] FROM STRING_SPLIT(@TARGET, '.') ORDER BY (SELECT 0) OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY);
            DECLARE @TARGET_SH NVARCHAR(255) = (SELECT [value] FROM STRING_SPLIT(@TARGET, '.') ORDER BY (SELECT 0) OFFSET 1 ROWS FETCH NEXT 1 ROWS ONLY);
            DECLARE @TARGET_TB NVARCHAR(255) = (SELECT [value] FROM STRING_SPLIT(@TARGET, '.') ORDER BY (SELECT 0) OFFSET 2 ROWS FETCH NEXT 1 ROWS ONLY);
            
            SET @SOURCE_DB = REPLACE(REPLACE(@SOURCE_DB, ']', ''), '[', '')
            SET @SOURCE_SH = REPLACE(REPLACE(@SOURCE_SH, ']', ''), '[', '')
            SET @SOURCE_TB = REPLACE(REPLACE(@SOURCE_TB, ']', ''), '[', '')
            SET @TARGET_DB = REPLACE(REPLACE(@TARGET_DB, ']', ''), '[', '')
            SET @TARGET_SH = REPLACE(REPLACE(@TARGET_SH, ']', ''), '[', '')
            SET @TARGET_TB = REPLACE(REPLACE(@TARGET_TB, ']', ''), '[', '')
            
            SELECT @SOURCE_DB, @SOURCE_SH, @SOURCE_TB
            DECLARE @COLS_SCHEMA	NVARCHAR(MAX)	= NULL;
            DECLARE @MERGE_SCHEMA	NVARCHAR(MAX)	= NULL;
            
            
            DECLARE @SQL_GET_COLS	NVARCHAR(MAX) = N'
                DECLARE @VAR NVARCHAR(MAX);
                SET @VAR = (
                    SELECT		'' ['' + TARGET.COLUMN_NAME + ''],'' [text()]
                    FROM		[' + @TARGET_DB + '].INFORMATION_SCHEMA.COLUMNS		AS TARGET
                    LEFT JOIN	[' + @SOURCE_DB + '].INFORMATION_SCHEMA.COLUMNS		AS SOURCE
                                ON TARGET.[COLUMN_NAME] = SOURCE.[COLUMN_NAME]
                    WHERE				TARGET.TABLE_CATALOG	= ''' + @TARGET_DB + '''
                                AND		TARGET.TABLE_SCHEMA		= ''' + @TARGET_SH + '''
                                AND		TARGET.TABLE_NAME		= ''' + @TARGET_TB + '''
                                AND		SOURCE.TABLE_CATALOG	= ''' + @SOURCE_DB + '''
                                AND		SOURCE.TABLE_SCHEMA		= ''' + @SOURCE_SH + '''
                                AND		SOURCE.TABLE_NAME		= ''' + @SOURCE_TB + '''
                    ORDER BY	TARGET.[ORDINAL_POSITION]    FOR XML PATH ('''')
            
                );
                SELECT @COLS_SCHEMA = @VAR
            ';
            EXEC sp_executesql @SQL_GET_COLS, N'@COLS_SCHEMA NVARCHAR(MAX) OUTPUT', @COLS_SCHEMA OUTPUT;
            SET @COLS_SCHEMA = LEFT(@COLS_SCHEMA, LEN(@COLS_SCHEMA)-1);
            
            
                    
            DECLARE @SQL_GET_MERGE	NVARCHAR(MAX) = N'
                DECLARE @VAR NVARCHAR(MAX);
                SET @VAR = (
                    SELECT		'' TARGET.['' + TARGET.COLUMN_NAME + ''] = SOURCE.['' + TARGET.COLUMN_NAME + ''],'' [text()]
                    FROM		[' + @TARGET_DB + '].INFORMATION_SCHEMA.COLUMNS		AS TARGET
                    LEFT JOIN	[' + @SOURCE_DB + '].INFORMATION_SCHEMA.COLUMNS		AS SOURCE
                                ON TARGET.[COLUMN_NAME] = SOURCE.[COLUMN_NAME]
                    WHERE				TARGET.TABLE_CATALOG	= ''' + @TARGET_DB + '''
                                AND		TARGET.TABLE_SCHEMA		= ''' + @TARGET_SH + '''
                                AND		TARGET.TABLE_NAME		= ''' + @TARGET_TB + '''
                                AND		SOURCE.TABLE_CATALOG	= ''' + @SOURCE_DB + '''
                                AND		SOURCE.TABLE_SCHEMA		= ''' + @SOURCE_SH + '''
                                AND		SOURCE.TABLE_NAME		= ''' + @SOURCE_TB + '''
                    ORDER BY	TARGET.[ORDINAL_POSITION]    FOR XML PATH ('''')
                );
                SELECT @MERGE_SCHEMA = @VAR
            ';
            EXEC sp_executesql @SQL_GET_MERGE, N'@MERGE_SCHEMA NVARCHAR(MAX) OUTPUT', @MERGE_SCHEMA OUTPUT;
            SET @MERGE_SCHEMA = LEFT(@MERGE_SCHEMA, LEN(@MERGE_SCHEMA)-1);
            
            DECLARE @SQL_QUERY NVARCHAR(MAX) = '
                    MERGE		' + @TARGET + ' AS TARGET
                    USING		' + @SOURCE + ' AS SOURCE
                    ON			' + @ON + '
                    WHEN NOT MATCHED BY TARGET THEN INSERT (' + @COLS_SCHEMA + ') VALUES (' + @COLS_SCHEMA + ')
                    WHEN MATCHED THEN UPDATE SET ' + @MERGE_SCHEMA +  ';
            ';
            
            EXEC sp_executesql @SQL_QUERY;
            
            SET @SQL_QUERY = 'TRUNCATE TABLE ' + @SOURCE;
            EXEC sp_executesql @SQL_QUERY;


        
        """ % (self.config['stageTable'], self.config['targetTable'])
        cursor = self.conn.cursor()
        cursor.execute(stmt)
        self.conn.commit()

