# Car Scout 🚗

Car Scout howa assistant (intelligence artificielle) y3awnek tal9a karhba occasion fi Tounes.

Tektbou chnowa t7eb, b Darija, b Fran9ais walla b Anglais, w houwa ylawej fi les sites mta3 les annonces fi Tounes w yraja3lek jweb m3a les liens.

Exemple:

> nheb clio 4 essence fi sfax, mouch akther men 35 alf

## Chnowa ya3mel

- **Yefhem chnowa t7eb**: el marque, el modèle, el ville, el budget, el carburant, boîte auto walla manuelle.
- **Ylawej 3al annonces** fil internet, w y3tik les liens.
- **Yetfakker chnowa t7eb**: ken 9otlou marra "diesel fi Tunis", el marra el jeya ya3ref.

## Chnowa mazel mouch mawjoud

- Mazel ma y9arach el prix, el 3am wel kilométrage mta3 kol annonce.
- Mazel ma yetfakkarch el messages elli 9bal: ken tes2lou "w wa7da arkhes?", ma yefhemch.

Les détails lkol mawjoudin fi [TODO.md](TODO.md).

## Kifech mabni

```
CarScout/
  main.py          howa elli ydemarri el application
  frontend/        el page elli tchoufha (React)
    src/App.jsx      el page: les messages w b3ath el sou2el
    src/components/  les morceaux mta3 el page: Header, Welcome, Message, Composer
    src/api.js       el page kifech tahki m3a el backend
  backend/         el code Python lkol
    config.py      les réglages, w ya9ra el fichier .env
    agent/         les étapes mta3 el assistant w les instructions elli yab3athhom l Claude
    tools/         les outils: recherche des annonces, sauvegarde des préférences
    services/      el connexion m3a Claude, SearXNG w Supabase
    models/        chakl les données: recherche, annonce, préférences
    rules/         7ssab el prix (rkhis, normal, ghali) w comparaison des karhbet
    app/           el API web (api.py) w el chat fil terminal (cli.py)
  setup/           fichiers t7athrhom marra barka
    database/      les tables elli lazem ta3mel'hom fi Supabase
    searxng/       les réglages mta3 SearXNG
```

## Chnowa testa3mel

| Chnowa | 3lech |
| --- | --- |
| **Claude** (Anthropic) | yefhem el sou2el w yekteb el jweb. **Kol sou2el yekhou chwaya flous** mel crédit mta3ek. |
| **SearXNG** | moteur de recherche ykhdem 3and'ek fil PC, b Docker. Bilech, ma ylazmouch clé. |
| **Supabase** | base de données fil internet, tkhabi fiha les conversations wel préférences. |
| **React** | el page elli tchoufha fil navigateur. |

## Kifech tkhaddmou

Lazmek **Python** (3.11 walla jdid), **Node.js** w **Docker Desktop**.
Les commandes lkol tektebhom fil terminal (fi VS Code: menu **Terminal > New Terminal**), w enti dakhel fil dossier `CarScout`.

**1. Habbet les librairies Python** (marra barka):
```bash
pip install -r requirements.txt
```

**2. 7ather el fichier `.env`** (marra barka):
```bash
copy .env.example .env
```
Ba3d, 7ell `.env` w 7ott fih les clés mta3ek: el clé mta3 Claude w les clés mta3 Supabase.
⚠️ El fichier hedha fih des secrets: **ma tpartajih m3a 7ad** w ma t7ottouch 3la GitHub. (Mahou déjà ma yetla3ch, `.gitignore` ymanna3).

**3. 7ather Supabase** (marra barka):
7ell Supabase, emchi l **SQL Editor**, copier el contenu mta3 `setup/database/create_tables.sql` w a3mel **Run**.

**4. 7ather SearXNG** (marra barka):
- Copier `setup/searxng/settings.example.yml` w semmi el copie `settings.yml` (fi nafs el dossier).
- Fi `settings.yml`, baddel `change-me` b klam random. Tnajjem testa3mel:
  ```bash
  python -c "import secrets; print(secrets.token_hex(16))"
  ```
- 7ell Docker Desktop w a3mel:
  ```bash
  docker run -d --name searxng -p 8080:8080 -v "%cd%\setup\searxng:/etc/searxng" searxng/searxng
  ```
  (Ken el terminal mta3ek PowerShell, baddel `%cd%` b `${PWD}`.)

El marrat el jeyin, yekfi t7ell Docker Desktop, temchi l **Containers** w tenzel 3al ▶️ 9oddem `searxng`.

**5. Bni el page React** (marra barka, w 3awedha kol ma tbaddel 7aja fi `frontend`):
```bash
cd frontend
npm install
npm run build
cd ..
```

**6. Demarri Car Scout:**
```bash
python main.py
```
El page tet7al wa7adha fil navigateur 3al `http://127.0.0.1:8000`.
Bech tsakkrou: `Ctrl+C` fil terminal.

El page tekhdem **ken 3al PC mta3ek**, 5ater ma fihech login.

### Ken t7eb el chat fil terminal

```bash
python main.py cli
```

### Ken t7eb tbaddel fil page React

7ell zouz terminals:
- Terminal 1: `python main.py`
- Terminal 2: `cd frontend` ba3d `npm run dev`, w 7ell `http://localhost:5173`

Kol ma tsajjel fichier, el page titbaddel wa7adha, mouch lazem ta3mel build.

## Ken famma mochkla

- **"Not saved"**: Supabase ma jewbetch. Car Scout yjaweb 3adi, ama ma ykhabich el conversation. Thabbet les clés mta3 Supabase fi `.env`.
- **Ma yal9a 7atta annonce, walla y9oul el recherche ma khdmetch**: SearXNG mahouch khaddem. 7ell Docker Desktop w demarri `searxng`.
- **"The Anthropic API key was rejected"**: el clé mta3 Claude ghalta. Thabbetha fi `.env`.
- **"The chat page is not built yet"**: a3mel l'étape 5.
- **SearXNG mouch 3al port 8080?** 7ott `SEARXNG_URL=...` fi `.env`.
