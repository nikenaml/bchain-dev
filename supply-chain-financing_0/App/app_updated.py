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
from marshmallow import fields
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
UPLOAD_FOLDER = "UPLOAD_FOLDER"
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__),'static',UPLOAD_FOLDER)
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
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    order = db.relationship('Order', backref='enterprise',lazy=True,cascade=None)
    def __repr__(self):
        return f'<Enterprise {self.company_name}>'

class Item(db.Model):
    # __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100),nullable=False)
    price = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    supplier_id = db.Column(db.Integer,db.ForeignKey('supplier.id'))
    order = db.relationship('Order', backref='item',lazy=True,cascade=None)
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
    item = db.relationship('Item', backref='supplier',lazy=True,cascade=None)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    order = db.relationship('Order', backref='supplier',lazy=True,cascade=None)
    def __repr__(self):
        return f'<Supplier {self.company_name}>'  

class PaymentType(db.Model):
    # __tablename__ = "payment_types"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    discount = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    order = db.relationship('Order', backref='payment_type',lazy=True,cascade=None)
    def __repr__(self):
        return f'<PaymentType {self.name}>'

class ApplyLoan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sell_report_path = db.Column(db.String(100))
    finance_report_path = db.Column(db.String(100))
    account_statement_path = db.Column(db.String(100))
    sign_finance = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    order = db.relationship('Order', uselist=False,backref='apply_loan')
    def __repr__(self):
        return f'<ApplyLoan order_id={self.order_id} >'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enterprise_id = db.Column(db.Integer,db.ForeignKey('enterprise.id'))
    item_id = db.Column(db.Integer,db.ForeignKey('item.id'))
    supplier_id = db.Column(db.Integer,db.ForeignKey('supplier.id'))
    applyloan_id = db.Column(db.Integer,db.ForeignKey('apply_loan.id'))
    item_count = db.Column(db.Integer)
    payment_type_id = db.Column(db.Integer,db.ForeignKey('payment_type.id'))
    sign_supplier = db.Column(db.String(100))
    sign_enterprise = db.Column(db.String(100))
    upload_voucher = db.Column(db.String(100))
    total_discount = db.Column(db.Integer)
    total_price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
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
    created_at = fields.DateTime(format='%Y-%m-%dT%H:%M:%S')
    updated_at = fields.DateTime(format='%Y-%m-%dT%H:%M:%S')
    class Meta:
        model = Order
        include_fk = True

def get_orders(by,value):
    res = requests.get("http://localhost:5001/blockchain")
    orders = res.json()['chain'][1:][::-1]
    orders_bc = []
    temp_id = []
    for order in orders:
        if order['transactions'][0]['data'][-1][by] == value and order['transactions'][0]['id'] not in temp_id:
            del order['transactions'][0]['data'][-1]['action']
            # del order['transactions']['data'][-1]['created_at']
            # del order['transactions']['data'][-1]['updated_at']
            order['transactions'][0]['data'][-1]['updated_at'] = datetime.strptime(order['transactions'][0]['data'][-1]['updated_at'],'%Y-%m-%dT%H:%M:%S')
            order['transactions'][0]['data'][-1]['created_at'] = datetime.strptime(order['transactions'][0]['data'][-1]['created_at'],'%Y-%m-%dT%H:%M:%S')
            s= Supplier.query.filter_by(id=order['transactions'][0]['data'][-1]['supplier_id']).first()
            e= Enterprise.query.filter_by(id= order['transactions'][0]['data'][-1]['enterprise_id']).first()
            i = Item.query.filter_by(id=order['transactions'][0]['data'][-1]['item_id']).first()
            p = PaymentType.query.filter_by(id=order['transactions'][0]['data'][-1]['payment_type_id']).first()
            o = Order(**order['transactions'][0]['data'][-1])
            o.payment_type=p
            o.supplier = s
            o.enterprise = e
            o.item = i
            temp_id.append(o.id)
            orders_bc.append(o)
    return orders_bc

def get_order(id):
    res = requests.get("http://localhost:5001/blockchain")
    orders = res.json()['chain'][1:][::-1]
    
    for order in orders:
        # if order['data'][-1][by] == value:
        if order['transactions'][0]['id']== id:
            # Remove action key
            del order['transactions'][0]['data'][-1]['action']
            
            # Change datetime string to datetime object
            order['transactions'][0]['data'][-1]['updated_at'] = datetime.now()
            order['transactions'][0]['data'][-1]['created_at'] = datetime.strptime(order['transactions'][0]['data'][-1]['created_at'],'%Y-%m-%dT%H:%M:%S')
            
            s= Supplier.query.filter_by(id=order['transactions'][0]['data'][-1]['supplier_id']).first()
            e= Enterprise.query.filter_by(id= order['transactions'][0]['data'][-1]['enterprise_id']).first()
            i = Item.query.filter_by(id=order['transactions'][0]['data'][-1]['item_id']).first()
            p = PaymentType.query.filter_by(id=order['transactions'][0]['data'][-1]['payment_type_id']).first()
            # o = Order(**order['transactions'][0]['data'][-1])
            o = Order.query.filter_by(id=order['transactions'][0]['id']).first()
            o.supplier = s
            o.enterprise = e
            o.item = i
            result = o
            break
    return result

