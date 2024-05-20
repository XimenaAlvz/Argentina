--Tabla Cliente
CREATE TABLE Cliente (
    ID_Cliente SERIAL PRIMARY KEY,
    Nombre_Cliente VARCHAR(100)
);

--Tabla Empleado
CREATE TABLE Empleado (
    ID_Empleado SERIAL PRIMARY KEY,
    Nombre_Empleado VARCHAR(100),
    RFC_Empleado VARCHAR(15),
    Direccion_Empleado VARCHAR(100)
);

--Tabla Proveedores
CREATE TABLE Proveedores (
    ID_Proveedor SERIAL PRIMARY KEY,
    Nombre_Proveedor VARCHAR(100),
    Telefono_Proveedor VARCHAR(20)
);

--Tabla Venta
CREATE TABLE Venta (
    ID_Venta SERIAL PRIMARY KEY,
    ID_Cliente INT REFERENCES Cliente(ID_Cliente),
    ID_Empleado INT REFERENCES Empleado(ID_Empleado),
    Fecha_Venta DATE,
    Total_Venta DECIMAL(10, 2)
);

--Tabla Producto
CREATE TABLE Producto (
    ID_Producto SERIAL PRIMARY KEY,
    ID_Proveedor INT REFERENCES Proveedores(ID_Proveedor),
    Nombre_Producto VARCHAR(100),
    Precio_Producto DECIMAL(10, 2),
    Descripcion_Producto VARCHAR(100),
    Stock_Producto INT
);

--Tabla Detalle_Venta
CREATE TABLE Detalle_Venta (
    ID_Detalle SERIAL PRIMARY KEY,
    ID_Producto INT REFERENCES Producto(ID_Producto),
	Descripcion_Detalle VARCHAR(100),
    Cantidad_Detalle INT,
    Precio_Venta DECIMAL(10, 2)
);


SELECT * FROM Cliente

SELECT * FROM Empleado

SELECT * FROM Proveedores

SELECT * FROM Producto

SELECT * FROM Detalle_Venta

