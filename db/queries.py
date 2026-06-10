import pandas as pd
import streamlit as st
from db.connection import get_connection
from utils.security import hash_password, verify_password

def authenticate_user(employee_code, password):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            user_id,
            full_name,
            role,
            password_hash
        FROM users
        WHERE employee_code = :1
        AND is_active = 'Y'
    """, [employee_code])

    user = cursor.fetchone()

    print("USER =", user)

    cursor.close()
    connection.close()

    if not user:
        print("User not found")
        return None

    print("Stored Hash =", user[3])

    result = verify_password(
        password,
        user[3]
    )

    print("Password Match =", result)

    if result:
        return (
            user[0],
            user[1],
            user[2]
        )

    return None

def get_categories():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            category_id,
            category_name
        FROM service_categories
        WHERE is_active = 'Y'
        ORDER BY category_name
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
def get_services(category_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            service_id,
            service_name
        FROM services
        WHERE category_id = :1
        AND is_active = 'Y'
        ORDER BY service_name
    """, [category_id])

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def create_audit_log(
        user_id,
        action_type,
        details):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO audit_logs(
            user_id,
            action_type,
            details
        )
        VALUES(
            :1,
            :2,
            :3
        )
    """, [
        user_id,
        action_type,
        details
    ])

    conn.commit()

    cursor.close()
    conn.close()
def get_dashboard_counts(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) total_logs,

            SUM(
                CASE
                    WHEN status = 'DRAFT'
                    THEN 1
                    ELSE 0
                END
            ) draft_logs,

            SUM(
                CASE
                    WHEN status = 'SUBMITTED'
                    THEN 1
                    ELSE 0
                END
            ) submitted_logs,

            SUM(
                CASE
                    WHEN status = 'APPROVED'
                    THEN 1
                    ELSE 0
                END
            ) approved_logs

        FROM daily_logs
        WHERE user_id = :1
    """, [user_id])

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row
def get_log_statistics(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            status,
            COUNT(*)
        FROM daily_logs
        WHERE user_id = :1
        GROUP BY status
    """, [user_id])

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
def get_recent_logs(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            d.log_date,
            s.service_name,
            d.status
        FROM daily_logs d
        JOIN services s
            ON d.service_id = s.service_id
        WHERE d.user_id = :1
        ORDER BY d.log_id DESC
        FETCH FIRST 10 ROWS ONLY
    """, [user_id])

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def get_submitted_logs():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            d.log_id,
            u.full_name,
            s.service_name,
            d.log_date,
            d.activity_description,
            d.activity_location,
            d.status
        FROM daily_logs d
        JOIN users u
            ON d.user_id = u.user_id
        JOIN services s
            ON d.service_id = s.service_id
        WHERE d.status = 'SUBMITTED'
        ORDER BY d.log_date DESC
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def approve_log(
        log_id,
        supervisor_id,
        comments):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE daily_logs
        SET status = 'APPROVED'
        WHERE log_id = :1
    """, [log_id])

    cursor.execute("""
        INSERT INTO approvals(
            log_id,
            approved_by,
            approval_status,
            comments
        )
        VALUES(
            :1,
            :2,
            'APPROVED',
            :3
        )
    """, [
        log_id,
        supervisor_id,
        comments
    ])

    conn.commit()

    cursor.close()
    conn.close()

    create_audit_log(
    supervisor_id,
        "APPROVE_LOG",
        f"Approved log ID {log_id}"
    )

def reject_log(
        log_id,
        supervisor_id,
        comments):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE daily_logs
        SET status = 'REJECTED'
        WHERE log_id = :1
    """, [log_id])

    cursor.execute("""
        INSERT INTO approvals(
            log_id,
            approved_by,
            approval_status,
            comments
        )
        VALUES(
            :1,
            :2,
            'REJECTED',
            :3
        )
    """, [
        log_id,
        supervisor_id,
        comments
    ])

    conn.commit()

    cursor.close()
    conn.close()
    
    create_audit_log(
        supervisor_id,
        "REJECT_LOG",
        f"Rejected log ID {log_id}"
    )

