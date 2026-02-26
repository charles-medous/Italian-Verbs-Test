# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 18:52:32 2025

@author: cmedous
"""

# -*- coding: utf-8 -*-
"""
Generate FR->IT JSON files (ALL TENSES) for these -ERE verbs:
scrivere, prendere, chiedere, chiudere, conoscere, correre, decidere, leggere,
mettere, perdere, piangere, ridere, sorridere, vedere, vendere, rispondere,
vincere, vivere, crescere, spendere, ricevere, dividere, offendere, temere, scendere

It writes into:  decks/fr-it/<french_lemma_ascii>.json
and merges them into decks/fr-it/index.json

Run from Spyder or:
  python generate_ere_verbs.py
"""

import json, os, unicodedata

DECK_DIR = os.path.join("decks", "fr-it")
os.makedirs(DECK_DIR, exist_ok=True)

FR_PRONOUNS = ["je", "tu", "il/elle", "nous", "vous", "ils/elles"]
IT_PRONOUNS = ["io", "tu", "lui/lei", "noi", "voi", "loro"]

def ascii_name(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))\
            .replace("’","").replace("'","").replace(" ", "_").lower()

# it_verb -> (fr_display, fr_ascii_filename, aux_it "avere|essere")
SPEC = {
    "scrivere": ("écrire", "ecrire", "avere"),
    "prendere": ("prendre", "prendre", "avere"),
    "chiedere": ("demander", "demander", "avere"),
    "chiudere": ("fermer", "fermer", "avere"),
    "conoscere": ("connaître", "connaitre", "avere"),
    "correre": ("courir", "courir", "avere"),
    "decidere": ("décider", "decider", "avere"),
    "leggere": ("lire", "lire", "avere"),
    "mettere": ("mettre", "mettre", "avere"),
    "perdere": ("perdre", "perdre", "avere"),
    "piangere": ("pleurer", "pleurer", "avere"),
    "ridere": ("rire", "rire", "avere"),
    "sorridere": ("sourire", "sourire", "avere"),
    "vedere": ("voir", "voir", "avere"),
    "vendere": ("vendre", "vendre", "avere"),
    "rispondere": ("répondre", "repondre", "avere"),
    "vincere": ("gagner", "gagner", "avere"),
    "vivere": ("vivre", "vivre", "avere"),
    "crescere": ("grandir", "grandir", "essere"),
    "spendere": ("dépenser", "depenser", "avere"),
    "ricevere": ("recevoir", "recevoir", "avere"),
    "dividere": ("diviser", "diviser", "avere"),
    "offendere": ("offenser", "offenser", "avere"),
    "temere": ("craindre", "craindre", "avere"),
    "scendere": ("descendre", "descendre", "essere"),
}

# irregular past participles
PP = {
    "scrivere":"scritto","prendere":"preso","chiedere":"chiesto","chiudere":"chiuso",
    "conoscere":"conosciuto","correre":"corso","decidere":"deciso","leggere":"letto",
    "mettere":"messo","perdere":"perso","piangere":"pianto","ridere":"riso","sorridere":"sorriso",
    "vedere":"visto","vendere":"venduto","rispondere":"risposto","vincere":"vinto","vivere":"vissuto",
    "crescere":"cresciuto","spendere":"speso","ricevere":"ricevuto","dividere":"diviso",
    "offendere":"offeso","temere":"temuto","scendere":"sceso",
}

# irregular future/conditional stems
FUT_STEM = { "vedere":"vedr", "vivere":"vivr" }

# passato remoto (no pronouns)
REMOTO = {
    "scrivere": ["scrissi","scrivesti","scrisse","scrivemmo","scriveste","scrissero"],
    "prendere": ["presi","prendesti","prese","prendemmo","prendeste","presero"],
    "chiedere": ["chiesi","chiedesti","chiese","chiedemmo","chiedeste","chiesero"],
    "chiudere": ["chiusi","chiudesti","chiuse","chiudemmo","chiudeste","chiusero"],
    "conoscere": ["conobbi","conoscesti","conobbe","conoscemmo","conosceste","conobbero"],
    "correre": ["corsi","corresti","corse","corremmo","correste","corsero"],
    "decidere": ["decisi","decidesti","decise","decidemmo","decideste","decisero"],
    "leggere": ["lessi","leggesti","lesse","leggemmo","leggeste","lessero"],
    "mettere": ["misi","mettesti","mise","mettemmo","metteste","misero"],
    "perdere": ["persi","perdesti","perse","perdemmo","perdeste","persero"],
    "piangere": ["piansi","piangesti","pianse","piangemmo","piangeste","piansero"],
    "ridere": ["risi","ridesti","rise","ridemmo","rideste","risero"],
    "sorridere": ["sorrisi","sorridesti","sorrise","sorridemmo","sorrideste","sorrisero"],
    "vedere": ["vidi","vedesti","vide","vedemmo","vedeste","videro"],
    "vendere": ["vendetti","vendesti","vendette","vendemmo","vendeste","vendettero"],
    "rispondere": ["risposi","rispondesti","rispose","rispondemmo","rispondeste","risposero"],
    "vincere": ["vinsi","vincesti","vinse","vincemmo","vinceste","vinsero"],
    "vivere": ["vissi","vivesti","visse","vivemmo","viveste","vissero"],
    "crescere": ["crebbi","crescesti","crebbe","crescEmmo".lower(),"cresceste","crebbero"],
    "spendere": ["spesi","spendesti","spese","spendemmo","spendeste","spesero"],
    "ricevere": ["ricevetti","ricevesti","ricevette","ricevemmo","riceveste","ricevettero"],
    "dividere": ["divisi","dividesti","divise","dividemmo","divideste","divisero"],
    "offendere": ["offesi","offendesti","offese","offendemmo","offendeste","offesero"],
    "temere": ["temetti","temesti","temette","tememmo","temeste","temettero"],
    "scendere": ["scesi","scendesti","scese","scendemmo","scendeste","scesero"],
}

def st(verb_it): return verb_it[:-3]  # remove 'ere'

def indicativo_presente(verb_it):
    base = st(verb_it)
    ends = ["o","i","e","iamo","ete","ono"]
    return [f"{p} {base}{e}" for p,e in zip(IT_PRONOUNS, ends)]

def imperfetto(verb_it):
    base = st(verb_it)
    ends = ["evo","evi","eva","evamo","evate","evano"]
    return [f"{p} {base}{e}" for p,e in zip(IT_PRONOUNS, ends)]

def passato_remoto(verb_it):
    forms = REMOTO.get(verb_it, [st(verb_it)+"etti", st(verb_it)+"esti", st(verb_it)+"ette", st(verb_it)+"emmo", st(verb_it)+"este", st(verb_it)+"ettero"])
    return [f"{p} {f}" for p,f in zip(IT_PRONOUNS, forms)]

def futuro_root(verb_it): return FUT_STEM.get(verb_it, verb_it[:-1])  # infinitive minus final -e
def futuro_semplice(verb_it):
    r = futuro_root(verb_it)
    ends = ["ò","ai","à","emo","ete","anno"]
    return [f"{p} {r}{e}" for p,e in zip(IT_PRONOUNS, ends)]

def condizionale_presente(verb_it):
    r = futuro_root(verb_it)
    ends = ["ei","esti","ebbe","emmo","este","ebbero"]
    return [f"{p} {r}{e}" for p,e in zip(IT_PRONOUNS, ends)]

def congiuntivo_presente(verb_it):
    base = st(verb_it)
    ends = ["a","a","a","iamo","iate","ano"]
    return [f"che {p} {base}{e}" for p,e in zip(IT_PRONOUNS, ends)]

def congiuntivo_imperfetto(verb_it):
    base = st(verb_it)
    ends = ["essi","essi","esse","essimo","este","essero"]
    return [f"che {p} {base}{e}" for p,e in zip(IT_PRONOUNS, ends)]

def aux_pres(it): return ["ho","hai","ha","abbiamo","avete","hanno"] if it=="avere" else ["sono","sei","è","siamo","siete","sono"]
def aux_impf(it): return ["avevo","avevi","aveva","avevamo","avevate","avevano"] if it=="avere" else ["ero","eri","era","eravamo","eravate","erano"]
def aux_rem(it):  return ["ebbi","avesti","ebbe","avemmo","aveste","ebbero"] if it=="avere" else ["fui","fosti","fu","fummo","foste","furono"]
def aux_fut(it):  return ["avrò","avrai","avrà","avremo","avrete","avranno"] if it=="avere" else ["sarò","sarai","sarà","saremo","sarete","saranno"]
def aux_cond(it): return ["avrei","avresti","avrebbe","avremmo","avreste","avrebbero"] if it=="avere" else ["sarei","saresti","sarebbe","saremmo","sareste","sarebbero"]
def aux_cong_pres(it): return ["che io abbia","che tu abbia","che lui/lei abbia","che noi abbiamo","che voi abbiate","che loro abbiano"] if it=="avere" else ["che io sia","che tu sia","che lui/lei sia","che noi siamo","che voi siate","che loro siano"]
def aux_cong_impf(it): return ["che io avessi","che tu avessi","che lui/lei avesse","che noi avessimo","che voi aveste","che loro avessero"] if it=="avere" else ["che io fossi","che tu fossi","che lui/lei fosse","che noi fossimo","che voi foste","che loro fossero"]

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

def imperativo(verb_it):
    base = st(verb_it)
    # ["—", tu, lui/lei, noi, voi, loro]  (-ere pattern)
    return ["—", base+"i", base+"a", base+"iamo", base+"ete", base+"ano"]

def build_json(verb_it, fr_disp, fr_ascii, aux_it):
    base = st(verb_it)
    essere = (aux_it == "essere")
    pp = PP[verb_it]

    data = {
        "source_lang": "fr",
        "target_lang": "it",
        "source_lemma": fr_disp,
        "target_lemma": verb_it,
        "meta": {
            "regularity": { "fr": "2e groupe (-ere) avec irrégularités", "it": "seconda coniugazione (-ere)" },
            "auxiliary": { "fr": "être" if essere else "avoir", "it": aux_it }
        },
        "pronouns": { "fr": FR_PRONOUNS, "it": IT_PRONOUNS },
        "Indicativo": {
            "Presente": indicativo_presente(verb_it),
            "Passato prossimo": compose(aux_pres(aux_it), pp, essere=essere),
            "Imperfetto": imperfetto(verb_it),
            "Trapassato prossimo": compose(aux_impf(aux_it), pp, essere=essere),
            "Passato remoto": passato_remoto(verb_it),
            "Trapassato remoto": compose(aux_rem(aux_it), pp, essere=essere),
            "Futuro semplice": futuro_semplice(verb_it),
            "Futuro anteriore": compose(aux_fut(aux_it), pp, essere=essere),
        },
        "Condizionale": {
            "Presente": condizionale_presente(verb_it),
            "Passato": compose(aux_cond(aux_it), pp, essere=essere),
        },
        "Congiuntivo": {
            "Presente": congiuntivo_presente(verb_it),
            "Passato": [f"{a} {pp}" for a in aux_cong_pres(aux_it)],
            "Imperfetto": congiuntivo_imperfetto(verb_it),
            "Trapassato": [f"{a} {pp}" for a in aux_cong_impf(aux_it)],
        },
        "Imperativo": { "Presente": imperativo(verb_it) },
        "Infinito": {
            "Presente": [verb_it],
            "Passato": [("essere" if essere else "avere") + " " + pp]
        },
        "Participio": {
            "Presente": [base + "ente"],
            "Passato": [pp]
        },
        "Gerundio": {
            "Presente": [base + "endo"],
            "Passato": [("essendo" if essere else "avendo") + " " + pp]
        }
    }

    path = os.path.join(DECK_DIR, f"{fr_ascii}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return os.path.basename(path)

# --- Write all files ---
new_files = []
for it, (fr_disp, fr_ascii, aux) in SPEC.items():
    new_files.append(build_json(it, fr_disp, fr_ascii, aux))

# --- Merge into decks/fr-it/index.json ---
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