def get_order_id():
    res = requests.get("http://localhost:5001/blockchain")
    orders = res.json()['chain'][1:]
    if len(orders)== 0:
        return 1
    else:
        id = orders[-1]['transactions'][0]['id']+1
        return id
class ApplyLoanSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ApplyLoan
        include_fk = True

@app.route('/enterprise',methods=['GET'])
def enterprise_index():
    url = urlparse(request.referrer)
    if url.path == '/supplier' or url.path == '/profile-supplier' or url.path == '/finance':
        return render_template("common/failed.html")
        # , user='supplier')
    
    # orders = Order.query.filter_by(enterprise_id=1).all()

    # Query Order from blockchain
    orders = get_orders(by='enterprise_id',value=1)
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
        data['id'] = get_order_id()
        # Commit data to get primary key
        order = Order(**data)
        # db.session.add(order)
        # db.session.commit()
        order_schema = OrderSchema()

        #Digital Enterprise Sign
        enterprise_private_file = File.read(f"./key/private/{enterprise}.pem")
        enterprise_privatekey = PrivateKey.fromPem(enterprise_private_file)
        signature = Ecdsa.sign(json.dumps(order_schema.dump(order)),enterprise_privatekey).toBase64()
        order.sign_enterprise = signature
        db.session.add(order)
        db.session.commit()

        order_serializer = order_schema.dump(order)
        order_serializer['action'] = "create_order"

        ## Send to Blockchain Service
        res= requests.post("http://localhost:5001/transaction/broadcast",json=order_serializer)
        if res.status_code== 200:
            r = requests.get("http://localhost:5001/mine")
            if r.status_code==200:
            # Save with digital signature
                db.session.commit()
                flash('Order sukses ditambahkan')
                return make_response(jsonify({"order": data, "message": "Order sukses ditambahkan"}), 200)
        else:
            return "<h1>Error<h1>"


                

@app.route('/')
def index_user():
    # ---------------Create and Run Init SQL SCRIPT---------
    # db.create_all()
    # with open("./scf.sql") as file:
    #     queries = file.read().split(";")
    #     for q in queries:
    #         query = text(q)
    #         db.engine.execute(query) 
    #--------------------------------------------------------
    return render_template("auth/select_account.html")


@app.route('/supplier')
def main_menu_supplier():
    url = urlparse(request.referrer)
    if url.path == '/enterprise':
        return render_template("common/failed.html", user='enterprise')
    orders = get_orders(by='supplier_id',value=1)
    # data = Order.query.filter_by(supplier_id=1).all()
    return render_template('supplier/manage_orders.html', 
        manage_orders = orders
    )
@app.route('/supplier/order/<id>',methods=['GET'])
def confirm_order_from_supplier(id):
    order = Order.query.filter_by(id=id).first()
    order_schema = OrderSchema()
    # order = get_order(int(id))

    #Digital Enterprise Sign
    supplier_private_file = File.read(f"./key/private/{order.supplier.owner_name}.pem")
    supplier_privatekey = PrivateKey.fromPem(supplier_private_file)
    signature = Ecdsa.sign(json.dumps(order_schema.dump(order)),supplier_privatekey).toBase64()
    order.sign_supplier = signature

    #Update order supplier signature
    order_db = Order.query.filter_by(id=id).first()
    order_db.sign_supplier = signature
    db.session.commit()    

    # Serialize Order orm and add action description
    order_serializer = order_schema.dump(order)
    order_serializer['action'] = "sign_by_supplier"
    
    # Send to BC
    res= requests.post("http://localhost:5001/transaction/broadcast",json=order_serializer)
    if res.status_code== 200:
        r = requests.get("http://localhost:5001/mine")
        if r.status_code==200:
            db.session.commit()
            data = get_orders(by='supplier_id',value=1)
            return render_template('supplier/manage_orders.html', 
                manage_orders = data
            )

@app.route('/api/order/<id>', methods = ['GET'])
def get_order_endpoint(id):
    o = get_order(int(id))
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
    return make_response(jsonify(order), 200)
    
@app.route('/profile-supplier')
def view_supplier_profile():
    url = urlparse(request.referrer)
    if url.path == '/enterprise' or url.path == '/finance':
        return render_template("common/failed.html")
    suppliers = Supplier.query.all()
    return render_template('supplier/profile.html',
        profile = suppliers
    )

    