def get_daily_report(report_date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            u.full_name,
            c.category_name,
            s.service_name,
            d.activity_location,
            d.activity_description,
            d.status
        FROM daily_logs d
        JOIN users u
            ON d.user_id = u.user_id
        JOIN services s
            ON d.service_id = s.service_id
        JOIN service_categories c
            ON s.category_id = c.category_id
        WHERE TRUNC(d.log_date) = :1
        ORDER BY u.full_name
    """, [report_date])

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
def get_user_logs(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            d.log_id,
            d.log_date,
            s.service_name,
            d.activity_location,
            d.status
        FROM daily_logs d
        JOIN services s
            ON d.service_id = s.service_id
        WHERE d.user_id = :1
        ORDER BY d.log_date DESC
    """, [user_id])

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
def get_employee_performance():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            u.full_name,
            COUNT(*) total_logs
        FROM daily_logs d
        JOIN users u
            ON d.user_id = u.user_id
        GROUP BY u.full_name
        ORDER BY total_logs DESC
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
def get_user_logs(
        user_id,
        status=None):

    conn = get_connection()

    cursor = conn.cursor()

    sql = """
        SELECT
            d.log_id,
            d.log_date,
            s.service_name,
            d.activity_location,
            d.status
        FROM daily_logs d
        JOIN services s
            ON d.service_id = s.service_id
        WHERE d.user_id = :1
    """

    params = [user_id]

    if status and status != "ALL":

        sql += """
            AND d.status = :2
        """

        params.append(status)

    sql += """
        ORDER BY d.log_date DESC,
                 d.log_id DESC
    """

    cursor.execute(sql, params)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
def create_daily_log(
        user_id,
        log_date,
        service_id,
        activity_location,
        activity_description,
        start_time,
        end_time,
        duration_minutes,
        outcome,
        remark,
        status):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO daily_logs(
            user_id,
            log_date,
            service_id,
            activity_location,
            activity_description,
            start_time,
            end_time,
            duration_minutes,
            outcome,
            remark,
            status
        )
        VALUES(
            :1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11
        )
    """, [
        user_id,
        log_date,
        service_id,
        activity_location,
        activity_description,
        start_time,
        end_time,
        duration_minutes,
        outcome,
        remark,
        status
    ])

    conn.commit()

    cursor.close()
    conn.close()

    create_audit_log(
        user_id,
        "CREATE_LOG",
        f"Created {status} daily log"
    )
def create_user(
        employee_code,
        full_name,
        role,
        department,
        password,
        created_by):

    hashed_password = hash_password(password)

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users(
            employee_code,
            full_name,
            role,
            department,
            password_hash
        )
        VALUES(
            :1,:2,:3,:4,:5
        )
    """, [
        employee_code,
        full_name,
        role,
        department,
        hashed_password
    ])

    conn.commit()

    cursor.close()
    conn.close()

    create_audit_log(
        created_by,
        "CREATE_USER",
        f"Created user {employee_code}"
    )
def get_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            user_id,
            employee_code,
            full_name,
            role,
            department,
            is_active
        FROM users
        ORDER BY full_name
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def get_user(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            user_id,
            employee_code,
            full_name,
            role,
            department,
            is_active
        FROM users
        WHERE user_id = :1
    """, [user_id])

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row
def get_log_by_id(log_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            log_id,
            log_date,
            service_id,
            activity_location,
            activity_description,
            start_time,
            end_time,
            duration_minutes,
            outcome,
            remark,
            status
        FROM daily_logs
        WHERE log_id = :1
    """, [log_id])

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row    

