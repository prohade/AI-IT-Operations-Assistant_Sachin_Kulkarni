from datetime import datetime, timedelta, timezone
from .database import initialize_database, get_connection

def seed_database():
    initialize_database()
    now = datetime.now(timezone.utc)
    with get_connection() as conn:
        conn.execute("DELETE FROM tickets")
        conn.execute("DELETE FROM knowledge_articles")
        conn.execute("DELETE FROM employees")
        employees = [
            ("EMP1001","Amit Sharma","Finance","amit.sharma@example.com","Finance Analyst","Active"),
            ("EMP1024","Sachin Kulkarni","IT","sachin.kulkarni@example.com","IT Manager","Active"),
            ("EMP1030","Priya Patel","HR","priya.patel@example.com","HR Executive","Active"),
            ("EMP1045","Rahul Mehta","Sales","rahul.mehta@example.com","Sales Executive","Active"),
            ("EMP1052","Neha Joshi","Operations","neha.joshi@example.com","Operations Analyst","Active"),
        ]
        conn.executemany("INSERT INTO employees VALUES (?,?,?,?,?,?)", employees)
        articles = [
            ("VPN","Reset VPN Password","Open the corporate password portal, sign in, choose Change Password, and complete MFA verification.","vpn,password,reset,mfa"),
            ("VPN","VPN Connection Troubleshooting","Check internet connectivity, restart the VPN client, confirm the corporate VPN profile, and retry MFA.","vpn,connection,troubleshooting,remote access"),
            ("Laptop","Laptop Performance Troubleshooting","Restart the laptop, close unnecessary applications, check disk space, and install pending updates.","laptop,slow,performance,freeze"),
            ("Email","Outlook Not Syncing","Check network connectivity, restart Outlook, and verify Outlook is not in Offline mode.","outlook,email,sync,mail"),
        ]
        conn.executemany("INSERT INTO knowledge_articles (category,title,content,keywords) VALUES (?,?,?,?)", articles)
        tickets = [
            ("INC10001","EMP1024","VPN","VPN disconnects frequently","VPN disconnects every 10 to 15 minutes.","Medium","In Progress","Network Support",(now-timedelta(days=1)).isoformat()),
            ("INC10002","EMP1024","Laptop","Laptop running slowly","Laptop becomes slow after several hours.","Low","Resolved","Desktop Support",(now-timedelta(days=8)).isoformat()),
            ("INC10003","EMP1001","Email","Outlook not syncing","Outlook is not synchronizing new messages.","Medium","Open","Messaging Support",(now-timedelta(hours=6)).isoformat()),
        ]
        conn.executemany("INSERT INTO tickets (ticket_id,employee_id,category,subject,description,priority,status,assigned_to,created_at) VALUES (?,?,?,?,?,?,?,?,?)", tickets)
        conn.commit()

if __name__ == "__main__":
    seed_database()
    print("Database seeded successfully.")
