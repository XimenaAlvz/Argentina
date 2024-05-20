from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask("primer-web-pythonflask")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:*Futbol2004@localhost/zoila'
db = SQLAlchemy(app)

# Definición de modelos
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

# Rutas para operaciones CRUD
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

        # Actualizar archivo de productos
        actualizar_archivo_productos()

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

        # Actualizar archivo de clientes
        actualizar_archivo_clientes()

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

        # Actualizar archivo de empleados
        actualizar_archivo_empleados()

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

        nuevo_proveedor = Proveedor(nombre_proveedor=nombre_proveedor, telefono_proveedor=telefono_proveedor)

        db.session.add(nuevo_proveedor)
        db.session.commit()

        # Actualizar archivo de proveedores
        actualizar_archivo_proveedores()

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

        for id_producto, descripcion_detalle, cantidad_detalle, precio_venta in zip(id_productos, descripciones_detalle, cantidades_detalle, precios_venta):
            cantidad_detalle = int(cantidad_detalle)
            precio_venta = float(precio_venta)
            nuevo_detalle_venta = Detalle_Venta(
                id_producto=id_producto,
                descripcion_detalle=descripcion_detalle,
                cantidad_detalle=cantidad_detalle,
                precio_venta=(precio_venta * cantidad_detalle)
            )

            producto = Productos.query.filter_by(id_producto=id_producto).first()
            if producto and producto.stock_producto >= int(cantidad_detalle):
                producto.stock_producto -= int(cantidad_detalle)

                db.session.add(nuevo_detalle_venta)
            else:
                return f"No hay suficiente stock para el producto ID {id_producto} o producto no encontrado", 400

        db.session.commit()

        # Actualizar archivo de detalles de venta y productos
        actualizar_archivo_detalle_venta()
        actualizar_archivo_productos()

        return redirect(url_for('hola_prueba'))
    
    elif request.method == 'GET':
        return render_template("DetalleVenta.html")
    else:
        return "Método no permitido", 405

@app.route("/", methods=['GET', 'POST'])
def hola_prueba():
    return render_template("index.html")

# Funciones para actualizar archivos de texto
def actualizar_archivo_productos():
    productos = Productos.query.all()
    contenido = ""
    for producto in productos:
        contenido += f"ID Producto: {producto.id_producto}, Nombre: {producto.nombre_producto}, Precio: {producto.precio_producto}, Stock: {producto.stock_producto}\n"
    
    escribir_en_archivo('productos.txt', contenido)

def actualizar_archivo_clientes():
    clientes = Cliente.query.all()
    contenido = ""
    for cliente in clientes:
        contenido += f"ID Cliente: {cliente.id_cliente}, Nombre: {cliente.nombre_cliente}\n"
    
    escribir_en_archivo('clientes.txt', contenido)

def actualizar_archivo_empleados():
    empleados = Empleado.query.all()
    contenido = ""
    for empleado in empleados:
        contenido += f"ID Empleado: {empleado.id_empleado}, Nombre: {empleado.nombre_empleado}, RFC: {empleado.rfc_empleado}, Dirección: {empleado.direccion_empleado}\n"
    
    escribir_en_archivo('empleados.txt', contenido)

def actualizar_archivo_proveedores():
    proveedores = Proveedor.query.all()
    contenido = ""
    for proveedor in proveedores:
        contenido += f"ID Proveedor: {proveedor.id_proveedor}, Nombre: {proveedor.nombre_proveedor}, Teléfono: {proveedor.telefono_proveedor}\n"
    
    escribir_en_archivo('proveedores.txt', contenido)

def actualizar_archivo_detalle_venta():
    detalles_venta = Detalle_Venta.query.all()
    contenido = ""
    for detalle in detalles_venta:
        contenido += f"ID Detalle Venta: {detalle.id_detalle}, ID Producto: {detalle.id_producto}, Descripción: {detalle.descripcion_detalle}, Cantidad: {detalle.cantidad_detalle}, Precio Venta: {detalle.precio_venta}\n"
    
    escribir_en_archivo('detalle_venta.txt', contenido)

# Función para escribir en un archivo de texto
def escribir_en_archivo(nombre_archivo, contenido):
    with open(nombre_archivo, 'w') as file:
        file.write(contenido)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)