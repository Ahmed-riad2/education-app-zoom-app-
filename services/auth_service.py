from database.db_manager import get_connection, hash_password

class AuthService:
    @staticmethod
    def authenticate_user(email, password):
        """Verifies credentials against the database and returns user data."""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, email, role FROM users WHERE email=? AND password_hash=?", 
                       (email, hash_password(password)))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "role": user[3]
            }
        return None