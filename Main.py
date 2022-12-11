from flask import Flask,render_template,request,url_for,redirect,flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#MYSQL Connection
app.config['MYSQL_HOST'] = "127.0.0.1"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "guayara504"
app.config['MYSQL_DB'] = "flask_contacts"
mysql = MySQL(app)

#Settings
app.secret_key = "mysecretkey"

@app.route("/")
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("select * from contacts")
    data = cursor.fetchall()

    return render_template("index.html", contacts = data)

@app.route("/add_contact", methods = ["POST"])
def add_contact():
    if request.method == "POST":
        fullname = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]
        cursor = mysql.connection.cursor()
        cursor.execute("insert into contacts (fullname,phone,email) values (%s,%s,%s)",(fullname,phone,email))
        mysql.connection.commit()
        flash("Contact Added successfully")
        return redirect(url_for("index"))


@app.route("/edit/<id>")
def get_contact(id):
    cursor = mysql.connection.cursor()
    cursor.execute("select * from contacts where id = %s",[id])
    data = cursor.fetchall()
    return render_template("edit-contact.html", contact = data[0])

@app.route("/update/<id>", methods = ["post"])
def update_contact(id):
    if request.method == "POST":
        fullname = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]
    cursor = mysql.connection.cursor()
    cursor.execute("""
    update contacts
    set fullname = %s,
    email = %s,
    phone = %s
    where id = %s
    """,(fullname,phone,email,id) )
    mysql.connection.commit()
    flash("Contact updated successfully")
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def delete_Contact(id):
    cursor = mysql.connection.cursor()
    cursor.execute("delete from contacts where id = {0}".format(id))
    mysql.connection.commit()
    flash("Contact Removed successfully")
    return redirect(url_for("index"))
 

if __name__ == "__main__":
    app.run(debug=True)