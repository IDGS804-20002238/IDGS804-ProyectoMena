USE mena;


CREATE TABLE cat_Estatus(
	estatus int NOT NULL PRIMARY KEY IDENTITY(1,1),
	descripcionEstatus varchar(255) NOT NULL
);
CREATE TABLE material_usado(
  materialUsadoID int PRIMARY KEY  not null,
  telaUsada varchar(50) NOT NULL,
  cantidadTela int not null,
  hiloUsado int not null,
  cierreUsado int not null,
  carroUsado int NOT NULL,
  reflejanteUsado int NOT NULL,
  argollaUsada int NOT NULL,
  bandolaUsada int NOT NULL,
  hombreraUsada int NOT NULL,
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
  idrole int NOT NULL PRIMARY KEY IDENTITY(1,1),
  name varchar(80) DEFAULT NULL,
  description varchar(255) DEFAULT NULL
);
CREATE TABLE domicilio(
	domicilioId int NOT NULL PRIMARY KEY IDENTITY(1,1),
	estado varchar(255) NOT NULL,
	municipio varchar(255) NOT NULL,
	codigoPostal int NOT NULL,
	colonia varchar(255) NOT NULL,
	calle varchar(255) NOT NULL,
	numeroExt int NOT NULL,
	numeroInt int DEFAULT NULL,
	referencia varchar(255) NOT NULL
);
CREATE TABLE [user] (
  id int NOT NULL PRIMARY KEY IDENTITY(1,1),
  name varchar(50) NOT NULL,
  email varchar(255) DEFAULT NULL,
  password varchar(255) NOT NULL,
  active tinyint DEFAULT 1,
  confirmed_at datetime DEFAULT GETDATE(),
  idrole INT not null default 4,
  UNIQUE (email),
  domicilioId int NOT NULL,
  CONSTRAINT fk_domiclio_id FOREIGN KEY (domicilioId) REFERENCES domicilio(domicilioId),
  CONSTRAINT fk_rol_id FOREIGN KEY (idrole) REFERENCES role(idrole)
);

