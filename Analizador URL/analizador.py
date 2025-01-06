import webbrowser
from urllib.parse import quote


# Función para limpiar la URL
def limpiar_url(url):
    url = url.strip()
    if url.startswith("http://"):
        url = url[7:]
    elif url.startswith("https://"):
        url = url[8:]
    if url.startswith("www."):
        url = url[4:]
    return url


# Métodos específicos para cada página
def buscar_urlvoid(url):
    url_final = f"https://www.urlvoid.com/scan/{limpiar_url(url)}"
    webbrowser.open(url_final)


def buscar_talos_intelligence(url):
    url_final = f"https://www.talosintelligence.com/reputation_center/lookup?search={quote(url)}"
    webbrowser.open(url_final)


def buscar_sitechecker(url):
    url_final = f"https://sitechecker.pro/app/main/website-safety-land?pageUrl={quote(url)}"
    webbrowser.open(url_final)


def buscar_norton(url):
    url_final = f"https://safeweb.norton.com/report?url={quote(url)}"
    webbrowser.open(url_final)


def buscar_google_safe_browsing(url):
    url_final = f"https://transparencyreport.google.com/safe-browsing/search?url={quote(url)}"
    webbrowser.open(url_final)


# Lista de servicios
SERVICIOS = [
    ("URLVoid", buscar_urlvoid),
    ("Talos Intelligence", buscar_talos_intelligence),
    ("SiteChecker", buscar_sitechecker),
    ("Norton Safe Web", buscar_norton),
    ("Google Safe Browsing", buscar_google_safe_browsing),
]