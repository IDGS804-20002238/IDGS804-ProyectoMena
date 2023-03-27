USE mena;


CREATE TABLE material_usado(
  materialUsadoID int PRIMARY KEY  not null,
  telaUsada varchar(50) NOT NULL,
  cantidadTela int not null,
  hiloUsado int not null,
  cierreUsado int not null
);

CREATE TABLE tipo_producto(
  tipoProductoID int PRIMARY KEY  not null,
  nombreProducto varchar(50) NOT NULL,
  materialUsadoID int not null,
  FOREIGN KEY (materialUsadoID) REFERENCES material_usado(materialUsadoID)
);

CREATE TABLE productos (
  idProducto int NOT NULL PRIMARY KEY IDENTITY(1,1),
  nombre varchar(255) NOT NULL,
  precio varchar(255) DEFAULT NULL,
  tipoProductoID int not null,
  image_name varchar(255) DEFAULT NULL,
  estatus int DEFAULT NULL
  FOREIGN KEY (tipoProductoID) REFERENCES tipo_producto(tipoProductoID)
);

CREATE TABLE role (
  id int NOT NULL PRIMARY KEY IDENTITY(1,1),
  name varchar(80) DEFAULT NULL,
  description varchar(255) DEFAULT NULL
);

CREATE TABLE [user] (
  id int NOT NULL PRIMARY KEY IDENTITY(1,1),
  name varchar(50) NOT NULL,
  email varchar(255) DEFAULT NULL,
  password varchar(255) NOT NULL,
  active tinyint DEFAULT NULL,
  confirmed_at datetime DEFAULT NULL,
  UNIQUE (email)
);

CREATE TABLE compras (
  idCompra int NOT NULL PRIMARY KEY IDENTITY(1,1),
  fechaCompra datetime NOT NULL,
  id int NOT NULL,
  subtotal int NOT NULL,
  estatus int default 1
  CONSTRAINT fk_compras_user FOREIGN KEY (id) REFERENCES [user](id)
);

CREATE TABLE detalleCompra (
  idDetalleCompra int NOT NULL PRIMARY KEY IDENTITY(1,1),
  idCompra int NOT NULL,
  idProducto int NOT NULL,
  cantidad int NOT NULL,
  costo float NOT NULL,
  CONSTRAINT fk_compras_idCompra FOREIGN KEY (idCompra) REFERENCES compras(idCompra),
  CONSTRAINT fk_compras_idProducto FOREIGN KEY (idProducto) REFERENCES productos(idProducto)
);

CREATE TABLE roles_users (
  userId int DEFAULT NULL ,
  roleId int DEFAULT NULL,
  FOREIGN KEY (userId) REFERENCES [user](id),
  FOREIGN KEY (roleId) REFERENCES role(id)
);

CREATE TABLE materiaPrima (
  materiaPrimaId int NOT NULL PRIMARY KEY IDENTITY(1,1),
  image_name varchar(255) DEFAULT NULL,
  nombreMateriaPrima varchar(255)NOT NULL,
  metrosMateriaPrima int NOT NULL
);

----------------------------------------------------------Vistas---------------------------------------------------------
CREATE VIEW v_tipo_producto AS
SELECT tipoProductoID, nombreProducto
FROM tipo_producto;

CREATE VIEW v_detalle_producto AS
SELECT p.idProducto, p.nombre, p.precio, t.nombreProducto, m.telaUsada, m.cantidadTela, m.hiloUsado, m.cierreUsado
FROM productos p
JOIN tipo_producto t ON p.tipoProductoID = t.tipoProductoID
JOIN material_usado m ON t.materialUsadoID = m.materialUsadoID;

CREATE VIEW v_detalle_compras AS
SELECT c.idCompra AS CompraId, c.fechaCompra, u.id AS UsuarioID, u.name AS UsuarioNombre, p.nombre AS ProductoNombre, dc.cantidad, dc.costo, dc.cantidad * dc.costo AS subtotal
FROM compras c
INNER JOIN [user] u ON c.id = u.id
INNER JOIN detalleCompra dc ON c.idCompra = dc.idCompra
INNER JOIN productos p ON dc.idProducto = p.idProducto;

