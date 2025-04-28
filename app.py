from flask import Flask, render_template, request
import duckdb
import os

app = Flask(__name__)

# Configuration
# Update DB path for Render
DB_PATH = os.getenv('DB_PATH', 'my_database.duckdb')  
# On local machine, you can set DB_PATH as environment variable if needed.

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
    columns = []

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

# Only needed for local testing
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
