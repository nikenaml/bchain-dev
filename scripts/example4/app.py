### CORE IMPORT
from dataclasses import fields
from datetime import datetime
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
### IMPORT FOR PYMYSQL
from flaskext.mysql import MySQL
import pymysql

### IMPORT FOR BLOCKCHAIN
# from ellipticcurve.privateKey import PrivateKey, PublicKey
# from ellipticcurve.utils.file import File
# from ellipticcurve.ecdsa import Ecdsa
# from ellipticcurve.signature import Signature
# import argparse

app = Flask("scf")
app.secret_key = "Scf-Platform"

mysql = MySQL(app)

### CONFIG FOR PYMYSQL
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'scf'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)


# bc = Blockchain(args.port))
# @app.route('/user/<user>', methods=['GET'])
# def index(user):
#     return render_template("user/index.html",user=user)

# @app.route("/supplier/confirmation",methods=['GET',"POST"])
# def confirmation():
#     if request.method=='POST':
            
#         supplier_private_file = File.read("./key/supplier_private.pem")
#         supplier_privatekey = PrivateKey.fromPem(supplier_private_file)
        
#         supplier_public_file = File.read("./key/supplier_public.pem")
#         supplier_publickey = PublicKey.fromPem(supplier_public_file)
        
#         # sign_file = File.read("./key/signature.txt")
#         # signature = Signature.fromBase64(sign_file)

#         with open("./signature/test2.txt","w+") as f:
#             f.write(Ecdsa.sign("test",supplier_privatekey).toBase64())
        
#         # print(Ecdsa.verify("test", signature, core_publickey))
#         return render_template("common/success.html",user="supplier")
#     return render_template('supplier/confirm_invoice.html',user="supplier")

# @app.route('/user/<user>/register',methods=['GET',"POST"])  # type: ignore
# def register(user):
#     if user == "supplier":
#         return render_template("register.html",type='offline',user="supplier")
#     elif user == "core":
#         if request.method=='POST':
            
#             core_private_file = File.read("./key/core_private.pem")
#             core_privatekey = PrivateKey.fromPem(core_private_file)
            
#             core_public_file = File.read("./key/core_public.pem")
#             core_publickey = PublicKey.fromPem(core_public_file)
            
#             # sign_file = File.read("./key/signature.txt")
#             # signature = Signature.fromBase64(sign_file)

#             with open("./signature/test.txt","w+") as f:
#                 f.write(Ecdsa.sign("test",core_privatekey).toBase64())
            
#             # print(Ecdsa.verify("test", signature, core_publickey))
#             return render_template("common/success.html",user="core")
#         return render_template("user/order.html",user="core")
#     # else:
#         # return render_template("register.html",type='offline')

@app.route('/check_discount', methods=['POST'])
def add_extra_disc():
    if request.method == 'POST':
        data = request.get_json()
        sourceBanding = data.sourceBanding
        valueBanding = data.valueBanding
        totalHarga =data.totalHarga

        total = 0
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)
        cur.execute('''SELECT extra_disc.* FROM extra_disc''')
        extraDiscList = cur.fetchall()
        for ed in extraDiscList:
            if (ed.condition_banding == '=>'):
                if (sourceBanding == ed.source_banding):
                    if  (valueBanding == ed.value_banding) & (valueBanding > ed.value_banding) :
                        total = totalHarga - (totalHarga * ed.disc)
                    else:
                        pass
            elif (ed.condition_banding == '='):
                if (sourceBanding == ed.source_banding):
                    if (valueBanding == ed.value_banding) :
                        total = totalHarga - (totalHarga * ed.disc)
                    else:
                        pass
            elif (ed.condition_banding == '>'):
                if (sourceBanding == ed.source_banding):
                    if (valueBanding > ed.value_banding):
                        total = totalHarga - (totalHarga * ed.disc)
                    else:
                        pass
        total_ed = total
    return make_response(jsonify({"extra_discount": total_ed}), 200)
                

@app.route('/')
def index_user():
    return render_template("auth/select_account.html")


@app.route('/<user>')
def Index(user):
    if (user != "enterprise"):
        return render_template("common/failed.html", user=user)
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)  # type: ignore
 
    cur.execute('''SELECT orders.*, enterprises.nama_pt_enterprise FROM orders 
    LEFT JOIN enterprises on orders.id_enterprise = enterprises.id''')
    data = cur.fetchall()

    cur.execute('''SELECT DISTINCT jenis_bayar, discount, id FROM payment_types ORDER BY jenis_bayar ASC''')
    paymentTypeList = cur.fetchall()

    cur.execute('''SELECT DISTINCT nama_barang, harga_barang, id FROM items ORDER BY nama_barang ASC''')
    itemList = cur.fetchall()

    cur.execute('''SELECT DISTINCT nama_pt_enterprise, id FROM enterprises ORDER BY nama_pt_enterprise ASC''')
    nameSupplierList = cur.fetchall()

    cur.close()
    return render_template('enterprise/index.html',
        orders = data,
        itemList = itemList,
        paymentTypeList = paymentTypeList,
        nameSupplierList = nameSupplierList,
        user = user
    )
 
@app.route('/api/order', methods=['POST'])  # type: ignore
def add_order():
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        data = request.get_json()
        idEnterprise = int(data.get('idEnterprise')),
        namaPemesan = data.get('namaPemesan')
        noHpPemesan = data.get('noHpPemesan')
        idBarang = int(data.get('idBarang'))
        idJenisPembayaran = int(data.get('idJenisPembayaran'))
        jumlahBarang = int(data.get('jumlahBarang'))
        totalHarga = int(data.get('totalHarga'))
        # query_string = "SELECT harga_barang FROM items WHERE id = %s"
        # cur.execute(query_string, (idBarang))
        # barang = cur.fetchall()

        # extraDiscItemTertentu = add_extra_disc('items.id', idBarang, totalHarga)
        # extraDiscJumlahBarang = add_extra_disc('orders.jumlah_barang', jumlahBarang, totalHarga)
        # extraDiscHargaBarang = add_extra_disc('items.harga_barang', barang.harga_barang, totalHarga)
        # totalExtraDiscSementara = extraDiscItemTertentu + extraDiscJumlahBarang + extraDiscHargaBarang
        # totalHarga = totalHarga - totalExtraDiscSementara

        cur.execute('''INSERT INTO orders (id_enterprise, nama_pemesan, no_hp_pemesan, id_item, jumlah_barang, id_payment_type, total_harga) VALUES (%s,%s,%s,%s,%s,%s,%s)''', (idEnterprise, namaPemesan, noHpPemesan, idBarang, jumlahBarang, idJenisPembayaran, totalHarga))
        conn.commit()
        cur.close()
        return make_response(jsonify({"order": data}), 200)
        # flash('Order sukses ditambahkan')
        # return redirect(url_for('/enterprise'))

# def getPembanding(pembanding):
#     if (pembanding == '>'):
#         # TODO
    

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_order(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('SELECT * FROM `orders` WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', order = data[0])
 
@app.route('/update/<id>', methods=['POST'])  # type: ignore
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
        return redirect(url_for('index'))
 
@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_order(id):
    conn = mysql.connect()
    cur = conn.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('DELETE `orders` WHERE id = {0}'.format(id))
    conn.commit()
    flash('Order Removed Successfully')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
    