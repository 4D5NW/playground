#!/usr/bin/env python3
import os, json, hashlib, requests, feedparser

MM_WEBHOOK_URL = os.environ["MM_WEBHOOK_URL"]
FEEDS = [
#    "https://www.cisa.gov/news.xml",
#    "https://www.ncsc.gov.uk/alerts.xml",
#    "https://www.kb.cert.org/vuls/rss/rss_feed.xml",
#    "https://www.cert.ssi.gouv.fr/actualite/feed/",
#    "https://www.bsi.bund.de/SiteGlobals/Functions/RSSFeed/DE/RSSNewsfeed/RSSNews.xml",
    "https://rss.golem.de/rss.php?feed=RSS1.0&ms=security",
    "https://tarnkappe.info/artikel/it-sicherheit/feed/",
    "https://www.heise.de/security/rss/news-atom.xml"
]
KEYWORDS = [
    # Allgemein / Schwachstellen
    "cve","vulnerability","vulnerabilities","exploit","exploited","zeroday","zero-day","0day","lpe","dos","csrf","xss","ssrf",
    "sql injection","sqli","directory traversal","rce","remote code execution","privilege escalation","bypass",
    "escalation","misconfiguration","security flaw","security issue","patch","update","fix","security update",
    "sicherheitslücke","sicherheitsupdate","schwachstelle","lücke","notfallpatch","aktualisierung","update verfügbar",

    # Angriffe / Kampagnen / Bedrohungen
    "ransomware","malware","spyware","trojan","trojaner","infostealer","stealer","backdoor","botnet","rootkit","worm",
    "phishing","smishing","vishing","social engineering","credential stuffing","bruteforce","brute force",
    "session hijacking","ddos","exfiltration","data leak","datenleck","datendiebstahl","data theft","breach","compromise",
    "hack","hacked","hacking","hacker","attack","angriff","cyberangriff","intrusion","unauthorized access",
    "erpressung","erpressersoftware","scam","betrug","spoofing","fake","fraud","online fraud","cyberangriff","identity theft","identitätsdiebstahl",

    # Hersteller & Produkte (Security / Infrastruktur)
    "microsoft","windows","exchange","office","azure","aws","amazon","google cloud","gcp","cloudflare","okta","auth0",
    "github","gitlab","atlassian","jira","confluence","oracle","sap","adobe","vmware","palo alto","fortinet","fortigate",
    "cisco","juniper","checkpoint","check point","sophos","trend micro","kaspersky","eset","crowdstrike","sentinelone",
    "tenable","nessus","rapid7","qualys","elastic","splunk","darktrace","mcafee","symantec","broadcom","carbon black",
    "proofpoint","barracuda","sonicwall","watchguard","f5","bigip","citrix","netapp","qnap","synology","lenovo",
    "dell","hp","intel","amd","supermicro","huawei","zte","aruba","ubiquiti","mariadb","mysql","postgres","nginx","apache",
    "tomcat","grafana","kibana","elasticsearch","prometheus","jenkins","docker","kubernetes","proxmox",

    # Threat Actor / Malware-Familien / APTs
    "apt","advanced persistent threat","lazarus","sandworm","fin7","conti","lockbit","blackcat","black basta","clop",
    "revil","darkside","alphv","ragnar","babuk","royal","cactus","qakbot","emotet","trickbot","icedid","smokeloader",
    "raccoon","redline","agent tesla","formbook","metasploit","cobalt strike","c2","command and control",

    # Cloud / Plattform / SaaS / Dienste
    "office 365","one drive","teams","sharepoint","google workspace","slack","zoom","dropbox","salesforce","zendesk",
    "okta","auth0","aws","ec2","s3","iam","azure ad","cloudflare","fastly","cdn","github","gitlab","bitbucket","jira",
    "atlassian","confluence","jenkins","git","docker","kubernetes","proxmox","harbor","rundeck","ansible","terraform",
    "grafana","prometheus","elastic","elasticsearch","kibana","splunk",

    # Industrial / IoT / OT
    "scada","ics","plc","siemens","abb","schneider","honeywell","industrial control","ot","iot","router","firmware",
    "netzwerk","firewall","vpn","ssl","tls","certificate","auth","ldap","radius","openvpn","wireguard",

    # Themen / Konzepte / Tools
    "cyberattack","cybersecurity","information security","infosec","incident","forensics","threat","threat intel","threat hunting",
    "soc","siem","mitre","tactic","technique","procedure","ttp","payload","ransom note","phishing mail","payload",
    "exploit kit","poc","proof of concept","exploit released","vulnerability disclosure","security advisory",
    "security bulletin","advisory","cisa","bsi","ncsc","cert-bund","us-cert","auscert","govcert","warnung","meldung",
    "it-sicherheit","cyber","datenschutz","datensicherheit","meldung sicherheit","sicherheitswarnung","warnmeldung"
]


STATE = "/var/tmp/mm_news_state.json"

def seen_load():
    try:
        return set(json.load(open(STATE))["seen"])
    except:
        return set()

def seen_save(s):
    tmp = STATE + ".tmp"
    json.dump({"seen": list(s)}, open(tmp,"w"))
    os.replace(tmp, STATE)

def iid(e):
    src = e.get("id") or e.get("link") or e.get("title","")
    return hashlib.sha256(src.encode()).hexdigest()

def post(text):
    requests.post(MM_WEBHOOK_URL, json={"text": text}, timeout=15).raise_for_status()

def run_once():
    seen = seen_load()
    for url in FEEDS:
        d = feedparser.parse(url)
        for e in d.entries[:30]:
            h = iid(e)
            if h in seen:
                continue
            title = e.get("title","")
            summary = e.get("summary","")
            link = e.get("link","")
            if not any(k in (title+" "+summary).lower() for k in KEYWORDS):
                continue
            post(f"**{title}**\nQuelle: {d.feed.get('title',url)}\n{link}")
            seen.add(h)
    seen_save(seen)

if __name__ == "__main__":
    import time
    while True:
        run_once()
        time.sleep(600)  # 600 Sekunden = 10 Minuten
