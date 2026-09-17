-- Apply only to a fresh base.sql teaching database.
PRAGMA foreign_keys=ON;
BEGIN;
INSERT INTO time_unit (id,offset,scale,status) VALUES (3,2,28800,1);
UPDATE order_item SET delivery_time=3 WHERE id=2;
INSERT INTO capacity (id,time_unit,used,workcenter) VALUES (5,3,0,11),(6,3,0,12);
-- With issues [80,0,40] and opening stock 20, retain inventory in [20,100].
UPDATE inventory_limit SET lower_bound_acc=80,upper_bound_acc=160 WHERE time_unit=2;
INSERT INTO inventory_limit (id,product,time_unit,binding,upper_bound_acc,lower_bound_acc,urgency)
VALUES (3,1,3,NULL,200,120,0);
-- Period 2 arrivals are retained; zero in period 3 is an increment, not cumulative supply.
INSERT INTO kitting_information (id,time_unit,material,number) VALUES (5,3,1,0),(6,3,2,0);
COMMIT;
