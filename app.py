from flask import Flask , render_template , request , redirect
import sqlite3

app = Flask(__name__)


# connect db
def get_db():
    conn = sqlite3.connect("library_system.db")
    # conn.row_factory allows for column names to be used when connecting to db rather than index number
    conn.row_factory = sqlite3.Row
    return conn

# read
@app.route('/')
def index():
    db = get_db()
    # use aliasing to clean up ui
    query = "SELECT account_id AS account_id , email AS email , password_hash AS password_hash FROM Account"
    account = db.execute(query).fetchall()
    db.close()
    return render_template("index.html" , account=account)

# update
@app.route("/library_add" , methods = ["GET" , "POST"])
def add_book():
    if request.method == 'POST':
        t , a = request.form['email'] , request.form['password_hash']
        db = get_db()
        db.execute("INSERT INTO Account (email , password_hash) VALUES (? , ?)" , (t , a))
        db.commit()
        db.close()
        return redirect("/")
    return render_template('library_add.html')

@app.route('/my_loan')
def my_loan():
    db = get_db()
    # use aliasing again to clean up ui
    query = "SELECT title AS title , content_type AS content_type , release_year AS release_year, content_link AS content_link , content_id AS content_id FROM Content"
    content = db.execute(query).fetchall()
    db.close()
    return render_template("my_loan.html" , content = content)

# delete
@app.route('/delete/<int:id>')
def delete_book(id):
    db = get_db
    db.execute("DELETE FROM Account WHERE account_id = ?" , (id,))
    db.commit()
    db.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)