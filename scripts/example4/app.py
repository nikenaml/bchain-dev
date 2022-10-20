#app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import pymysql
 
app = Flask(__name__)
# app.secret_key = "Cairocoders-Ednalan"
  
mysql = MySQL()
   
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'scf'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
 
@app.route('/')
def Index():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
 
    cur.execute('SELECT * FROM order')
    data = cur.fetchall()
  
    cur.close()
    return render_template('index.html', employee = data)
 
@app.route('/add_barang', methods=['POST'])
def add_employee():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        nama_pt = request.form['nama_pt']
        nama_pemesan = request.form['nama_pemesan']
        no_hp_pemesan = request.form['no_hp_pemesan']
        email_kantor = request.form['email_kantor']
        nama_barang = request.form['nama_barang']
        jumlah_barang = request.form['jumlah_barang']
        jenis_pembayaran = request.form['jenis_pembayaran']
        total_harga = request.form['total_harga']
        cur.execute("INSERT INTO order (nama_pt, nama_pemesan, no_hp_pemesan, email_kantor, nama_barang, jumlah_barang, jenis_pembayaran, total_harga) VALUES (%s,%s,%s)", (nama_pt, nama_pemesan, no_hp_pemesan, email_kantor, nama_barang, jumlah_barang, jenis_pembayaran, total_harga))
        conn.commit()
        flash('Order Added successfully')
        return redirect(url_for('Index'))
 
@app.route("/add_barang)
def input():
    cityList=db.execute("SELECT * FROM item order by nama_barang")
    return render_template("index.html",cityList=cityList )

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_barang(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('SELECT * FROM order WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', employee = data[0])
 
@app.route('/update/<id>', methods=['POST'])
def update_barang(id):
    if request.method == 'POST':
        nama_pt = request.form['nama_pt']
        nama_pemesan = request.form['nama_pemesan']
        no_hp_pemesan = request.form['no_hp_pemesan']
        email_kantor = request.form['email_kantor']
        nama_barang = request.form['nama_barang']
        jumlah_barang = request.form['jumlah_barang']
        jenis_pembayaran = request.form['jenis_pembayaran']
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            UPDATE order
            SET nama_pt = %s,
                nama_pemesan = %s,
                no_hp_pemesan = %s,
                email_kantor = %s,
                nama_barang = %s,
                jumlah_barang = %s,
                jenis_pembayaran = %s
            WHERE id = %s
        """, (nama_pt, nama_pemesan, no_hp_pemesan, email_kantor, nama_barang, jumlah_barang, jenis_pembayaran, total_harga, id))
        flash('Order Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))
 
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_employee(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('DELETE order WHERE id = {0}'.format(id))
    conn.commit()
    flash('Order Removed Successfully')
    return redirect(url_for('Index'))
 
# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
