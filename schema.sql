drop table if exists casa;
drop table if exists vendedor;

create table vendedor (
	id integer primary key autoincrement,
	nombre text not null,
	apellidos text not null,
	telefono number not null,
	email text not null,
	balance float
);

create table casa (
	id integer primary key autoincrement,
	nombre text not null,
	direccion text not null,
	vendedor integer,
	construccion float,
	terreno float,
	valor float,
	balance float,
	status integer not null,
	FOREIGN KEY(vendedor) REFERENCES vendedor(id)
);