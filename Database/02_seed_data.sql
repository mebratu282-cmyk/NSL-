INSERT INTO service_categories(category_name)
VALUES ('Certification');

INSERT INTO service_categories(category_name)
VALUES ('Inspection');

INSERT INTO service_categories(category_name)
VALUES ('Reporting');

INSERT INTO service_categories(category_name)
VALUES ('Complaint Handling');

INSERT INTO services(category_id, service_name)
VALUES (1, 'Food Service Provider Certification');

INSERT INTO services(category_id, service_name)
VALUES (1, 'Food Manufacturing Certification');

INSERT INTO services(category_id, service_name)
VALUES (1, 'Warehouse Certification');

INSERT INTO services(category_id, service_name)
VALUES (2, 'Routine Inspection');

INSERT INTO services(category_id, service_name)
VALUES (2, 'Follow-up Inspection');

INSERT INTO services(category_id, service_name)
VALUES (2, 'Special Inspection');

INSERT INTO services(category_id, service_name)
VALUES (3, 'Daily Report');

INSERT INTO services(category_id, service_name)
VALUES (3, 'Weekly Report');

INSERT INTO services(category_id, service_name)
VALUES (3, 'Monthly Report');

INSERT INTO services(category_id, service_name)
VALUES (4, 'Complaint Registration');

INSERT INTO services(category_id, service_name)
VALUES (4, 'Complaint Investigation');

INSERT INTO users (
    employee_code,
    full_name,
    role,
    department
)
VALUES (
    'EMP001',
    'Darmyelesh Hailu',
    'EMPLOYEE',
    'Cluster One'
);

INSERT INTO users (
    employee_code,
    full_name,
    role,
    department
)
VALUES (
    'EMP002',
    'Employee Two',
    'EMPLOYEE',
    'Cluster One'
);

INSERT INTO users (
    employee_code,
    full_name,
    role,
    department
)
VALUES (
    'EMP003',
    'Employee Three',
    'EMPLOYEE',
    'Cluster One'
);

INSERT INTO users (
    employee_code,
    full_name,
    role,
    department
)
VALUES (
    'EMP004',
    'Employee Four',
    'EMPLOYEE',
    'Cluster One'
);

INSERT INTO users (
    employee_code,
    full_name,
    role,
    department
)
VALUES (
    'SUP001',
    'Supervisor One',
    'SUPERVISOR',
    'Cluster One'
);

UPDATE users
SET password_hash = '1234'
WHERE employee_code = 'EMP001';

UPDATE users
SET password_hash = '1234'
WHERE employee_code = 'EMP002';

UPDATE users
SET password_hash = '1234'
WHERE employee_code = 'EMP003';

UPDATE users
SET password_hash = '1234'
WHERE employee_code = 'EMP004';

UPDATE users
SET password_hash = 'admin123'
WHERE employee_code = 'SUP001';



ALTER TABLE daily_logs
ADD activity_location VARCHAR2(300);

ALTER TABLE daily_logs
ADD duration_minutes NUMBER;

ALTER TABLE users
ADD last_login DATE;
COMMIT;


COMMIT;
SELECT * FROM USERS;