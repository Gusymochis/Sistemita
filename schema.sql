drop table if exists casas;
drop table if exists vendedores;
create table casa (
	id integer primary key autoincrement,
	nombre text not null,
	FOREING KEY (vendedor) REFERENCES vendedor(id),
	construccion float,
	terreno float,
	precio float,
	balance float,
	status integer
);
create table vendedor (
	id integer primary key autoincrement,
	nombre text not null,
	balance float
);
