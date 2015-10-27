drop table if exists casas;
drop table if exists vendedores;
create table casas (
	id integer primary key autoincrement,
	nombre text not null,
	vendedor integer not null,
	construccion float,
	terreno float,
	precio float,
	balance float,
	status integer
);
create table vendedores (
	id integer primary key autoincrement,
	nombre text not null,
	balance float
);
