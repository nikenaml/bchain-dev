#app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
import pymysql
 
app = Flask(__name__)
app.secret_key = "Cairocoders-Ednalan"
  
mysql = MySQL(app)
   
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
 
    cur.execute("SELECT * FROM `orders`")
    data = cur.fetchall()

    cur.execute("SELECT DISTINCT nama_barang FROM `items` ORDER BY nama_barang ASC")
    itemList = cur.fetchall()

    cur.execute("SELECT DISTINCT jenis_bayar FROM `payment_type` ORDER BY jenis_bayar ASC")
    paymenttypeList = cur.fetchall()
  
    cur.close()
    return render_template('index.html', orders = data, itemList= itemList, paymenttypeList= paymenttypeList)
 
@app.route('/add_order', methods=['POST'])
def add_order():
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
        cur.execute("INSERT INTO `orders` (nama_pt, nama_pemesan, no_hp_pemesan, email_kantor, nama_barang, jumlah_barang, jenis_pembayaran, total_harga) VALUES (%s,%s,%s)", (nama_pt, nama_pemesan, no_hp_pemesan, email_kantor, nama_barang, jumlah_barang, jenis_pembayaran, total_harga))
        conn.commit()
        flash('Order Added successfully')
        return redirect(url_for('Index'))


@app.route("/add_order")
def input_jenis():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute("SELECT DISTINCT jenis_bayar FROM `payment_type` ORDER BY jenis_bayar ASC")
    paymenttypeList = cur.fetchall()
    cur.close()
    return render_template("index.html",paymenttypeList=paymenttypeList )

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_order(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('SELECT * FROM `orders` WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', order = data[0])
 
@app.route('/update/<id>', methods=['POST'])
def update_order(id):
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
            UPDATE `orders`
            SET nama_pt = %s,
                nama_pemesan = %s,
                no_hp_pemesan = %s,
                email_kantor = %s,
                nama_barang = %s,
                jumlah_barang = %s,
                jenis_pembayaran = %s
            WHERE id = %s
        """, (nama_pt, nama_pemesan, no_hp_pemesan, email_kantor, nama_barang, jumlah_barang, jenis_pembayaran, id))
        flash('Order Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))
 
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_order(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('DELETE `orders` WHERE id = {0}'.format(id))
    conn.commit()
    flash('Order Removed Successfully')
    return redirect(url_for('Index'))
 
# starting the app
if __name__ == "__main__":
    # app.run(port=3000, debug=True)
    app.run(debug=True)

