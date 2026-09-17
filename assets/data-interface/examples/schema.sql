-- Standard SQLite teaching template. No business records.
PRAGMA foreign_keys=ON;
CREATE TABLE capacity (
	id INTEGER NOT NULL,
	time_unit INTEGER NOT NULL,
	used FLOAT NOT NULL,
	workcenter INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(time_unit) REFERENCES time_unit (id),
	FOREIGN KEY(workcenter) REFERENCES workcenter (id)
);

CREATE TABLE ingredient (
	id INTEGER NOT NULL,
	process INTEGER NOT NULL,
	material INTEGER NOT NULL,
	number INTEGER NOT NULL,
	priority INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(process) REFERENCES process (id),
	FOREIGN KEY(material) REFERENCES material (id)
);

CREATE TABLE inventory_limit (
	id INTEGER NOT NULL,
	product INTEGER NOT NULL,
	time_unit INTEGER NOT NULL,
	binding INTEGER,
	upper_bound_acc INTEGER,
	urgency FLOAT NOT NULL, lower_bound_acc INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(product) REFERENCES product (id),
	FOREIGN KEY(time_unit) REFERENCES time_unit (id)
);

CREATE TABLE kitting_information (
	id INTEGER NOT NULL,
	time_unit INTEGER NOT NULL,
	material INTEGER NOT NULL,
	number INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(time_unit) REFERENCES time_unit (id),
	FOREIGN KEY(material) REFERENCES material (id)
);

CREATE TABLE material (
	id INTEGER NOT NULL,
	code VARCHAR NOT NULL,
	name VARCHAR NOT NULL,
	vendor VARCHAR NOT NULL,
	substitute INTEGER,
	binding INTEGER,
	extend INTEGER,
	PRIMARY KEY (id)
);

CREATE TABLE order_info (
	id INTEGER NOT NULL,
	description VARCHAR NOT NULL,
	priority INTEGER NOT NULL,
	code VARCHAR,
	created_at DATETIME,
	PRIMARY KEY (id)
);

CREATE TABLE order_item (
	id INTEGER NOT NULL,
	product INTEGER NOT NULL,
	information INTEGER NOT NULL,
	delivery_time INTEGER,
	number INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(product) REFERENCES product (id),
	FOREIGN KEY(information) REFERENCES order_info (id),
	FOREIGN KEY(delivery_time) REFERENCES time_unit (id)
);

CREATE TABLE planning_result (
	id INTEGER NOT NULL,
	workcenter INTEGER,
	time_unit INTEGER NOT NULL,
	process INTEGER,
	number INTEGER NOT NULL,
	value_1 INTEGER NOT NULL,
	value_2 INTEGER NOT NULL,
	value_3 INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(workcenter) REFERENCES workcenter (id),
	FOREIGN KEY(time_unit) REFERENCES time_unit (id),
	FOREIGN KEY(process) REFERENCES process (id)
);

CREATE TABLE process (
	id INTEGER NOT NULL,
	route INTEGER NOT NULL,
	name VARCHAR NOT NULL,
	code VARCHAR,
	operation_number INTEGER NOT NULL,
	seqno INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY(route) REFERENCES process_route (id)
);

CREATE TABLE process_adaptor (
	id INTEGER NOT NULL,
	process INTEGER,
	workcenter INTEGER,
	priority INTEGER NOT NULL,
	wip_buffer_size INTEGER NOT NULL,
	productivity INTEGER NOT NULL,
	processing_time FLOAT NOT NULL,
	setup_time FLOAT NOT NULL,
	batch_size INTEGER NOT NULL,
	"OEE" INTEGER NOT NULL,
	binding INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(process) REFERENCES process (id),
	FOREIGN KEY(workcenter) REFERENCES workcenter (id)
);

CREATE TABLE process_route (
	id INTEGER NOT NULL,
	product INTEGER NOT NULL,
	name VARCHAR NOT NULL,
	code VARCHAR NOT NULL,
	priority INTEGER NOT NULL,
	description VARCHAR,
	PRIMARY KEY (id),
	FOREIGN KEY(product) REFERENCES product (id)
);

CREATE TABLE product (
	id INTEGER NOT NULL,
	name VARCHAR NOT NULL,
	code VARCHAR NOT NULL,
	vin VARCHAR,
	property_1 INTEGER,
	property_2 INTEGER,
	property_3 INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(property_1) REFERENCES property_1 (id),
	FOREIGN KEY(property_2) REFERENCES property_2 (id),
	FOREIGN KEY(property_3) REFERENCES property_3 (id)
);

CREATE TABLE property_1 (
	id INTEGER NOT NULL,
	name VARCHAR NOT NULL,
	code VARCHAR,
	value FLOAT,
	is_key BOOLEAN NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE property_2 (
	id INTEGER NOT NULL,
	name VARCHAR NOT NULL,
	code VARCHAR,
	value FLOAT,
	is_key BOOLEAN NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE property_3 (
	id INTEGER NOT NULL,
	name VARCHAR NOT NULL,
	code VARCHAR,
	value FLOAT,
	is_key BOOLEAN NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE shared_resource (
	id INTEGER NOT NULL,
	binding INTEGER,
	"to" INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(binding) REFERENCES workcenter (id),
	FOREIGN KEY("to") REFERENCES workcenter (id)
);

CREATE TABLE time_unit (
	id INTEGER NOT NULL,
	"offset" INTEGER NOT NULL,
	scale INTEGER NOT NULL,
	status INTEGER NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE workcenter (
	id INTEGER NOT NULL,
	name VARCHAR NOT NULL,
	code VARCHAR,
	type INTEGER NOT NULL,
	parallelism INTEGER NOT NULL,
	station_count INTEGER NOT NULL,
	equipping_time FLOAT NOT NULL,
	parent_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(parent_id) REFERENCES workcenter (id)
);