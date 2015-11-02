drop table if exists casa;
drop table if exists vendedor;

create table vendedor (
	id integer primary key autoincrement,
	nombre text not null,
	balance float
);

create table casa (
	id integer primary key autoincrement,
	nombre text not null,
	vendedor integer,
	construccion float,
	terreno float,
	precio float,
	balance float,
	status integer not null,
	FOREIGN KEY(vendedor) REFERENCES vendedor(id)
);