CREATE TABLE compras (
  idCompra int NOT NULL PRIMARY KEY IDENTITY(1,1),
  fechaCompra datetime NOT NULL,
  id int NOT NULL,
  estado varchar(255) NOT NULL,
  municipio varchar(255) NOT NULL,
  codigoPostal int NOT NULL,
  colonia varchar(255) NOT NULL,
  calle varchar(255) NOT NULL,
  numeroExt int NOT NULL,
  numeroInt int DEFAULT NULL,
  referencia varchar(255) NOT NULL,
  subtotal int NOT NULL,
  totalBotiquines int NOT NULL,
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

CREATE TABLE materiaPrima (
  materiaPrimaId int NOT NULL PRIMARY KEY IDENTITY(1,1),
  image_name varchar(255) DEFAULT NULL,
  nombreMateriaPrima varchar(255)NOT NULL,
  metrosMateriaPrima int NOT NULL
);

CREATE TABLE proovedores(
	proovedoresId int NOT NULL PRIMARY KEY IDENTITY(1,1),
	nombre varchar(250) NOT NULL,
	materiaPrima varchar(250) NOT NULL,
	costoxmetro varchar(250) NOT NULL,
	estatus int NOT NULL DEFAULT 1
);

CREATE TABLE compraMateriaPrima(
	compraMateriaPrimaID int NOT NULL PRIMARY KEY IDENTITY(1,1),
	proovedoresId int NOT NULL,
	cantidadEnMetros int NOT NULL,
	pagoTotal int NOT NULL,
	confirmed_at datetime DEFAULT GETDATE(),
	CONSTRAINT fk_proovedores_proovedoresId FOREIGN KEY (proovedoresId) REFERENCES proovedores(proovedoresId),
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

CREATE VIEW v_detalle_compras
AS
SELECT dc.idDetalleCompra, c.idCompra AS CompraId, c.fechaCompra, u.id AS UsuarioID, u.name AS UsuarioNombre, p.nombre AS ProductoNombre, p.tipoProductoID, dc.cantidad, dc.costo, dc.cantidad * dc.costo AS subtotal, e.descripcionEstatus AS Estatus
FROM compras c
INNER JOIN [user] u ON c.id = u.id
INNER JOIN detalleCompra dc ON c.idCompra = dc.idCompra
INNER JOIN productos p ON dc.idProducto = p.idProducto
INNER JOIN cat_Estatus e ON c.estatus = e.estatus
WITH CHECK OPTION;


CREATE VIEW v_compras_estatus AS
SELECT c.idCompra, c.fechaCompra, c.id,u.name as userName, c.subtotal, e.descripcionEstatus,
concat(compras.estado, ', ', compras.municipio, '. ', compras.colonia, '. ', compras.codigoPostal, '. ',
compras.calle, ' ', compras.numeroExt,
CASE WHEN compras.numeroInt <> '0' THEN concat(' ', compras.numeroInt) ELSE '' END,
'. ', compras.referencia) as domicilio
FROM compras c
INNER JOIN cat_Estatus e ON c.estatus = e.estatus
INNER JOIN [user] u ON c.id = u.id
INNER JOIN compras ON c.idCompra = compras.idCompra;



CREATE VIEW v_detalle_compras_con_material AS
SELECT dc.idDetalleCompra, c.idCompra AS CompraId, c.fechaCompra, u.id AS UsuarioID, u.name AS UsuarioNombre, 
       p.nombre AS ProductoNombre, p.tipoProductoID, 
       dc.cantidad, dc.costo, dc.cantidad * dc.costo AS subtotal, 
       e.descripcionEstatus AS Estatus,
       tp.materialUsadoID,
       telaUsada, 
       mu.cantidadTela * dc.cantidad AS cantidadTela, 
       mu.hiloUsado * dc.cantidad AS hiloUsado, 
       mu.cierreUsado * dc.cantidad AS cierreUsado,
       mu.carroUsado * dc.cantidad AS carroUsado ,
       mu.reflejanteUsado * dc.cantidad AS reflejanteUsado ,
       mu.argollaUsada * dc.cantidad AS argollaUsada ,
       mu.bandolaUsada * dc.cantidad AS bandolaUsada ,
       mu.hombreraUsada * dc.cantidad AS hombreraUsada 
FROM compras c
INNER JOIN [user] u ON c.id = u.id
INNER JOIN detalleCompra dc ON c.idCompra = dc.idCompra
INNER JOIN productos p ON dc.idProducto = p.idProducto
INNER JOIN cat_Estatus e ON c.estatus = e.estatus
LEFT JOIN tipo_producto tp ON p.tipoProductoID = tp.tipoProductoID
LEFT JOIN material_usado mu ON tp.materialUsadoID = mu.materialUsadoID;

CREATE VIEW v_user_con_domicilio AS
SELECT u.id, u.name, u.email,u.password, d.estado, d.municipio, d.codigoPostal, d.colonia, d.calle, d.numeroExt, d.numeroInt, d.referencia
FROM [user] u
INNER JOIN domicilio d ON u.domicilioId = d.domicilioId;

CREATE VIEW v_usuario_con_domicilio AS
SELECT u.id, u.name, u.email,
       r.name as role_name,
	   u.active,
       CONCAT(d.estado, ', ', d.municipio, '. ', d.colonia, '. ', d.codigoPostal, '. ',
              d.calle, ' ', d.numeroExt,
              CASE WHEN d.numeroInt <> '0' THEN CONCAT(' ', d.numeroInt) ELSE '' END,
              '. ', d.referencia) as domicilio
FROM [user] u
JOIN role r ON u.idrole = r.idrole
JOIN domicilio d ON u.domicilioId = d.domicilioId

----------------------------------------------------------INSERTS---------------------------------------------------------
SET IDENTITY_INSERT role ON
INSERT INTO role (idrole, name, description) VALUES
(1, 'Admin', 'administrador'),
(2, 'Empleado', 'Empleado de la empresa'),
(3, 'Repartidor', 'Repartidor de la emprea'),
(4, 'Cliente', 'Cliente de la empresa'),
(5, 'Inactivo', 'Usuario Inactivo');
SET IDENTITY_INSERT role OFF

SET IDENTITY_INSERT domicilio ON
INSERT INTO domicilio (domicilioId,estado,municipio,codigoPostal,colonia,calle,numeroExt,referencia)
VALUES
(1,'guanajuato','leon','37570','Granjeno Plus','Granja eva','114','casa dos pisos porton negro'),
(2,'guanajuato','leon','37570','Granjeno Plus','Granja Norma','232','casa roja'),
(3,'guanajuato','leon','37570','Granjeno Plus','Granja Martha','452','casa verde con reja negra');
SET IDENTITY_INSERT domicilio OFF

SET IDENTITY_INSERT [user] ON
INSERT INTO [user] (id, name, [email], [password], active, idrole, domicilioId) 
VALUES
(1,'angel', 'angeltovar308@gmail.com', 'sha256$5DGfv5cgFrKbMZz3$52389e87feb6e1a17cad14d8fe8fcef25bbecb0564c6a7ec4752e99f55328d79',1,1,1),
(2,'Jose', 'angro1212@gmail.com', 'sha256$6j2avdMEX7UgH3HT$a9ea793320d38ead008540397c27054079389b76e12ab9b99da9568af83b5e53',1,2,2),
(3,'pedro', '3@gmail.com', 'sha256$ERUhmMIzpUKtOSw4$eddbb4db44c30094412ebfebdfe42db31de476ae19d75d41193bf281325048a0',1,3,3);
SET IDENTITY_INSERT [user] OFF

-- Insertar datos en la tabla material_usado
INSERT INTO material_usado (materialUsadoID, telaUsada, cantidadTela, hiloUsado, cierreUsado,carroUsado,reflejanteUsado,argollaUsada,bandolaUsada,hombreraUsada)
VALUES 
    (1, 'Roja', 2, 100, 3,6,1,2,1,1),
    (2, 'Roja', 1, 60, 1,2,1,2,1,1),
    (3, 'Roja', 2, 130, 2,5,1,2,1,1),
    (4, 'Roja', 2, 170, 2,6,1,2,1,1),
    (5, 'Roja', 3, 200, 3,10,2,2,1,1);

-- Insertar datos en la tabla tipo_producto
INSERT INTO tipo_producto (tipoProductoID, nombreProducto, materialUsadoID)
VALUES 
    (1, 'Botiquin 4 bolsas', 1),
    (2, 'Botiquin mini', 2),
    (3, 'Botiquin 3 bolsas', 3),
    (4, 'Botiquin 5 bolsas', 4),
    (5, 'Botiquin para ambulancia', 5);

-- Insertar datos en la tabla productos
SET IDENTITY_INSERT productos ON
INSERT INTO productos (idProducto,nombre, precio, tipoProductoID, image_name, estatus)
VALUES
  (1,'Botiquin de Primeros Auxilios 4 bolsas', '514', 1, 'botiquin_4_bolsas.png', 1),
  (2,'Botiquin de Primeros Auxilios mini', '698', 2, 'botiquin_mini.png', 1),
  (3,'Botiquin de Primeros Auxilios 3 bolsas', '731', 3, 'botiquin_3_bolsas.png', 1),
  (4,'Botiquin de Primeros Auxilios 5 bolsas', '800', 4, 'botiquin_5_bolsas.png', 1),
  (5,'Botiquin de Primeros Auxilios Para Ambulancia', '696', 5, 'botiquin_ambulancia.png', 1);
SET IDENTITY_INSERT productos OFF



-- Insertar datos en la tabla materiaPrima
INSERT INTO materiaPrima (nombreMateriaPrima,image_name,metrosMateriaPrima) 
VALUES 
	('Roja','telaRoja.png',200),
	('Hilo','Hilo.png',10000),
	('Cierre','Cierre.png',100),
	('Carros','carros.png',100),
	('Reflejante','reflejante.png',100),
	('Argollas','argolla.png',100),
	('Bandola','bandola.png',100),
	('Hombrera','hombrera.png',100);

SET IDENTITY_INSERT cat_Estatus ON
INSERT INTO cat_Estatus (estatus,descripcionEstatus) 
values
	(1,'EN ESPERA DE ELABORACION'),
	(2,'ELABORANDO PEDIDO'),
	(3,'PEDIDO ENVIADO'),
	(4,'PEDIDO ENTREGADO'),
	(5,'PEDIDO CANCELADO');
SET IDENTITY_INSERT cat_Estatus OFF


----------------------------------------------------------querys---------------------------------------------------------
/*
USE mena;
DROP TABLE [user];
DROP TABLE domicilio;
DROP TABLE role;
DROP TABLE roles_users;
DROP TABLE productos;
DROP TABLE material_usado;
DROP TABLE tipo_producto;
DROP TABLE materiaPrima;
DROP TABLE compras;
DROP TABLE detalleCompra;
DROP TABLE cat_Estatus;
DROP TABLE proovedores;
DROP TABLE compraMateriaPrima;


DROP VIEW v_tipo_producto;
DROP VIEW v_detalle_producto;
DROP VIEW v_detalle_compras;
DROP VIEW v_roles_users;
DROP VIEW v_compras_estatus;
DROP VIEW v_detalle_compras_con_material;
DROP VIEW v_user_con_domicilio;
DROP VIEW v_usuario_con_domicilio;



select * from [user];
select * from domicilio;
select * from role;
select * from productos;
select * from material_usado;
select * from tipo_producto;
select * from materiaPrima;
select * from compras;
select * from detalleCompra;
select * from cat_Estatus;
select * from proovedores;
select * from compraMateriaPrima;



select * from v_tipo_producto;
select * from v_detalle_producto;
select * from v_detalle_compras;
select * from v_roles_users;
select * from v_compras_estatus;
select * from v_detalle_compras_con_material;
select * from v_user_con_domicilio;
select * from v_usuario_con_domicilio;






UPDATE [user]
SET active = 1 WHERE id=6;
*/
UPDATE [user]
SET idrole = 3 WHERE id=4;