@app.route('/enterprise/order/<id>',methods=['POST'])
def upload_voucher(id):
    # order = Order.query.filter_by(id=id).first()
    order = get_order(int(id))
    file = request.files['file']
    # Check file is valid and save it
    if file.filename.endswith('jpg') or file.filename.endswith('png') or file.filename.endswith('pdf') or file.filename.endswith('PNG'):
        ID = uuid.uuid4().hex
        folder = 'static/' + UPLOAD_FOLDER +"/" + ID
        current_time = str(datetime.now()).replace('-', '_').replace(':', '_')
        if not os.path.exists(folder):
            os.mkdir(folder)
        filename  = folder + '/' + current_time + "." + file.filename.split(".")[-1]
        file.save(filename)
        order.upload_voucher = ID + '/' + current_time + "." + file.filename.split(".")[-1]
        order_schema = OrderSchema()
        order_serializer = order_schema.dump(order)
        order_serializer['action'] = "enterprise_upload_voucher"
        res= requests.post("http://localhost:5001/transaction/broadcast",json=order_serializer)
        if res.status_code== 200:
            r = requests.get("http://localhost:5001/mine")
            if r.status_code==200:
                db.session.commit()
                return redirect(url_for('enterprise_index'))
            else:
                return "<h1>Cant mine block</h1>"
        else:
            return "<h1>Blockchain cant accept data</h1>"
    else:
        return "<h1>The format is not accepted</h1>"

@app.route('/finance')
def index_finance():
    url = urlparse(request.referrer)
    if url.path == '/enterprise' or url.path == '/supplier':
        return render_template("common/failed.html")
    # data = ApplyLoan.query.join(Order, Order.id == ApplyLoan.order_id).order_by(ApplyLoan.id).all()
    data = ApplyLoan.query.all()
    return render_template('finance/index.html', 
        loans = data
    )


@app.route('/api/supplier/upload-additional-data',methods=['POST'])
def upload_additional_data_supplier():
    order_id = request.form.get('order_id')
    
    if 'finance_report_file' not in request.files and 'sell_order_file' not in request.files and 'account_statement_file' not in request.files:
        # flash('No file part')
        return redirect(request.url)        
    finance_report_file = request.files['finance_report_file']
    sell_order_file = request.files['sell_order_file']
    account_statement_file = request.files['account_statement_file']

    files = [finance_report_file, sell_order_file, account_statement_file]

    for i in files:
        if i.filename == '':
            # flash('No selected file')
            redirect(request.url)
            break
    
    filenames = []
    ID = uuid.uuid4().hex
    folder = 'static/' + UPLOAD_FOLDER +"/" + ID
    if not os.path.exists(folder):
        os.mkdir(folder)
    for i in files:
        if i.filename.endswith('pdf'):
            current_time = str(datetime.now()).replace('-', '_').replace(':', '_')
            filename  = folder + '/' + current_time + "." + i.filename.split(".")[-1]
            i.save(filename)
            filenames.append(filename)
    # return make_response(jsonify({"order": order_id, "message": "Order sukses ditambahkan"}), 200)
    order = get_order(int(order_id))
    app = ApplyLoan(finance_report_path=filenames[0], sell_report_path=filenames[1], account_statement_path=filenames[2])
    app.order = order
    db.session.add(app)   
    db.session.commit()

    

    # 'Update' Applyloan id in Blockchain
    order.applyloan_id = app.id
    order_schema = OrderSchema()
    order_serializer = order_schema.dump(order)
    order_serializer['action'] = "apply_loan"
    res= requests.post("http://localhost:5001/transaction/broadcast",json=order_serializer)
    if res.status_code== 200:
        r = requests.get("http://localhost:5001/mine")
        if r.status_code==200:
            db.session.commit()
            return redirect(url_for('main_menu_supplier'))
        else:
            return "<h1>Cant mine block</h1>"
    else:
        return "<h1>Error</h1>"


@app.route('/api/finance/confirm/<loan_id>', methods=['GET'])  # type: ignore
def confirm_loan_by_finance(loan_id):
    schema = ApplyLoanSchema()
    loan = ApplyLoan.query.filter_by(id=loan_id).first()
    #Digital Enterprise Sign
    private_key_file = File.read(f"./key/private/financier.pem")
    private_key = PrivateKey.fromPem(private_key_file)

    loan_schema_json = schema.dump(loan)
    signature = Ecdsa.sign(json.dumps(loan_schema_json),private_key).toBase64()
    
    # Add Digital Signature
    loan.sign_finance = signature
    db.session.add(loan)
    db.session.commit()

    # Get order from BC
    order = get_order(int(loan.order.id))
    order.applyloan_id = loan.id
    order_schema = OrderSchema()
    order_serializer = order_schema.dump(order)
    order_serializer['action'] = "loan_confirm_by_finance"
    res= requests.post("http://localhost:5001/transaction/broadcast",json=order_serializer)
    if res.status_code== 200:
        r = requests.get("http://localhost:5001/mine")
        if r.status_code==200:
            db.session.commit()
            return make_response(json.dumps(loan, cls=AlchemyEncoder))
        else:
            return "<h1>Cant mine block</h1>"
    else:
        return "<h1>Blockchain cant accept data<h1>"

if __name__ == '__main__':
    app.run(debug=True)
    