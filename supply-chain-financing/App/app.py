### CORE IMPORT
from datetime import datetime

from ellipticcurve.privateKey import PrivateKey, PublicKey
from ellipticcurve.utils.file import File
from ellipticcurve.ecdsa import Ecdsa
from ellipticcurve.signature import Signature
import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from logging.config import dictConfig
from urllib.parse import urlparse
from sqlalchemy import text
from flask_migrate import Migrate
# from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from flask_marshmallow import Marshmallow
from sqlalchemy.ext.declarative import DeclarativeMeta
# Base = declarative_base()

### IMPORT FOR PYMYSQL
from flask_sqlalchemy import SQLAlchemy
import json
import uuid
import requests

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask("scf")
app.secret_key = "Scf-Platform"
# mysql = MySQL(app)

db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
app.session_type = "filesystem"

# path to upload files
# UPLOAD_FOLDER = "UPLOAD_FOLDER/"
UPLOAD_FOLDER = "static/uploads/"

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
# mysql.init_app(app)

class Enterprise(db.Model):
    # __tablename__ = "enterprises"
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(100), nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    established_since = db.Column(db.Integer,nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phonenumber = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    # order = db.relationship('Order', backref='enterprise')
    orders = db.relationship('Order', backref='enterprise')
    def __repr__(self):
        return f'<Enterprise {self.company_name}>'

class Item(db.Model):
    # __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100),nullable=False)
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    supplier_id = db.Column(db.Integer,db.ForeignKey('supplier.id'))
    order = db.relationship('Order', backref='item')
    def __repr__(self):
        return f'<Item {self.name}>'

# class ItemSchema(ma.SQLAlchemyAutoSchema):
#     class Meta:
#         model = Item
#         include_fk = True

class Supplier(db.Model):
    # __tablename__ = "suppliers"
    id = db.Column(db.Integer, primary_key=True)
    no_izin_usaha = db.Column(db.Integer, unique=True)
    no_ktp_pemilik = db.Column(db.Integer, unique=True)
    no_npwp_pemilik = db.Column(db.Integer, unique=True)
    company_name = db.Column(db.String(100), nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    established_since = db.Column(db.Integer,nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phonenumber = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    item = db.relationship('Item', backref='supplier')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    order = db.relationship('Order', backref='supplier')
    def __repr__(self):
        return f'<Supplier {self.company_name}>'  

class PaymentType(db.Model):
    # __tablename__ = "payment_types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    discount = db.Column(db.Float)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    order = db.relationship('Order', backref='payment_type')
    def __repr__(self):
        return f'<PaymentType {self.name}>'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enterprise_id = db.Column(db.Integer,db.ForeignKey('enterprise.id'))
    item_id = db.Column(db.Integer,db.ForeignKey('item.id'))
    supplier_id = db.Column(db.Integer,db.ForeignKey('supplier.id'))
    item_count = db.Column(db.Integer)
    payment_type_id = db.Column(db.Integer,db.ForeignKey('payment_type.id'))
    sign_supplier = db.Column(db.String(100))
    sign_enterprise = db.Column(db.String(100))
    upload_voucher = db.Column(db.String(100))
    total_discount = db.Column(db.Integer)
    total_price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    def __repr__(self):
        return f'<Order enterprise_id={self.enterprise_id}=> supplier_id={self.supplier_id} >'

class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)

#Loan
#order_id
# signature_financier 
# dokumen
# 

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_fk = True

@app.route('/enterprise',methods=['GET'])
def enterprise_index():
    # ---------------Create and Run Init SQL SCRIPT---------
    # db.create_all()
    # with open("./scf.sql") as file:
    #     queries = file.read().split(";")
    #     for q in queries:
    #         query = text(q)
    #         db.engine.execute(query)
    #--------------------------------------------------------
    url = urlparse(request.referrer)
    if url.path == '/supplier' or url.path == '/profile-supplier':
        return render_template("common/failed.html", user='supplier')
    
    orders = Order.query.filter_by(enterprise_id=1).all()
    payment_types = PaymentType.query.all()
    suppliers = Supplier.query.all()
    items = Item.query.all()
    return render_template('enterprise/index.html',
        orders = orders,
        items = items,
        payment_types = payment_types,
        suppliers = suppliers
    )
 
@app.route('/api/order', methods=['POST'])  # type: ignore
def add_order():
    if request.method == 'POST':
        data = request.get_json()

        # Get Enterprise Name
        enterprise_id = int(data.get('enterprise_id'))
        enterprise = Enterprise.query.filter_by(id=enterprise_id).first().owner_name
        
        # Commit data to get primary key
        order = Order(**data)
        db.session.add(order)
        db.session.commit()
        order_schema = OrderSchema()

        order_serializer = order_schema.dump(order)
        order_serializer['action'] = "create_order"
        #Digital Enterprise Sign
        enterprise_private_file = File.read(f"./key/private/{enterprise}.pem")
        enterprise_privatekey = PrivateKey.fromPem(enterprise_private_file)
        signature = Ecdsa.sign(json.dumps(order_serializer),enterprise_privatekey).toBase64()
        order.sign_enterprise = signature

        ## Send to Blockchain Service
        # res= requests.post("http://localhost:5001/transaction/broadcast",json=order_serializer)
        # if res.status_code== 200:
            # requests.get("http://localhost:5001/mine")
        # Save with digital signature
        db.session.add(order)
        db.session.commit()
        # flash('Order sukses ditambahkan')
        return make_response(jsonify({"order": data, "message": "Order sukses ditambahkan"}), 200)


@app.route('/api/order/<id>', methods = ['GET'])
def get_order(id):
    # data = db.session.query(Order.id, Order.created_at)\
    #                 .join(Enterprise, Order.enterprise_id == Enterprise.id)\
    #                 .join(Item, Order.item_id == Item.id)\
    #                 .join(PaymentType, Order.payment_type_id == PaymentType.id)\
    #                 .filter_by(id=id).first()
    o = Order.query.filter_by(id=id).first()
    order = {
        "id": o.id,
        "nama_pt_enterprise": o.enterprise.company_name,
        "nama_pemesan": o.enterprise.owner_name,
        "no_hp_pemesan": o.enterprise.phonenumber,
        "nama_barang": o.item.name,
        "jumlah_barang": o.item_count,
        "jenis_bayar": o.payment_type.name,
        "total_diskon": o.total_discount,
        "total_harga": o.total_price,
        "sign_enterprise": o.sign_enterprise,
        "sign_supplier": o.sign_supplier,
        "voucher": o.upload_voucher,
        "created_at": o.created_at,
    }
    # app.logger.info('order => %s', order)
    # app.logger.info('enterprise => %s', enterprise)
    # return make_response(json.dumps(order, cls=AlchemyEncoder))
    # return make_response(data, 200)
    return make_response(jsonify(order), 200)
    # return render_template('edit.html', order = data[0])

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


@app.route('/supplier')
def main_menu_supplier():
    url = urlparse(request.referrer)
    if url.path == '/enterprise':
        return render_template("common/failed.html", user='enterprise')
    data = Order.query.filter_by(supplier_id=1).all()
    return render_template('supplier/manage_orders.html', 
        manage_orders = data
    )

@app.route('/supplier/order/<id>',methods=['GET'])
def confirm_order_from_supplier(id):
    order_schema = OrderSchema()
    order = Order.query.filter_by(id=id).first()
    #Digital Enterprise Sign
    supplier_private_file = File.read(f"./key/private/{order.supplier.owner_name}.pem")
    supplier_privatekey = PrivateKey.fromPem(supplier_private_file)

    order_serializer = order_schema.dump(order)
    order_serializer['action'] = "sign_by_supplier"
    signature = Ecdsa.sign(json.dumps(order_serializer),supplier_privatekey).toBase64()
    
    # Add Digital Signature
    order.sign_supplier = signature
    db.session.add(order)
    db.session.commit()

    # Send to BC
    res= requests.post("http://localhost:5001/transaction/broadcast",json=order_serializer)
    if res.status_code== 200:
        # Mine to block
        requests.get("http://localhost:5001/mine")
        data = Order.query.filter_by(supplier_id=1).all()
        return render_template('supplier/manage_orders.html', 
            manage_orders = data
        )

@app.route('/profile-supplier')
def view_supplier_profile():
    url = urlparse(request.referrer)
    if url.path == '/enterprise':
        return render_template("common/failed.html", user='enterprise')
    
    suppliers = Supplier.query.all()
    return render_template('supplier/profile.html',
        profile = suppliers
    )

    
@app.route('/enterprise/order/<id>',methods=['POST'])
def upload_voucher(id):
    order = Order.query.filter_by(id=id).first()
    file = request.files['file']
    # Check file is valid and save it
    if file.filename.endswith('jpg') or file.filename.endswith('png') or file.filename.endswith('pdf'):
        ID = uuid.uuid4().hex
        folder = UPLOAD_FOLDER + ID
        current_time = str(datetime.now()).replace('-', '_').replace(':', '_')
        if not os.path.exists(folder):
            os.mkdir(folder)
        filename  = folder + '/' + current_time + "." + file.filename.split(".")[-1]
        file.save(filename)
        order.upload_voucher = filename
        db.session.add(order)
        db.session.commit()
        return redirect(url_for('enterprise_index'))
        
    else:
        raise("Erorr")


        



if __name__ == '__main__':
    app.run(debug=True)
    