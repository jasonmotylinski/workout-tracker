#!/usr/bin/env python
"""
CLI script to manage users - e.g., reset password
Usage:
    python manage_user.py reset-password <email> <new_password>
"""

import sys
from getpass import getpass
from app import create_app, db
from app.models.user import User

app = create_app()

def reset_password(email, password):
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if not user:
            print(f"❌ User '{email}' not found")
            return False

        from app import bcrypt
        user.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        db.session.commit()
        print(f"✓ Password updated for {email}")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python manage_user.py reset-password <email> [password]")
        print("  If password not provided, you'll be prompted for it")
        sys.exit(1)

    command = sys.argv[1]

    if command == "reset-password":
        if len(sys.argv) < 3:
            print("Usage: python manage_user.py reset-password <email> [password]")
            sys.exit(1)

        email = sys.argv[2]
        password = sys.argv[3] if len(sys.argv) > 3 else getpass("Enter new password: ")

        if not password:
            print("❌ Password cannot be empty")
            sys.exit(1)

        reset_password(email, password)
    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)
