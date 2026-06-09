from db.connection import get_connection
from utils.security import hash_password

conn = get_connection()
cursor = conn.cursor()

new_hash = hash_password("admin123")

cursor.execute("""
    UPDATE users
    SET password_hash = :1
    WHERE employee_code = 'ADMIN001'
""", [new_hash])

conn.commit()

print("Updated successfully")
print(new_hash)

cursor.close()
conn.close()