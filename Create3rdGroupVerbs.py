# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 19:04:04 2025

@author: cmedous
"""

# -*- coding: utf-8 -*-
"""
Generate FR->IT JSON files (ALL TENSES) for these -IRE verbs:
aprire, partire, coprire, offrire, scoprire, seguire, sentire, servire,
finire, capire, pulire, preferire, costruire, bollire, nutrire, proibire,
spedire, unire, vestire, tossire

Writes into:  decks/fr-it/<french_lemma_ascii>.json
Merges into:  decks/fr-it/index.json

Run from Spyder or:
  python generate_ire_verbs.py
"""

import json, os

DECK_DIR = os.path.join("decks", "fr-it")
os.makedirs(DECK_DIR, exist_ok=True)

FR_PRONOUNS = ["je", "tu", "il/elle", "nous", "vous", "ils/elles"]
IT_PRONOUNS = ["io", "tu", "lui/lei", "noi", "voi", "loro"]

# Fixed 'scopire' -> 'scoprire'
VERBS = [
    "aprire","partire","coprire","offrire","scoprire","seguire","sentire","servire",
    "finire","capire","pulire","preferire","costruire","bollire","nutrire","proibire",
    "spedire","unire","vestire","tossire"
]

# Display French lemmas (and ASCII filenames)
FR_MAP = {
    "aprire": ("ouvrir","ouvrir"),
    "partire": ("partir","partir"),
    "coprire": ("couvrir","couvrir"),
    "offrire": ("offrir","offrir"),
    "scoprire": ("découvrir","decouvrir"),
    "seguire": ("suivre","suivre"),
    "sentire": ("entendre","entendre"),
    "servire": ("servir","servir"),
    "finire": ("finir","finir"),
    "capire": ("comprendre","comprendre"),
    "pulire": ("nettoyer","nettoyer"),
    "preferire": ("préférer","preferer"),
    "costruire": ("construire","construire"),
    "bollire": ("bouillir","bouillir"),
    "nutrire": ("nourrir","nourrir"),
    "proibire": ("interdire","interdire"),
    "spedire": ("envoyer","envoyer"),
    "unire": ("unir","unir"),
    "vestire": ("habiller","habiller"),
    "tossire": ("tousser","tousser"),
}

# Auxiliaries: essere only for 'partire'; others avere
AUX = {v: ("essere" if v=="partire" else "avere") for v in VERBS}

# Past participles
PP = {
    "aprire":"aperto","partire":"partito","coprire":"coperto","offrire":"offerto","scoprire":"scoperto",
    "seguire":"seguito","sentire":"sentito","servire":"servito","finire":"finito","capire":"capito",
    "pulire":"pulito","preferire":"preferito","costruire":"costruito","bollire":"bollito","nutrire":"nutrito",
    "proibire":"proibito","spedire":"spedito","unire":"unito","vestire":"vestito","tossire":"tossito"
}

# -isc- verbs (presente / cong. pres. / imperativo tu-lui-loro)
ISC = {"finire","capire","pulire","preferire","costruire","proibire","spedire","unire","tossire"}

def stem(v): return v[:-3]

def indicativo_presente(v):
    b = stem(v)
    if v in ISC:
        forms = [b+"isco", b+"isci", b+"isce", b+"iamo", b+"ite", b+"iscono"]
    else:
        forms = [b+"o", b+"i", b+"e", b+"iamo", b+"ite", b+"ono"]
    return [f"{p} {f}" for p,f in zip(IT_PRONOUNS, forms)]

def imperfetto(v):
    b = stem(v); ends = ["ivo","ivi","iva","ivamo","ivate","ivano"]
    return [f"{p} {b}{e}" for p,e in zip(IT_PRONOUNS, ends)]

def passato_remoto(v):
    b = stem(v)
    forms = [b+"ii", b+"isti", b+"ì", b+"immo", b+"iste", b+"irono"]
    return [f"{p} {f}" for p,f in zip(IT_PRONOUNS, forms)]

def futuro_root(v): return v[:-1]  # infinitive minus -e
def futuro_semplice(v):
    r = futuro_root(v); ends = ["ò","ai","à","emo","ete","anno"]
    return [f"{p} {r}{e}" for p,e in zip(IT_PRONOUNS, ends)]

def condizionale_presente(v):
    r = futuro_root(v); ends = ["ei","esti","ebbe","emmo","este","ebbero"]
    return [f"{p} {r}{e}" for p,e in zip(IT_PRONOUNS, ends)]

def congiuntivo_presente(v):
    b = stem(v)
    if v in ISC:
        forms = [b+"isca", b+"isca", b+"isca", b+"iamo", b+"iate", b+"iscano"]
    else:
        forms = [b+"a", b+"a", b+"a", b+"iamo", b+"iate", b+"ano"]
    return [f"che {p} {f}" for p,f in zip(IT_PRONOUNS, forms)]

def congiuntivo_imperfetto(v):
    b = stem(v); ends = ["issi","issi","isse","issimo","iste","issero"]
    return [f"che {p} {b}{e}" for p,e in zip(IT_PRONOUNS, ends)]

def participio_presente(v): return stem(v) + "ente"
def gerundio_presente(v):   return stem(v) + "endo"

def aux_pres(a): return ["ho","hai","ha","abbiamo","avete","hanno"] if a=="avere" else ["sono","sei","è","siamo","siete","sono"]
def aux_impf(a): return ["avevo","avevi","aveva","avevamo","avevate","avevano"] if a=="avere" else ["ero","eri","era","eravamo","eravate","erano"]
def aux_rem(a):  return ["ebbi","avesti","ebbe","avemmo","aveste","ebbero"] if a=="avere" else ["fui","fosti","fu","fummo","foste","furono"]
def aux_fut(a):  return ["avrò","avrai","avrà","avremo","avrete","avranno"] if a=="avere" else ["sarò","sarai","sarà","saremo","sarete","saranno"]
def aux_cond(a): return ["avrei","avresti","avrebbe","avremmo","avreste","avrebbero"] if a=="avere" else ["sarei","saresti","sarebbe","saremmo","sareste","sarebbero"]
def aux_cong_pres(a): return ["che io abbia","che tu abbia","che lui/lei abbia","che noi abbiamo","che voi abbiate","che loro abbiano"] if a=="avere" else ["che io sia","che tu sia","che lui/lei sia","che noi siamo","che voi siate","che loro siano"]
def aux_cong_impf(a): return ["che io avessi","che tu avessi","che lui/lei avesse","che noi avessimo","che voi aveste","che loro avessero"] if a=="avere" else ["che io fossi","che tu fossi","che lui/lei fosse","che noi fossimo","che voi foste","che loro fossero"]

def compose(aux_forms, pp, essere=False):
    out = []
    for p,a in zip(IT_PRONOUNS, aux_forms):
        if essere:
            # masculine default; plural -> 'i'
            if any(k in a for k in ["siamo","siete","eravamo","eravate","saremo","sarete","fummo","foste"]) or a.endswith(("mo","te","no")):
                out.append(f"{p} {a} {pp[:-1] + 'i' if pp.endswith('o') else pp}")
            else:
                out.append(f"{p} {a} {pp}")
        else:
            out.append(f"{p} {a} {pp}")
    return out

def imperativo(v):
    b = stem(v)
    if v in ISC:
        return ["—", b+"isci", b+"isca", b+"iamo", b+"ite", b+"iscano"]
    else:
        return ["—", b+"i", b+"a", b+"iamo", b+"ite", b+"ano"]

def build_json(v):
    fr_disp, fr_ascii = FR_MAP[v]
    aux = AUX[v]; essere = (aux=="essere"); pp = PP[v]
    data = {
        "source_lang": "fr",
        "target_lang": "it",
        "source_lemma": fr_disp,
        "target_lemma": v,
        "meta": {
            "regularity": { "fr": "3e groupe (-ire)", "it": "terza coniugazione (-ire)" + (" con -isc-" if v in ISC else "") },
            "auxiliary": { "fr": "être" if essere else "avoir", "it": aux }
        },
        "pronouns": { "fr": FR_PRONOUNS, "it": IT_PRONOUNS },
        "Indicativo": {
            "Presente": indicativo_presente(v),
            "Passato prossimo": compose(aux_pres(aux), pp, essere=essere),
            "Imperfetto": imperfetto(v),
            "Trapassato prossimo": compose(aux_impf(aux), pp, essere=essere),
            "Passato remoto": passato_remoto(v),
            "Trapassato remoto": compose(aux_rem(aux), pp, essere=essere),
            "Futuro semplice": futuro_semplice(v),
            "Futuro anteriore": compose(aux_fut(aux), pp, essere=essere),
        },
        "Condizionale": {
            "Presente": condizionale_presente(v),
            "Passato": compose(aux_cond(aux), pp, essere=essere),
        },
        "Congiuntivo": {
            "Presente": congiuntivo_presente(v),
            "Passato": [f"{a} {pp}" for a in aux_cong_pres(aux)],
            "Imperfetto": congiuntivo_imperfetto(v),
            "Trapassato": [f"{a} {pp}" for a in aux_cong_impf(aux)],
        },
        "Imperativo": { "Presente": imperativo(v) },
        "Infinito": {
            "Presente": [v],
            "Passato": [("essere" if essere else "avere") + " " + pp]
        },
        "Participio": {
            "Presente": [participio_presente(v)],
            "Passato": [pp]
        },
        "Gerundio": {
            "Presente": [gerundio_presente(v)],
            "Passato": [("essendo" if essere else "avendo") + " " + pp]
        }
    }
    path = os.path.join(DECK_DIR, f"{fr_ascii}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return os.path.basename(path)

# --- write files ---
new_files = [build_json(v) for v in VERBS]

# --- merge into index.json ---
index_path = os.path.join(DECK_DIR, "index.json")
try:
    with open(index_path, "r", encoding="utf-8") as f:
        idx = json.load(f)
    files = list(dict.fromkeys((idx.get("files") or []) + new_files))
except FileNotFoundError:
    files = new_files

with open(index_path, "w", encoding="utf-8") as f:
    json.dump({"files": files}, f, ensure_ascii=False, indent=2)

print(f"Generated {len(new_files)} files and updated index.json.")
print("Added:", ", ".join(new_files))
