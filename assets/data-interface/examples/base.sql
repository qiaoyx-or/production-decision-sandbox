PRAGMA foreign_keys=ON;

INSERT INTO time_unit (id, offset, scale, status) VALUES
  (1, 0, 28800, 1), (2, 1, 28800, 1);
INSERT INTO property_1 (id, name, code, value, is_key) VALUES
  (1, 'Color', 'BLUE', 1, 1);
INSERT INTO product (id, name, code, vin, property_1, property_2, property_3) VALUES
  (1, 'Blue bracket', 'P-1', 'FIN-P1', 1, NULL, NULL);
INSERT INTO workcenter (id, name, code, type, parallelism, station_count, equipping_time, parent_id) VALUES
  (10, 'Shop', 'SHOP', 1, 1, 1, 0, NULL),
  (11, 'Stamping A', 'PRESS-A', 0, 1, 1, 0, 10),
  (12, 'Assembly', 'ASSEMBLY', 0, 1, 1, 0, 10);
INSERT INTO order_info (id, description, priority, code, created_at) VALUES
  (1, 'Staged bracket delivery', 0, 'O-100', NULL);
INSERT INTO order_item (id, product, information, delivery_time, number) VALUES
  (1, 1, 1, 1, 80), (2, 1, 1, 2, 40);
INSERT INTO process_route (id, product, name, code, priority, description) VALUES
  (101, 1, 'Stamp then assemble', 'ROUTE-P1', 0, 'Teaching route');
INSERT INTO process (id, route, name, code, operation_number, seqno) VALUES
  (1001, 101, 'Stamping', 'STAMP', 10, 1),
  (1002, 101, 'Assembly', 'ASSEMBLE', 20, 2);
INSERT INTO process_adaptor (id, process, workcenter, priority, wip_buffer_size, productivity, processing_time, setup_time, batch_size, OEE, binding) VALUES
  (1, 1001, 11, 0, 120, 4, 600, 0, 20, 100, NULL),
  (2, 1002, 12, 0, 120, 1, 120, 0, 20, 100, NULL);
INSERT INTO material (id, code, name, vendor, substitute, binding, extend) VALUES
  (1, 'BLANK', 'Blank', 'SUPPLIER-1', NULL, NULL, NULL),
  (2, 'FASTENER', 'Fastener', 'SUPPLIER-2', NULL, NULL, NULL);
INSERT INTO ingredient (id, process, material, number, priority) VALUES
  (1, 1001, 1, 1, 0), (2, 1002, 2, 2, 0);
INSERT INTO kitting_information (id, time_unit, material, number) VALUES
  (1, 1, 1, 80), (2, 1, 2, 160), (3, 2, 1, 40), (4, 2, 2, 80);
INSERT INTO capacity (id, time_unit, used, workcenter) VALUES
  (1, 1, 0.25, 11), (2, 1, 0, 12), (3, 2, 0, 11), (4, 2, 0, 12);
INSERT INTO inventory_limit (id, product, time_unit, binding, upper_bound_acc, lower_bound_acc, urgency) VALUES
  (1, 1, 1, NULL, 160, 80, 0), (2, 1, 2, NULL, 200, 120, 0);
-- planning_result deliberately stays empty. Candidate rows are a separate teaching CSV.
