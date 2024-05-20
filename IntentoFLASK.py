from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask("primer-web-pythonflask")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:*Futbol2004@localhost/zoila'
db = SQLAlchemy(app)

class Productos(db.Model):
    __tablename__ = 'producto'
    id_producto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedores.id_proveedor'))
    nombre_producto = db.Column(db.String(100), nullable=False)
    precio_producto = db.Column(db.Numeric(10, 2), nullable=False)
    descripcion_producto = db.Column(db.String(100), nullable=False)
    stock_producto = db.Column(db.Integer, nullable=False)

class Cliente(db.Model):
    id_cliente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_cliente = db.Column(db.String(100), nullable=False)

class Empleado(db.Model):
    id_empleado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_empleado = db.Column(db.String(100), nullable=False)
    rfc_empleado = db.Column(db.String(15), nullable=False)
    direccion_empleado = db.Column(db.String(100), nullable=False)

class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    id_proveedor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre_proveedor = db.Column(db.String(100), nullable=False)
    telefono_proveedor = db.Column(db.String(20), nullable=False)


class Detalle_Venta(db.Model):
    __tablename__ = 'detalle_venta'
    id_detalle = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id_producto'))
    descripcion_detalle = db.Column(db.String(100), nullable=False)
    cantidad_detalle = db.Column(db.Integer, nullable=False)
    precio_venta = db.Column(db.Numeric(10, 2), nullable=False)


@app.route("/Producto", methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        id_proveedor = request.form.get('id_proveedor')
        nombre_producto = request.form.get('nombre_producto')
        precio_producto = request.form.get('precio_producto')
        descripcion_producto = request.form.get('descripcion_producto')
        stock_producto = request.form.get('stock_producto')

        nuevo_producto = Productos(id_proveedor=id_proveedor, nombre_producto=nombre_producto, precio_producto=precio_producto, descripcion_producto=descripcion_producto, stock_producto=stock_producto)

        db.session.add(nuevo_producto)
        db.session.commit()
        return redirect(url_for('hola_prueba'))
    
    elif request.method == 'GET':
        return render_template("Producto.html")
    else:
        return "Método no permitido", 405


@app.route("/Cliente", methods=['GET', 'POST'])
def add_cliente():
    if request.method == 'POST':
        nombre_cliente = request.form.get('nombre_cliente')

        nuevo_cliente = Cliente(nombre_cliente=nombre_cliente)

        db.session.add(nuevo_cliente)
        db.session.commit()
        return redirect(url_for('hola_prueba'))
    
    elif request.method == 'GET':
        return render_template("Cliente.html")
    else:
        return "Método no permitido", 405


@app.route("/Empleado", methods=['GET', 'POST'])
def add_empleado():
    if request.method == 'POST':
        nombre_empleado = request.form.get('nombre_empleado')
        rfc_empleado = request.form.get('rfc_empleado')
        direccion_empleado = request.form.get('direccion_empleado')

        nuevo_empleado = Empleado(nombre_empleado=nombre_empleado, rfc_empleado=rfc_empleado, direccion_empleado=direccion_empleado)

        db.session.add(nuevo_empleado)
        db.session.commit()
        return redirect(url_for('hola_prueba'))
    
    elif request.method == 'GET':
        return render_template("Empleado.html")
    else:
        return "Método no permitido", 405
    

@app.route("/Proveedor", methods=['GET', 'POST'])
def add_proveedores():
    if request.method == 'POST':
        nombre_proveedor = request.form.get('nombre_proveedor')
        telefono_proveedor = request.form.get('telefono_proveedor')

        nuevo_proveedores = Proveedor(nombre_proveedor=nombre_proveedor, telefono_proveedor=telefono_proveedor)

        db.session.add(nuevo_proveedores)
        db.session.commit()
        return redirect(url_for('hola_prueba'))
    
    elif request.method == 'GET':
        return render_template("Proveedor.html")
    else:
        return "Método no permitido", 405
    

@app.route("/DetalleVenta", methods=['GET', 'POST'])
def add_detalle_venta():
    if request.method == 'POST':
        id_productos = request.form.getlist('id_producto[]')
        descripciones_detalle = request.form.getlist('descripcion_detalle[]')
        cantidades_detalle = request.form.getlist('cantidad_detalle[]')
        precios_venta = request.form.getlist('precio_venta[]')
        total_venta = request.form.get('total_venta')

        print(f"ID Productos: {id_productos}")
        print(f"Descripciones: {descripciones_detalle}")
        print(f"Cantidad: {cantidades_detalle}")
        print(f"Precios: {precios_venta}")
        print(f"Total Venta: {total_venta}")

        for id_producto, descripcion_detalle, cantidad_detalle, precio_venta in zip(id_productos, descripciones_detalle, cantidades_detalle, precios_venta):
            nuevo_detalle_venta = Detalle_Venta(
                id_producto=id_producto,
                descripcion_detalle=descripcion_detalle,
                cantidad_detalle=cantidad_detalle,
                precio_venta=precio_venta
            )

            producto = Productos.query.filter_by(id_producto=id_producto).first()
            if producto and producto.stock_producto >= int(cantidad_detalle):
                producto.stock_producto -= int(cantidad_detalle)

                db.session.add(nuevo_detalle_venta)
            else:
                return f"No hay suficiente stock para el producto ID {id_producto} o producto no encontrado", 400

        db.session.commit()
        return redirect(url_for('hola_prueba'))
    
    elif request.method == 'GET':
        return render_template("DetalleVenta.html")
    else:
        return "Método no permitido", 405

@app.route("/", methods=['GET', 'POST'])
def hola_prueba():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host = '0.0.0.0', port = '5000')