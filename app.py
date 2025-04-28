from flask import Flask, render_template, request
import duckdb
import os

app = Flask(__name__)

# Configuration
DB_PATH = r'C:\Daya\DuckDB\database\my_database.duckdb'

# Function to get list of tables
def get_tables():
    con = duckdb.connect(DB_PATH)
    tables = con.execute("SHOW TABLES").fetchall()
    con.close()
    return [table[0] for table in tables]

@app.route('/', methods=['GET', 'POST'])
def index():
    query_result = None
    error = None
    query = ""

    if request.method == 'POST':
        query = request.form.get('query')
        try:
            con = duckdb.connect(DB_PATH)
            query_result = con.execute(query).fetchall()
            columns = [desc[0] for desc in con.description]
            con.close()
        except Exception as e:
            error = str(e)
            query_result = None
            columns = []

        return render_template('index.html', 
                               db_path=DB_PATH, 
                               tables=get_tables(), 
                               query_result=query_result, 
                               columns=columns, 
                               error=error, 
                               query=query)

    return render_template('index.html', 
                           db_path=DB_PATH, 
                           tables=get_tables(), 
                           query_result=None, 
                           columns=[], 
                           error=None, 
                           query=query)

if __name__ == '__main__':
    app.run(debug=True)
