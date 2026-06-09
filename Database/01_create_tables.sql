-- ==========================================
-- NSL Daily Activity Log System
-- Version 1.0
-- ==========================================

--------------------------------------------------
-- USERS
--------------------------------------------------
SELECT* FROM USERS;
CREATE TABLE users (
    user_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    employee_code VARCHAR2(20) UNIQUE NOT NULL,

    full_name VARCHAR2(100) NOT NULL,

    role VARCHAR2(20) NOT NULL,

    department VARCHAR2(100),

    phone VARCHAR2(20),

    password_hash VARCHAR2(255),

    is_active CHAR(1) DEFAULT 'Y'
        CHECK (is_active IN ('Y','N')),

    created_at DATE DEFAULT SYSDATE
);

--------------------------------------------------
-- SERVICE CATEGORIES
--------------------------------------------------

CREATE TABLE service_categories (
    category_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    category_name VARCHAR2(200) NOT NULL,

    is_active CHAR(1) DEFAULT 'Y'
        CHECK (is_active IN ('Y','N'))
);

--------------------------------------------------
-- SERVICES
--------------------------------------------------

CREATE TABLE services (
    service_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    category_id NUMBER NOT NULL,

    service_name VARCHAR2(300) NOT NULL,

    is_active CHAR(1) DEFAULT 'Y'
        CHECK (is_active IN ('Y','N')),

    CONSTRAINT fk_service_category
        FOREIGN KEY(category_id)
        REFERENCES service_categories(category_id)
);

--------------------------------------------------
-- DAILY LOGS
--------------------------------------------------

CREATE TABLE daily_logs (

    log_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    user_id NUMBER NOT NULL,

    service_id NUMBER NOT NULL,

    log_date DATE NOT NULL,

    activity_description VARCHAR2(2000),

    start_time TIMESTAMP,

    end_time TIMESTAMP,

    outcome VARCHAR2(2000),

    remark VARCHAR2(1000),

    status VARCHAR2(20)
        DEFAULT 'DRAFT'
        CHECK (
            status IN (
                'DRAFT',
                'SUBMITTED',
                'APPROVED',
                'REJECTED'
            )
        ),

    created_at DATE DEFAULT SYSDATE,

    CONSTRAINT fk_daily_log_user
        FOREIGN KEY(user_id)
        REFERENCES users(user_id),

    CONSTRAINT fk_daily_log_service
        FOREIGN KEY(service_id)
        REFERENCES services(service_id)
);

--------------------------------------------------
-- APPROVALS
--------------------------------------------------

CREATE TABLE approvals (

    approval_id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    log_id NUMBER NOT NULL,

    approved_by NUMBER NOT NULL,

    approval_status VARCHAR2(20)
        CHECK (
            approval_status IN (
                'APPROVED',
                'REJECTED'
            )
        ),

    comments VARCHAR2(1000),

    approval_date DATE DEFAULT SYSDATE,

    CONSTRAINT fk_approval_log
        FOREIGN KEY(log_id)
        REFERENCES daily_logs(log_id),

    CONSTRAINT fk_approval_user
        FOREIGN KEY(approved_by)
        REFERENCES users(user_id)
);