def update_daily_log(
        
        log_id,
        service_id,
        activity_location,
        activity_description,
        start_time,
        end_time,
        duration_minutes,
        outcome,
        remark):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE daily_logs
        SET
            service_id = :1,
            activity_location = :2,
            activity_description = :3,
            start_time = :4,
            end_time = :5,
            duration_minutes = :6,
            outcome = :7,
            remark = :8
        WHERE log_id = :9
    """, [
        service_id,
        activity_location,
        activity_description,
        start_time,
        end_time,
        duration_minutes,
        outcome,
        remark,
        log_id
    ])

    conn.commit()

    cursor.close()
    conn.close()
def delete_daily_log(
        
        log_id,
        user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM daily_logs
        WHERE log_id = :1
    """, [log_id])

    conn.commit()

    cursor.close()
    conn.close()

    create_audit_log(
        user_id,
        "DELETE_LOG",
        f"Deleted log ID {log_id}"
    )
def get_approval_comments(log_id):
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            approval_status,
            comments,
            approval_date
        FROM approvals
        WHERE log_id = :1
        ORDER BY approval_id DESC
    """, [log_id])

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row

def get_log_statistics(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            status,
            COUNT(*)
        FROM daily_logs
        WHERE user_id = :1
        GROUP BY status
    """, [user_id])

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def get_monthly_summary(month, year):


    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            u.full_name,
            COUNT(*) total_logs
        FROM daily_logs d
        JOIN users u
            ON d.user_id = u.user_id
        WHERE EXTRACT(MONTH FROM d.log_date)=:1
        AND EXTRACT(YEAR FROM d.log_date)=:2
        GROUP BY u.full_name
        ORDER BY total_logs DESC
    """, [month, year])

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def get_supervisor_dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            (SELECT COUNT(*)
             FROM daily_logs
             WHERE status='SUBMITTED'),

            (SELECT COUNT(*)
             FROM daily_logs
             WHERE status='APPROVED'),

            (SELECT COUNT(*)
             FROM daily_logs
             WHERE status='REJECTED'),

            (SELECT COUNT(*)
             FROM users
             WHERE role='EMPLOYEE')
        FROM dual
    """)

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row

def get_top_employees():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            u.full_name,
            COUNT(*) total_logs
        FROM daily_logs d
        JOIN users u
            ON d.user_id = u.user_id
        GROUP BY u.full_name
        ORDER BY total_logs DESC
        FETCH FIRST 10 ROWS ONLY
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def get_status_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            status,
            COUNT(*)
        FROM daily_logs
        GROUP BY status
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def change_password(
        
        user_id,
        new_password_hash):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET password_hash = :1
        WHERE user_id = :2
    """, [
        new_password_hash,
        user_id
    ])

    conn.commit()

    cursor.close()
    conn.close()

    create_audit_log(
        user_id,
        "CHANGE_PASSWORD",
        "User changed password"
    )

def get_password_hash(user_id):
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT password_hash
        FROM users
        WHERE user_id = :1
    """, [user_id])

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row[0]
def get_user_profile(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            employee_code,
            full_name,
            role,
            department,
            is_active,
            created_at,
            last_login,
            phone
        FROM users
        WHERE user_id = :1
    """, [user_id])

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row
def update_last_login(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET last_login = SYSDATE
        WHERE user_id = :1
    """, [user_id])

    conn.commit()

    cursor.close()
    conn.close()

def get_login_history(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            action_date,
            details
        FROM audit_logs
        WHERE user_id = :1
        AND action_type = 'LOGIN'
        ORDER BY action_date DESC
    """, [user_id])

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def get_audit_logs():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            a.action_date,
            u.full_name,
            a.action_type,
            a.details
        FROM audit_logs a
        JOIN users u
            ON a.user_id = u.user_id
        ORDER BY a.action_date DESC
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows

def save_attachment(
        log_id,
        file_name,
        file_path):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO log_attachments(
            log_id,
            file_name,
            file_path
        )
        VALUES(
            :1,:2,:3
        )
    """, [
        log_id,
        file_name,
        file_path
    ])

    conn.commit()

    cursor.close()
    conn.close()