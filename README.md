# Car Scout 🚗

Car Scout howa assistant (intelligence artificielle) y3awnek tal9a karhba occasion fi Tounes.

Tektbou chnowa t7eb, b Darija, b Fran9ais walla b Anglais, w houwa ylawej fi les sites mta3 les annonces fi Tounes w yraja3lek jweb m3a les liens.

Exemple:

> nheb clio 4 essence fi sfax, mouch akther men 35 alf

## Chnowa ya3mel

- **Yefhem chnowa t7eb**: el marque, el modèle, el ville, el budget, el carburant, boîte auto walla manuelle.
- **Ylawej 3al annonces** fil internet, w y3tik les liens.
- **Yetfakker chnowa t7eb**: ken 9otlou marra "diesel fi Tunis", el marra el jeya ya3ref.
- **Yetfakker el 7diith**: fi nafs el chat, tnajjem t9oullou "w wa7da arkhes?" walla "w fi Sousse?" w yefhem 3la chnowa tahki. "New chat" yebda men jdid.
- **Ma ynsach el chat**: ken t3awed t7ell el page, el chat elli kont fih yarja3.
- **Y9ra el prix, el 3am wel kilométrage** mel annonces, w y9ollek ken el prix rkhis, normal walla ghali m9arna bel annonces lokhrin.
- **Ys2lek ken mafhemch**: ken t9oullou "nheb karhba" bark, ys2lek chnowa el modèle wel budget 9bal ma ylawej.

## Chnowa mazel mouch mawjoud

- El prix, el 3am wel kilométrage y9rahom ken mel texte el 9sir elli ytla3 fil recherche, mouch mel annonce kemla. Ken el texte ma fihomch, lazmek t7ell el lien.
- El "rkhis walla ghali" m9arna ken bel annonces elli l9ahom fi nafs el recherche, ya3ni ta9rib barka.

Les détails lkol mawjoudin fi [TODO.md](TODO.md).

## Kifech yekhdem (el sou2el win yemchi)

1. **Ta3ref chkoun enti**: ya9ra les préférences mta3ek (Supabase) w el messages elli 9bal fi nafs el chat.
2. **Yefhem el sou2el** (Claude, appel 1): ya3mel menou recherche: marque, modèle, ville, budget...
   Ken el sou2el ghamedh barcha ("nheb karhba"), yes2lek sou2el w yo9ef houni.
3. **Ylawej** (SearXNG, bilech): yjib 10 résultats mel internet.
4. **Y9ra les annonces** (bilech, bla Claude): yal9a el prix, el 3am wel km, w y9arenhom ba3dhom.
5. **Yekteb el jweb** (Claude, appel 2): ykhtar a7sen les annonces w y3tik les liens.
6. **Ykhabbi** el sou2el wel jweb fi Supabase, bech yetfakkarhom el marra el jeya.

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
    agent/
      answer_question.py  el tartib mta3 les étapes lkol (chouf "Kifech yekhdem")
      steps/              kol étape fi fichier: load_conversation, understand_message,
                          ask_user_question, run_tools, write_answer, save_conversation...
      prompts/            el instructions elli yab3athhom l Claude (tnajjem tbaddelhom)
    tools/
      search_car_ads.py   el recherche fi SearXNG
      read_ads.py         y9ra el prix, el 3am wel km mel annonces
      save_preferences.py ykhabbi les préférences
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

### 9addech yekleflek

- Sou2el 3adi = **2 appels l Claude** (yefhem, ba3d yekteb).
- Ken ys2lek sou2el (ma fhemch) = **appel wa7ed** barka.
- El chat ki ytawel, kol sou2el ywalli ghali chwaya, 5ater yab3ath m3ah el messages elli 9bal (akther 7aja 10 messages).
- El model elli mesta3mel: `claude-haiku-5-5`, a rkhes wa7ed.

Tnajjem tbaddel hedha lkol fi [backend/config.py](backend/config.py):

| Réglage | Chnowa ya3mel |
| --- | --- |
| `DEFAULT_MODEL` | el model mta3 Claude. `claude-opus-5-5` a9wa ama aghla. |
| `MAX_SEARCH_RESULTS` | 9addech men résultat yjib mel recherche (10). |
| `MAX_EARLIER_MESSAGES` | 9addech men message 9dim yab3ath l Claude (10). A9al = arkhes. |
| `MAX_EARLIER_MESSAGE_LENGTH` | ya9ta3 el messages el twal (1500 7arf). |

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

**5. Bni el page React** (marra barka, w 3awedha kol ma tbaddel 7aja fi `frontend` walla ki tjib version jdida men GitHub):
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

## Kifech tjarrbou

Demarri `python main.py` (w SearXNG khaddem), ba3d jarreb:

| A3mel | Lazem ysir |
| --- | --- |
| Ekteb "Golf 7 diesel under 60k in Tunis" | Y3tik annonces m3a les liens, w ken el prix mektoub, y9ollek rkhis walla ghali |
| Ekteb "w wa7da arkhes?" | Ylawej 3la Golf 7 b prix a9al |
| A3mel F5 (reload) | El chat yarja3 kif ma kén |
| Enzel **New chat**, w ekteb "nheb karhba" | Ys2lek chnowa el modèle wel budget, w ma ylawejch |
| Jawbou "Clio 4, 35 alf" | Ylawej 3la Clio 4 b 35 000 DT walla a9al |

⚠️ Kol sou2el yekhou chwaya flous mel crédit Claude.

## Ken famma mochkla

- **"Could not save..." walla "Could not load..."**: Supabase ma jewbetch. Car Scout yjaweb 3adi, ama ma ykhabich el conversation w ma yetfakkarch. Thabbet les clés mta3 Supabase fi `.env`.
- **Ma yal9a 7atta annonce, walla y9oul el recherche ma khdmetch**: SearXNG mahouch khaddem. 7ell Docker Desktop w demarri `searxng`.
- **"The Anthropic API key was rejected"**: el clé mta3 Claude ghalta. Thabbetha fi `.env`.
- **"The chat page is not built yet"**: a3mel l'étape 5.
- **Baddelt fil React ama ma tbaddel chay fil page**: 3awed `npm run build` fi `frontend`, ba3d F5.
- **T7eb tsayyeb el chat el 9dim w tebda jdid**: enzel **New chat**.
- **SearXNG mouch 3al port 8080?** 7ott `SEARXNG_URL=...` fi `.env`.
