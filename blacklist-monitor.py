import dns.resolver
import smtplib
from email.message import EmailMessage
import schedule
import time

def check_blacklist(domain):
    blacklist_servers = [
        "zen.spamhaus.org",
        "bl.spamcop.net",
        "dnsbl.sorbs.net"
    ]
    
    ip_address = dns.resolver.resolve(domain, 'A')[0].to_text()
    reversed_ip = '.'.join(reversed(ip_address.split('.')))
    
    for server in blacklist_servers:
        try:
            query = f"{reversed_ip}.{server}"
            dns.resolver.resolve(query, 'A')
            send_mail_alert(domain)
            return
        except dns.resolver.NoAnswer:
            continue
        except dns.resolver.NXDOMAIN:
            continue

    send_mail_ok(domain)

def send_mail_alert(domain):
    msg = EmailMessage()
    msg.set_content(f"Die Domain {domain} ist auf einer Blacklist.")
    msg['Subject'] = f"Achtung: {domain} ist auf der Blacklist!"
    msg['From'] = "your-alert-sender@example.com"
    msg['To'] = "your-recipient@example.com"
    send_mail(msg)

def send_mail_ok(domain):
    msg = EmailMessage()
    msg.set_content(f"Die Domain {domain} ist nicht auf einer Blacklist.")
    msg['Subject'] = f"OK: {domain} ist sauber."
    msg['From'] = "your-ok-sender@example.com"
    msg['To'] = "your-recipient@example.com"
    send_mail(msg)

def send_mail(msg):
    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login("your-smtp-username", "your-smtp-password")
    server.send_message(msg)
    server.quit()

# Domain zur Überprüfung
DOMAIN_TO_CHECK = "example.com"

# Starte erste Überprüfung
check_blacklist(DOMAIN_TO_CHECK)

# Plane wiederholte Überprüfung jede Stunde
schedule.every(1).hours.do(check_blacklist, DOMAIN_TO_CHECK)

while True:
    schedule.run_pending()
    time.sleep(1)