CREATE VIEW v_roles_users AS
SELECT u.id AS userId, u.name AS userName, r.id AS roleId, r.name AS roleName
FROM roles_users ru
INNER JOIN [user] u ON ru.userId = u.id
INNER JOIN role r ON ru.roleId = r.id;



----------------------------------------------------------INSERTS---------------------------------------------------------
SET IDENTITY_INSERT [user] ON
INSERT INTO [user] (id, name, [email], [password], [active], [confirmed_at]) 
VALUES
(1,'angel', 'angeltovar308@gmail.com', 'sha256$5DGfv5cgFrKbMZz3$52389e87feb6e1a17cad14d8fe8fcef25bbecb0564c6a7ec4752e99f55328d79', 1, NULL),
(2,'Jose', 'angro1212@gmail.com', 'sha256$6j2avdMEX7UgH3HT$a9ea793320d38ead008540397c27054079389b76e12ab9b99da9568af83b5e53', 1, NULL),
(3,'pedro', '3@gmail.com', 'sha256$ERUhmMIzpUKtOSw4$eddbb4db44c30094412ebfebdfe42db31de476ae19d75d41193bf281325048a0', 1, NULL);
SET IDENTITY_INSERT [user] OFF

SET IDENTITY_INSERT role ON
INSERT INTO role (id, name, description) VALUES
(1, 'Admin', 'administrador'),
(2, 'Empleado', 'Empleado de la empresa'),
(3, 'Repartidor', 'Repartidor de la emprea'),
(4, 'Cliente', 'Cliente de la empresa');
SET IDENTITY_INSERT role OFF

SET IDENTITY_INSERT productos ON
INSERT INTO productos (idProducto, nombre, precio, image_name, estatus) VALUES
(1, 'destiny', '123', '6.png', 1),
(2, 'Halo Reach', '607', '4.png', 2);
SET IDENTITY_INSERT productos OFF


INSERT INTO roles_users (userId, roleId) VALUES
(1, 1),
(2, 2),
(3,4);

-- Insertar datos en la tabla material_usado
INSERT INTO material_usado (materialUsadoID, telaUsada, cantidadTela, hiloUsado, cierreUsado)
VALUES 
    (1, 'Roja', 5, 1, 1),
    (2, 'Azul', 5, 1, 1),
    (3, 'Blanco', 5, 1, 1),
    (4, 'Militar', 5, 1, 1),
    (5, 'Mezclilla', 5, 1, 1);

-- Insertar datos en la tabla tipo_producto
INSERT INTO tipo_producto (tipoProductoID, nombreProducto, materialUsadoID)
VALUES 
    (1, 'Botiquin Rojo', 1),
    (2, 'Botiquin Azul', 2),
    (3, 'Botiquin Blanco', 3),
    (4, 'Botiquin Militar', 4),
    (5, 'Botiquin Mezclilla', 5);

-- Insertar datos en la tabla materiaPrima
INSERT INTO materiaPrima (nombreMateriaPrima,image_name,metrosMateriaPrima) 
VALUES 
	('Roja','telaRoja.png',100),
	('Azul','telaAzul.png',100),
	('Blanco','telaBlanca.png',100),
	('Militar','telaMilitar.png',100),
	('Mezclilla','telaMezclilla.png',100),
	('Hilo','Hilo.png',10),
	('Cierre','Cierre.png',10);


----------------------------------------------------------querys---------------------------------------------------------
/*
USE mena;
DROP TABLE roles_users;
DROP TABLE [user];
DROP TABLE role;
DROP TABLE productos;
DROP TABLE material_usado;
DROP TABLE tipo_producto;
DROP TABLE materiaPrima;
DROP TABLE compras;
DROP TABLE detalleCompra;


DROP VIEW v_tipo_producto;
DROP VIEW v_detalle_producto;
DROP VIEW v_detalle_compras;
DROP VIEW v_roles_users;


select * from roles_users;
select * from [user];
select * from role;
select * from productos;
select * from material_usado;
select * from tipo_producto;
select * from materiaPrima;
select * from compras;
select * from detalleCompra;


select * from v_tipo_producto;
select * from v_detalle_producto;
select * from v_detalle_compras;
select * from v_roles_users;
*/
SELECT name
FROM sys.foreign_keys
WHERE parent_object_id = OBJECT_ID('[user]')
  AND referenced_object_id = OBJECT_ID('compras');