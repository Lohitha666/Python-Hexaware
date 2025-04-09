import sqlite3
from datetime import datetime
import configparser

# ====================== util/property_util.py ==========================
def get_property_string(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config['DEFAULT']['dbname']

# ====================== util/db_conn_util.py ===========================
def get_connection(property_file):
    db_name = get_property_string(property_file)
    return sqlite3.connect(db_name)

# ====================== entity/user.py ================================
class User:
    def __init__(self, user_id=None, username=None, password=None, role=None):
        self.__user_id = user_id
        self.__username = username
        self.__password = password
        self.__role = role

    def __str__(self):
        return f"User({self.__user_id}, {self.__username}, {self.__role})"

# ====================== entity/policy.py ==============================
class Policy:
    def __init__(self, policy_id=None, policy_name=None, policy_type=None, premium=None):
        self.policy_id = policy_id
        self.policy_name = policy_name
        self.policy_type = policy_type
        self.premium = premium

    def __str__(self):
        return f"Policy({self.policy_id}, {self.policy_name}, {self.policy_type}, {self.premium})"

# ====================== entity/client.py ==============================
class Client:
    def __init__(self, client_id=None, client_name=None, contact_info=None, policy_id=None):
        self.client_id = client_id
        self.client_name = client_name
        self.contact_info = contact_info
        self.policy_id = policy_id

    def __str__(self):
        return f"Client({self.client_id}, {self.client_name}, {self.contact_info}, {self.policy_id})"

# ====================== entity/claim.py ===============================
class Claim:
    def __init__(self, claim_id=None, claim_number=None, date_filed=None, claim_amount=None, status=None, policy_id=None, client_id=None):
        self.claim_id = claim_id
        self.claim_number = claim_number
        self.date_filed = date_filed
        self.claim_amount = claim_amount
        self.status = status
        self.policy_id = policy_id
        self.client_id = client_id

    def __str__(self):
        return f"Claim({self.claim_id}, {self.claim_number}, {self.status})"

# ====================== entity/payment.py =============================
class Payment:
    def __init__(self, payment_id=None, payment_date=None, payment_amount=None, client_id=None):
        self.payment_id = payment_id
        self.payment_date = payment_date
        self.payment_amount = payment_amount
        self.client_id = client_id

    def __str__(self):
        return f"Payment({self.payment_id}, {self.payment_date}, {self.payment_amount})"

# ====================== exception/policy_not_found_exception.py =======
class PolicyNotFoundException(Exception):
    def __init__(self, message="Policy not found!"):
        super().__init__(message)

# ====================== dao/ipolicy_service.py ========================
class IPolicyService:
    def create_policy(self, policy): pass
    def get_policy(self, policy_id): pass
    def get_all_policies(self): pass
    def update_policy(self, policy): pass
    def delete_policy(self, policy_id): pass

# ====================== dao/insurance_service_impl.py ================
class InsuranceServiceImpl(IPolicyService):
    def __init__(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def create_policy(self, policy):
        try:
            self.cursor.execute("INSERT INTO policy (policy_id, policy_name, policy_type, premium) VALUES (?, ?, ?, ?)",
                                (policy.policy_id, policy.policy_name, policy.policy_type, policy.premium))
            self.conn.commit()
            return True
        except Exception as e:
            print("Error creating policy:", e)
            return False

    def get_policy(self, policy_id):
        self.cursor.execute("SELECT * FROM policy WHERE policy_id = ?", (policy_id,))
        row = self.cursor.fetchone()
        if row:
            return Policy(*row)
        else:
            raise PolicyNotFoundException()

    def get_all_policies(self):
        self.cursor.execute("SELECT * FROM policy")
        return [Policy(*row) for row in self.cursor.fetchall()]

    def update_policy(self, policy):
        self.cursor.execute("UPDATE policy SET policy_name=?, policy_type=?, premium=? WHERE policy_id=?",
                            (policy.policy_name, policy.policy_type, policy.premium, policy.policy_id))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def delete_policy(self, policy_id):
        self.cursor.execute("DELETE FROM policy WHERE policy_id=?", (policy_id,))
        self.conn.commit()
        return self.cursor.rowcount > 0

# ====================== create_tables.py ==============================
def create_tables():
    conn = get_connection('resources/db.properties')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS policy (
        policy_id INTEGER PRIMARY KEY,
        policy_name TEXT,
        policy_type TEXT,
        premium REAL
    )''')
    conn.commit()
    conn.close()

# ====================== mainmod/main_module.py ========================
def main():
    from util.db_conn_util import get_connection
    from dao.insurance_service_impl import InsuranceServiceImpl
    from entity.policy import Policy
    from exception.policy_not_found_exception import PolicyNotFoundException

    conn = get_connection('resources/db.properties')
    service = InsuranceServiceImpl(conn)

    while True:
        print("\nInsurance Management System")
        print("1. Add Policy\n2. View Policy\n3. View All Policies\n4. Update Policy\n5. Delete Policy\n6. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            policy = Policy(int(input("ID: ")), input("Name: "), input("Type: "), float(input("Premium: ")))
            print("Added!" if service.create_policy(policy) else "Failed!")

        elif choice == '2':
            try:
                policy = service.get_policy(int(input("Enter Policy ID: ")))
                print(policy)
            except PolicyNotFoundException as e:
                print(e)

        elif choice == '3':
            for p in service.get_all_policies():
                print(p)

        elif choice == '4':
            policy = Policy(int(input("ID: ")), input("Name: "), input("Type: "), float(input("Premium: ")))
            print("Updated!" if service.update_policy(policy) else "Failed!")

        elif choice == '5':
            print("Deleted!" if service.delete_policy(int(input("ID: "))) else "Failed!")

        elif choice == '6':
            break
        else:
            print("Invalid choice")

if __name__ == '__main__':
    create_tables()
    main()
