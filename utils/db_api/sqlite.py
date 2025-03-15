import sqlite3


class Database:
    def __init__(self, path_to_db="data/main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self,chat_id: int, first_name: str,username: str ,date: str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO users(chat_id,first_name ,username, date) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(chat_id,first_name,username,date), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM users;", fetchone=True)

    def update_user_lang(self, lang, chat_id):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE users SET lang=? WHERE chat_id=?
        """
        return self.execute(sql, parameters=(lang, chat_id), commit=True)


    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

# _________________________________________________________________



    def add_example(self,template_img: str, result_img: str,deskription: str, name:str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO example(template_img,result_img ,deskription, name) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(template_img,result_img,deskription,name), commit=True)


    def select_all_example(self):
        sql = """
        SELECT * FROM example
        """
        return self.execute(sql, fetchall=True)


    def delete_example(self, name: str):
        sql = """
        DELETE FROM example WHERE name = ?
        """
        self.execute(sql, parameters=(name,), commit=True)


    # def get_result_img(self, name: str):
    #     sql = """
    #     SELECT result_img FROM example WHERE name = ?
    #     """
    #     result = self.execute(sql, parameters=(name,), fetchone=True)
    #     return result[0] if result else None


# _________________________________________________________________



    def add_templatetest(self,test_img: str,  name:str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO template_test(test_img, name) VALUES(?, ?)
        """
        self.execute(sql, parameters=(test_img,name), commit=True)



    def select_all_templatetest(self):
        sql = """
        SELECT * FROM template_test
        """
        return self.execute(sql, fetchall=True)
    

    def delete_templatetest(self, name: str):
        sql = """
        DELETE FROM template_test WHERE name = ?
        """
        self.execute(sql, parameters=(name,), commit=True)
    



# _________________________________________________________________


    def add_company(self,user: str, user_id: int,loyiha: str ,holat: str, muddat: str, shablonimg: str, resultimg: str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO company(user ,user_id ,loyiha, holat, muddat, shablonimg, resultimg) VALUES(?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(user ,user_id ,loyiha, holat, muddat, shablonimg, resultimg), commit=True)


    def select_all_company(self):
        sql = """
        SELECT * FROM company
        """
        return self.execute(sql, fetchall=True)


    def select_company(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM company WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)


    def delete_company(self, loyiha: str):
        sql = """
        DELETE FROM company WHERE loyiha = ?
        """
        self.execute(sql, parameters=(loyiha,), commit=True)


    def update_company_holat(self, holat, loyiha):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE company SET holat=? WHERE loyiha=?
        """
        return self.execute(sql, parameters=(holat, loyiha), commit=True)
    

    def update_company_muddat(self, muddat, loyiha):
        # SQL_EXAMPLE = "UPDATE Users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE company SET muddat=? WHERE loyiha=?
        """
        return self.execute(sql, parameters=(muddat, loyiha), commit=True)
    

    def is_user_exists(self, user_id: int) -> bool:
        sql = "SELECT EXISTS(SELECT 1 FROM company WHERE user_id = ?)"
        result = self.execute(sql, parameters=(user_id,), fetchone=True)
        return bool(result[0]) if result else False



# _________________________________________________________________


    def add_result(self,user_id: int,user: str ,resultimg: str, date: str):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
        INSERT INTO result(user_id ,user, resultimg, date) VALUES(?, ?, ?, ?)
        """
        self.execute(sql, parameters=(user_id ,user, resultimg, date), commit=True)


    def select_all_result(self):
        sql = """
        SELECT * FROM result
        """
        return self.execute(sql, fetchall=True)
    

    def select_result(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM result WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        result = self.execute(sql, parameters=parameters, fetchone=True)
        return result[3] if result else None



    
    def get_company_results(self, company_name: str):
        sql = """
        SELECT r.id, r.resultimg 
        FROM result r
        JOIN company c ON c.user_id = r.user_id
        WHERE c.loyiha = ?
        """
        return self.execute(sql, parameters=(company_name,), fetchall=True)








def logger(statement):
    pass
#     print(f"""
# _____________________________________________________
# Executing:
# {statement}
# _____________________________________________________
# """)