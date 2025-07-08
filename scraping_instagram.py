
import instaloader
import pandas as pd
from datetime import datetime

# Perfiles a analizar
accounts = [
    "ercoenergia",
    "epmestamosahi",
    "celsia_energia",
    "vatia_energia",
    "bia_energy",
    "enelx_colombia"
]

# Inicializa Instaloader
L = instaloader.Instaloader()

data = []

for account in accounts:
    try:
        profile = instaloader.Profile.from_username(L.context, account)
        for post in profile.get_posts():
            post_date = post.date_utc.strftime("%Y-%m-%d")
            if post_date < datetime.utcnow().strftime("%Y-%m-%d"):  # solo posts hasta hoy
                break
            data.append({
                "account": account,
                "date": post_date,
                "caption": post.caption,
                "likes": post.likes,
                "comments": post.comments,
                "url": post.url
            })
    except Exception as e:
        print(f"Error con {account}: {e}")

# Guardar histórico
df = pd.DataFrame(data)
today = datetime.today().strftime('%Y-%m-%d')
df.to_csv(f"instagram_data_{today}.csv", index=False)
print(f"Scraping completado para {len(accounts)} cuentas.")
