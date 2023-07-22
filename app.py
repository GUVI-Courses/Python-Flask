from flask import Flask,redirect,render_template,request,url_for
from flask.globals import request,session
from flask_sqlalchemy import SQLAlchemy
from flask import flash


local_server=True
app=Flask(__name__)
app.secret_key="@#%^#%R^#R#YTUG@B"

# database configuration
# app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/databasename'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/crudguvi'

db=SQLAlchemy(app)


class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))


class Products(db.Model):
    product_id=db.Column(db.Integer,primary_key=True)
    productName=db.Column(db.String(100))
    productDescription=db.Column(db.String(500))
    rating=db.Column(db.Integer)
    stocks=db.Column(db.Integer)
    productPrice=db.Column(db.Integer)



@app.route("/")
def home():
    products=Products.query.all()
    print(products)   
    return render_template("index.html",products=products)


@app.route("/test/")
def test():
    try:
        # query=Test.query.all()
        # print(query)
        sql_query="select * from test"
        with db.engine.begin() as conn:
            response=conn.exec_driver_sql(sql_query).all()
            print(response)
        return "Database is connected"
    except Exception as e:
        return f"Database is not connected, {e}"
    
# create or insert operation

@app.route("/create",methods=['GET','POST'])
def create():
    if request.method=="POST":
        productname=request.form.get('productname')
        productdesc=request.form.get('productDesc')
        productrating=request.form.get('rating')
        productstocks=request.form.get('stocks')
        productprice=request.form.get('price')
        # query=Products(productName=productname,productDescription=productdesc,rating=productrating,stocks=productstocks,productPrice=productprice)
        # db.session.add(query)
        # db.session.commit()
        query=f"INSERT INTO `products` (`productName`,`productDescription`,`rating`,`stocks`,`productPrice`) VALUES ('{productname}','{productdesc}','{productrating}','{productstocks}','{productprice}')"
        with db.engine.begin() as conn:
            response=conn.exec_driver_sql(query)
            flash("Product is Added","success")
            return redirect(url_for('home'))


        # return f'Product Added'

# edit operation
@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    product=Products.query.filter_by(product_id=id).first()

    if request.method=="POST":
        productname=request.form.get('productname')
        productdesc=request.form.get('productDesc')
        productrating=request.form.get('rating')
        productstocks=request.form.get('stocks')
        productprice=request.form.get('price') 

        query=f"UPDATE `products` SET `productName`='{productname}',`productDescription`='{productdesc}',`rating`='{productrating}',`stocks`='{productstocks}',`productPrice`='{productprice}' WHERE `product_id`='{id}'"
        with db.engine.begin() as conn:
            response=conn.exec_driver_sql(query)
            flash("Product is Updated","info")
            return redirect(url_for('home'))

    return render_template('edit.html',product=product)


# delete operation
@app.route('/delete/<int:id>',methods=['GET'])
def delete(id):
    # product=Products.query.filter_by(product_id=id).first()
    query=f"DELETE FROM `products` WHERE `product_id`={id}"
    with db.engine.begin() as conn:
        response=conn.exec_driver_sql(query)
        flash("Product is Deleted","warning")
        return redirect(url_for('home'))
    