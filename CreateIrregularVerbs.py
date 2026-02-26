# -*- coding: utf-8 -*-
"""
Created on Fri Aug 29 20:59:12 2025

@author: cmedous
"""

# -*- coding: utf-8 -*-
"""
Generate FR->IT JSON files (ALL TENSES) for irregular verbs:
andare, fare, dare, stare, bere, sapere, tenere, ottenere, mantenere,
ritenere, sostenere, trattenere, rimanere, scegliere, togliere, cogliere,
raccogliere, volere, condurre, tradurre, produrre, introdurre, proporre,
porre, esporre, opporre, uscire, dire, predire, disdire, venire, salire,
apparire, scomparire, finire, avere, essere

Writes into:  decks/fr-it/<french_lemma_ascii>.json
Merges into:  decks/fr-it/index.json
"""

import json, os

DECK_DIR = os.path.join("decks", "fr-it")
os.makedirs(DECK_DIR, exist_ok=True)

FR_PRONOUNS = ["je", "tu", "il/elle", "nous", "vous", "ils/elles"]
IT_PRONOUNS = ["io", "tu", "lui/lei", "noi", "voi", "loro"]

VERBS = [
    "andare","fare","dare","stare","bere","sapere","tenere","ottenere","mantenere","ritenere","sostenere","trattenere",
    "rimanere","scegliere","togliere","cogliere","raccogliere","volere","condurre","tradurre","produrre","introdurre",
    "proporre","porre","esporre","opporre","uscire","dire","predire","disdire","venire","salire","apparire","scomparire",
    "finire","avere","essere"
]

# Auxiliaries (it)
AUX = {v: "avere" for v in VERBS}
for v in ("andare","stare","rimanere","uscire","venire","salire","apparire","scomparire"):
    AUX[v] = "essere"

# French display lemmas + ascii filenames (unique)
FR_MAP = {
    "andare": ("aller","aller"),
    "fare": ("faire","faire"),
    "dare": ("donner","donner"),
    "stare": ("rester","rester"),
    "bere": ("boire","boire"),
    "sapere": ("savoir","savoir"),
    "tenere": ("tenir","tenir"),
    "ottenere": ("obtenir","obtenir"),
    "mantenere": ("maintenir","maintenir"),
    "ritenere": ("retenir","retenir"),
    "sostenere": ("soutenir","soutenir"),
    "trattenere": ("retenir (trattenere)","retenir_trattenere"),
    "rimanere": ("rester (rimanere)","rester_rimanere"),
    "scegliere": ("choisir","choisir"),
    "togliere": ("enlever","enlever"),
    "cogliere": ("cueillir","cueillir"),
    "raccogliere": ("recueillir","recueillir"),
    "volere": ("vouloir","vouloir"),
    "condurre": ("conduire","conduire"),
    "tradurre": ("traduire","traduire"),
    "produrre": ("produire","produire"),
    "introdurre": ("introduire","introduire"),
    "porre": ("poser","poser"),
    "proporre": ("proposer","proposer"),
    "esporre": ("exposer","exposer"),
    "opporre": ("opposer","opposer"),
    "uscire": ("sortir","sortir"),
    "dire": ("dire","dire"),
    "predire": ("prédire","predire"),
    "disdire": ("décommander","decommander"),
    "venire": ("venir","venir"),
    "salire": ("monter","monter"),
    "apparire": ("apparaître","apparaitre"),
    "scomparire": ("disparaître","disparaitre"),
    "finire": ("finir","finir"),
    "avere": ("avoir","avoir"),
    "essere": ("être","etre"),
}

# Indicativo Presente (io..loro without pronouns)
PRES_IND = {
    "andare": ["vado","vai","va","andiamo","andate","vanno"],
    "fare": ["faccio","fai","fa","facciamo","fate","fanno"],
    "dare": ["do","dai","dà","diamo","date","danno"],
    "stare": ["sto","stai","sta","stiamo","state","stanno"],
    "bere": ["bevo","bevi","beve","beviamo","bevete","bevono"],
    "sapere": ["so","sai","sa","sappiamo","sapete","sanno"],
    "tenere": ["tengo","tieni","tiene","teniamo","tenete","tengono"],
    "ottenere": ["ottengo","ottieni","ottiene","otteniamo","ottenete","ottengono"],
    "mantenere": ["mantengo","mantieni","mantiene","manteniamo","mantenete","mantengono"],
    "ritenere": ["ritengo","ritieni","ritiene","riteniamo","ritenete","ritengono"],
    "sostenere": ["sostengo","sostieni","sostiene","sosteniamo","sostenete","sostengono"],
    "trattenere": ["trattengo","trattieni","trattiene","tratteniamo","trattenete","trattengono"],
    "rimanere": ["rimango","rimani","rimane","rimaniamo","rimanete","rimangono"],
    "scegliere": ["scelgo","scegli","sceglie","scegliamo","scegliete","scelgono"],
    "togliere": ["tolgo","togli","toglie","togliamo","togliete","tolgono"],
    "cogliere": ["colgo","cogli","coglie","cogliamo","cogliete","colgono"],
    "raccogliere": ["raccolgo","raccogli","raccoglie","raccogliamo","raccogliete","raccolgono"],
    "volere": ["voglio","vuoi","vuole","vogliamo","volete","vogliono"],
    "condurre": ["conduco","conduci","conduce","conduciamo","conducete","conducono"],
    "tradurre": ["traduco","traduci","traduce","traduciamo","traducete","traducono"],
    "produrre": ["produco","produci","produce","produciamo","producete","producono"],
    "introdurre": ["introduco","introduci","introduce","introduciamo","introducete","introducono"],
    "porre": ["pongo","poni","pone","poniamo","ponete","pongono"],
    "proporre": ["propongo","proponi","propone","proponiamo","proponete","propongono"],
    "esporre": ["espongo","esponi","espone","esponiamo","esponete","espongono"],
    "opporre": ["oppongo","opponi","oppone","opponiamo","opponete","oppongono"],
    "uscire": ["esco","esci","esce","usciamo","uscite","escono"],
    "dire": ["dico","dici","dice","diciamo","dite","dicono"],
    "predire": ["predico","predici","predice","prediciamo","predite","predicono"],
    "disdire": ["disdico","disdici","disdice","disdiciamo","disdite","disdicono"],
    "venire": ["vengo","vieni","viene","veniamo","venite","vengono"],
    "salire": ["salgo","sali","sale","saliamo","salite","salgono"],
    "apparire": ["appaio","appari","appare","appariamo","apparite","appaiono"],
    "scomparire": ["scompaio","scompari","scompare","scompariamo","scomparite","scompaiono"],
    "finire": ["finisco","finisci","finisce","finiamo","finite","finiscono"],
    "avere": ["ho","hai","ha","abbiamo","avete","hanno"],
    "essere": ["sono","sei","è","siamo","siete","sono"],
}

def with_pronouns(forms): return [f"{p} {f}" for p,f in zip(IT_PRONOUNS, forms)]

# Futuro/Condizionale stems
FUT_STEM = {
    "andare":"andr","fare":"far","dare":"dar","stare":"star","bere":"berr","sapere":"sapr",
    "tenere":"terr","ottenere":"otterr","mantenere":"manterr","ritenere":"riterr","sostenere":"sosterr","trattenere":"tratterr",
    "rimanere":"rimarr","scegliere":"sceglier","togliere":"toglier","cogliere":"coglier","raccogliere":"raccoglier",
    "volere":"vorr","condurre":"condurr","tradurre":"tradurr","produrre":"produrr","introdurre":"introdurr",
    "porre":"porr","proporre":"proporr","esporre":"esporr","opporre":"opporr",
    "uscire":"uscir","dire":"dir","predire":"predir","disdire":"disdir","venire":"verr","salire":"salir",
    "apparire":"apparir","scomparire":"scomparir","finire":"finir","avere":"avr","essere":"sar"
}
def futuro_semplice(v):
    r = FUT_STEM[v]; ends = ["ò","ai","à","emo","ete","anno"]
    return with_pronouns([r+e for e in ends])
def condizionale_presente(v):
    r = FUT_STEM[v]; ends = ["ei","esti","ebbe","emmo","este","ebbero"]
    return with_pronouns([r+e for e in ends])

# Passato remoto (no pronouns)
REMOTO = {
    "fare": ["feci","facesti","fece","facemmo","faceste","fecero"],
    "dare": ["diedi","desti","diede","demmo","deste","diedero"],
    "stare": ["stetti","stesti","stette","stemmo","steste","stettero"],
    "bere": ["bevvi","bevesti","bevve","bevemmo","beveste","bevvero"],
    "sapere": ["seppi","sapesti","seppe","sapemmo","sapeste","seppero"],
    "tenere": ["tenni","tenesti","tenne","tenemmo","teneste","tennero"],
    "ottenere": ["ottenni","ottenesti","ottenne","ottenemmo","otteneste","ottennero"],
    "mantenere": ["mantenni","mantenesti","mantenne","mantenemmo","manteneste","mantennero"],
    "ritenere": ["ritenni","ritenesti","ritenne","ritenemmo","riteneste","ritennero"],
    "sostenere": ["sostenni","sostenesti","sostenne","sostenemmo","sosteneste","sostennero"],
    "trattenere": ["trattenni","trattenesti","trattenne","trattenemmo","tratteneste","trattennero"],
    "rimanere": ["rimasi","rimanesti","rimase","rimanemmo","rimaneste","rimasero"],
    "scegliere": ["scelsi","scegliesti","scelse","scegliemmo","sceglieste","scelsero"],
    "togliere": ["tolsi","togliesti","tolse","togliemmo","toglieste","tolsero"],
    "cogliere": ["colsi","cogliesti","colse","cogliemmo","coglieste","colsero"],
    "raccogliere": ["raccolsi","raccogliesti","raccolse","raccogliemmo","raccoglieste","raccolsero"],
    "volere": ["volli","volesti","volle","volemmo","voleste","vollero"],
    "condurre": ["condussi","conducesti","condusse","conducemmo","conduceste","condussero"],
    "tradurre": ["tradussi","traducesti","tradusse","traducemmo","traduceste","tradussero"],
    "produrre": ["produssi","producesti","produsse","producemmo","produceste","produssero"],
    "introdurre": ["introdussi","introducesti","introdusse","introducemmo","introduceste","introdussero"],
    "porre": ["posi","ponesti","pose","ponemmo","poneste","posero"],
    "proporre": ["proposi","proponesti","propose","proponemmo","proponeste","proposero"],
    "esporre": ["esposi","esponesti","espose","esponemmo","esponeste","esposero"],
    "opporre": ["opposi","opponesti","oppose","opponemmo","opponeste","opposero"],
    "dire": ["dissi","dicesti","disse","dicemmo","diceste","dissero"],
    "predire": ["predissi","predicesti","predisse","predicemmo","prediceste","predissero"],
    "disdire": ["disdissi","disdicesti","disdisse","disdicemmo","disdiceste","disdissero"],
    "venire": ["venni","venisti","venne","venimmo","veniste","vennero"],
    "essere": ["fui","fosti","fu","fummo","foste","furono"],
    "avere": ["ebbi","avesti","ebbe","avemmo","aveste","ebbero"],
    "uscire": ["uscii","uscisti","uscì","uscimmo","usciste","uscirono"],
    "salire": ["salii","salisti","salì","salimmo","saliste","salirono"],
    "apparire": ["apparvi","apparisti","apparve","apparimmo","appariste","apparvero"],
    "scomparire": ["scomparvi","scomparisti","scomparve","scomparimmo","scompariste","scomparvero"],
    "finire": ["finii","finisti","finì","finimmo","finiste","finirono"],
}
def passato_remoto(v):
    if v in REMOTO:
        return with_pronouns(REMOTO[v])
    # default regular
    if v.endswith("are"):
        forms = ["ai","asti","ò","ammo","aste","arono"]
    elif v.endswith("ere"):
        forms = ["ei","esti","é","emmo","este","erono"]
    else: # ire
        forms = ["ii","isti","ì","immo","iste","irono"]
    base = v[:-3]
    return with_pronouns([base+e for e in forms])

# Participio passato
PP = {
    "andare":"andato","fare":"fatto","dare":"dato","stare":"stato","bere":"bevuto","sapere":"saputo",
    "tenere":"tenuto","ottenere":"ottenuto","mantenere":"mantenuto","ritenere":"ritenuto","sostenere":"sostenuto","trattenere":"trattenuto",
    "rimanere":"rimasto","scegliere":"scelto","togliere":"tolto","cogliere":"colto","raccogliere":"raccolto",
    "volere":"voluto","condurre":"condotto","tradurre":"tradotto","produrre":"prodotto","introdurre":"introdotto",
    "porre":"posto","proporre":"proposto","esporre":"esposto","opporre":"opposto",
    "uscire":"uscito","dire":"detto","predire":"predetto","disdire":"disdetto",
    "venire":"venuto","salire":"salito","apparire":"apparso","scomparire":"scomparso",
    "finire":"finito","avere":"avuto","essere":"stato"
}

# Imperfetto stems (special); default: verb[:-3]
IMPF_STEM = {
    "fare":"face","dire":"dice","bere":"beve",
    "porre":"pone","proporre":"propone","esporre":"espone","opporre":"oppone",
    "condurre":"conduce","tradurre":"traduce","produrre":"produce","introdurre":"introduce",
}
def imperfetto(v):
    if v == "essere":
        forms = ["ero","eri","era","eravamo","eravate","erano"]
        return with_pronouns(forms)
    base = IMPF_STEM.get(v, v[:-3])
    ends = ["vo","vi","va","vamo","vate","vano"]
    return with_pronouns([base+e for e in ends])

# Congiuntivo Presente
def cong_pres(v):
    if v == "avere":  return ["abbia","abbia","abbia","abbiamo","abbiate","abbiano"]
    if v == "essere": return ["sia","sia","sia","siamo","siate","siano"]
    mapping = {
        "andare":["vada","vada","vada","andiamo","andiate","vadano"],
        "dare":["dia","dia","dia","diamo","diate","diano"],
        "stare":["stia","stia","stia","stiamo","stiate","stiano"],
        "fare":["faccia","faccia","faccia","facciamo","facc iate".replace(" ",""),"facciano"],
        "bere":["beva","beva","beva","beviamo","beviate","bevano"],
        "sapere":["sappia","sappia","sappia","sappiamo","sappiate","sappiano"],
        "tenere":["tenga","tenga","tenga","teniamo","teniate","tengano"],
        "ottenere":["ottenga","ottenga","ottenga","otteniamo","otteniate","ottengano"],
        "mantenere":["mantenga","mantenga","mantenga","manteniamo","manteniate","mantengano"],
        "ritenere":["ritenga","ritenga","ritenga","riteniamo","riteniate","ritengano"],
        "sostenere":["sostenga","sostenga","sostenga","sosteniamo","sosteniate","sostengano"],
        "trattenere":["trattenga","trattenga","trattenga","tratteniamo","tratteniate","trattengano"],
        "rimanere":["rimanga","rimanga","rimanga","rimaniamo","rimaniate","rimangano"],
        "scegliere":["scelga","scelga","scelga","scegliamo","scegliate","scelgano"],
        "togliere":["tolga","tolga","tolga","togliamo","togliate","tolgano"],
        "cogliere":["colga","colga","colga","cogliamo","cogliate","colgano"],
        "raccogliere":["raccolga","raccolga","raccolga","raccogliamo","raccogliate","raccolgano"],
        "volere":["voglia","voglia","voglia","vogliamo","vogliate","vogliano"],
        "condurre":["conduca","conduca","conduca","conduciamo","conduciate","conducano"],
        "tradurre":["traduca","traduca","traduca","traduciamo","traduciate","traducano"],
        "produrre":["produca","produca","produca","produciamo","produciate","producano"],
        "introdurre":["introduca","introduca","introduca","introduciamo","introduciate","introducano"],
        "porre":["ponga","ponga","ponga","poniamo","poniate","pongano"],
        "proporre":["proponga","proponga","proponga","proponiamo","proponiate","propongano"],
        "esporre":["esponga","esponga","esponga","esponiamo","esponiate","espongano"],
        "opporre":["opponga","opponga","opponga","opponiamo","opponiate","oppongano"],
        "uscire":["esca","esca","esca","usciamo","usciate","escano"],
        "dire":["dica","dica","dica","diciamo","diciate","dicano"],
        "predire":["predica","predica","predica","prediciamo","prediciate","predicano"],
        "disdire":["disdica","disdica","disdica","disdiciamo","disdiciate","disdicano"],
        "venire":["venga","venga","venga","veniamo","veniate","vengano"],
        "salire":["salga","salga","salga","saliamo","salite","salgano"],
        "apparire":["appaia","appaia","appaia","appariamo","appariate","appaiano"],
        "scomparire":["scompaia","scompaia","scompaia","scompariamo","scompariate","scompaiano"],
        "finire":["finisca","finisca","finisca","finiamo","finiate","finiscano"],
    }
    if v in mapping: return mapping[v]
    pres1 = PRES_IND[v][0]
    base = pres1[:-2] if pres1.endswith("go") else pres1[:-1]
    return [base+"a",base+"a",base+"a",base+"iamo",base+"iate",base+"ano"]

def congiuntivo_presente(v):
    return [f"che {p} {f}" for p,f in zip(IT_PRONOUNS, cong_pres(v))]

# Congiuntivo Imperfetto
def congiuntivo_imperfetto(v):
    base_map = {
        "andare":"andass","dare":"dess","stare":"stess","fare":"facess","dire":"dicess","bere":"bevess",
        "sapere":"sapess","tenere":"teness","ottenere":"otteness","mantenere":"manteness","ritenere":"riteness",
        "sostenere":"sosteness","trattenere":"tratteness","rimanere":"rimaness","volere":"voless",
        "porre":"poness","proporre":"proponess","esporre":"esponess","opporre":"opponess",
        "condurre":"conducess","tradurre":"traducess","produrre":"producess","introdurre":"introducess",
        "scegliere":"scegliess","togliere":"togliess","cogliere":"cogliess","raccogliere":"raccogliess",
        "uscire":"usciss","venire":"veniss","salire":"saliss","apparire":"appariss","scomparire":"scompariss",
        "finire":"finiss","avere":"avess","essere":"foss","predire":"predicess","disdire":"disdicess",
    }
    base = base_map.get(v, v[:-3] + "ss")
    ends = ["i","i","e","imo","te","ero"]  # -> andassi,andassi,andasse,andassimo,andaste,andassero
    return [f"che {p} {base}{e}" for p,e in zip(IT_PRONOUNS, ends)]

# Imperativo
def imperativo(v):
    mp = {
        "andare":["—","vai","vada","andiamo","andate","vadano"],
        "dare":["—","dai","dia","diamo","date","diano"],
        "stare":["—","stai","stia","stiamo","state","stiano"],
        "fare":["—","fai","faccia","facciamo","fate","facciano"],
        "bere":["—","bevi","beva","beviamo","bevete","bevano"],
        "sapere":["—","sappi","sappia","sappiamo","sappiate","sappiano"],
        "tenere":["—","tieni","tenga","teniamo","tenete","tengano"],
        "ottenere":["—","ottieni","ottenga","otteniamo","ottenete","ottengano"],
        "mantenere":["—","mantieni","mantenga","manteniamo","mantenete","mantengano"],
        "ritenere":["—","ritieni","ritenga","riteniamo","ritenete","ritengano"],
        "sostenere":["—","sostieni","sostenga","sosteniamo","sostenete","sostengano"],
        "trattenere":["—","trattieni","trattenga","tratteniamo","trattenete","trattengano"],
        "rimanere":["—","rimani","rimanga","rimaniamo","rimanete","rimangano"],
        "scegliere":["—","scegli","scelga","scegliamo","scegliete","scelgano"],
        "togliere":["—","togli","tolga","togliamo","togliete","tolgano"],
        "cogliere":["—","cogli","colga","cogliamo","cogliete","colgano"],
        "raccogliere":["—","raccogli","raccolga","raccogliamo","raccogliete","raccolgano"],
        "volere":["—","vuoi","voglia","vogliamo","volete","vogliano"],
        "condurre":["—","conduci","conduca","conduciamo","conducete","conducano"],
        "tradurre":["—","traduci","traduca","traduciamo","traducete","traducano"],
        "produrre":["—","produci","produca","produciamo","producete","producano"],
        "introdurre":["—","introduci","introduca","introduciamo","introducete","introducano"],
        "porre":["—","poni","ponga","poniamo","ponete","pongano"],
        "proporre":["—","proponi","proponga","proponiamo","proponete","propongano"],
        "esporre":["—","esponi","esponga","esponiamo","esponete","espongano"],
        "opporre":["—","opponi","opponga","opponiamo","opponete","oppongano"],
        "uscire":["—","esci","esca","usciamo","uscite","escano"],
        "dire":["—","di'","dica","diciamo","dite","dicano"],
        "predire":["—","predici","predica","prediciamo","predite","predicano"],
        "disdire":["—","disdici","disdica","disdiciamo","disdite","disdicano"],
        "venire":["—","vieni","venga","veniamo","venite","vengano"],
        "salire":["—","sali","salga","saliamo","salite","salgano"],
        "apparire":["—","appari","appaia","appariamo","apparite","appaiano"],
        "scomparire":["—","scompari","scompaia","scompariamo","scomparite","scompaiano"],
        "finire":["—","finisci","finisca","finiamo","finite","finiscano"],
        "avere":["—","abbi","abbia","abbiamo","abbiate","abbiano"],
        "essere":["—","sii","sia","siamo","siate","siano"],
    }
    if v in mp: return mp[v]
    pres = PRES_IND[v]
    return ["—", pres[1], pres[2], pres[3], pres[4], pres[5]]

# Gerundio (key exceptions)
GERUND_EX = {
    "fare":"facendo","dire":"dicendo","porre":"ponendo","proporre":"proponendo","esporre":"esponendo","opporre":"opponendo",
    "condurre":"conducendo","tradurre":"traducendo","produrre":"producendo","introdurre":"introducendo",
    "bere":"bevendo"
}
def gerundio_presente(v):
    if v in GERUND_EX: return GERUND_EX[v]
    if v.endswith("are"): return v[:-3] + "ando"
    return v[:-3] + "endo"
def participio_presente(v):
    return v[:-3] + "ente"

# Aux helpers
def aux_present(aux): return ["ho","hai","ha","abbiamo","avete","hanno"] if aux=="avere" else ["sono","sei","è","siamo","siete","sono"]
def aux_imperf(aux):  return ["avevo","avevi","aveva","avevamo","avevate","avevano"] if aux=="avere" else ["ero","eri","era","eravamo","eravate","erano"]
def aux_rem(aux):     return ["ebbi","avesti","ebbe","avemmo","aveste","ebbero"] if aux=="avere" else ["fui","fosti","fu","fummo","foste","furono"]
def aux_fut(aux):     return ["avrò","avrai","avrà","avremo","avrete","avranno"] if aux=="avere" else ["sarò","sarai","sarà","saremo","sarete","saranno"]
def aux_cond(aux):    return ["avrei","avresti","avrebbe","avremmo","avreste","avrebbero"] if aux=="avere" else ["sarei","saresti","sarebbe","saremmo","sareste","sarebbero"]
def aux_cong_pres(aux): return ["che io abbia","che tu abbia","che lui/lei abbia","che noi abbiamo","che voi abbiate","che loro abbiano"] if aux=="avere" else ["che io sia","che tu sia","che lui/lei sia","che noi siamo","che voi siate","che loro siano"]
def aux_cong_impf(aux):  return ["che io avessi","che tu avessi","che lui/lei avesse","che noi avessimo","che voi aveste","che loro avessero"] if aux=="avere" else ["che io fossi","che tu fossi","che lui/lei fosse","che noi fossimo","che voi foste","che loro fossero"]

def compose(aux_forms, pp, essere=False):
    out = []
    for p,a in zip(IT_PRONOUNS, aux_forms):
        if essere:
            # plural agreement -> -i (masc. default)
            plural = any(k in a for k in ["siamo","siete","eravamo","eravate","saremo","sarete","fummo","foste"]) or a.endswith(("mo","te","no"))
            adj = (pp[:-1] + "i") if (plural and pp.endswith("o")) else pp
            out.append(f"{p} {a} {adj}")
        else:
            out.append(f"{p} {a} {pp}")
    return out

def congiuntivo_presente_full(v):
    return [f"che {p} {f}" for p,f in zip(IT_PRONOUNS, cong_pres(v))]

def congiuntivo_imperfetto_full(v):
    return congiuntivo_imperfetto(v)

def build_json(v):
    aux = AUX[v]
    essere = (aux == "essere")
    pp = PP[v]
    fr_disp, fr_ascii = FR_MAP[v]

    data = {
        "source_lang": "fr",
        "target_lang": "it",
        "source_lemma": fr_disp,
        "target_lemma": v,
        "meta": {
            "regularity": { "fr": "irrégulier", "it": "verbo irregolare" },
            "auxiliary": { "fr": "être" if essere else "avoir", "it": aux }
        },
        "pronouns": { "fr": FR_PRONOUNS, "it": IT_PRONOUNS },
        "Indicativo": {
            "Presente": with_pronouns(PRES_IND[v]),
            "Passato prossimo": compose(aux_present(aux), pp, essere=essere),
            "Imperfetto": imperfetto(v),
            "Trapassato prossimo": compose(aux_imperf(aux), pp, essere=essere),
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
            "Presente": congiuntivo_presente_full(v),
            "Passato": [f"{a} {pp}" for a in aux_cong_pres(aux)],
            "Imperfetto": congiuntivo_imperfetto_full(v),
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

# --- merge into decks/fr-it/index.json ---
index_path = os.path.join(DECK_DIR, "index.json")
try:
    with open(index_path, "r", encoding="utf-8") as f:
        idx = json.load(f)
    files = list(dict.fromkeys((idx.get("files") or []) + new_files))
except FileNotFoundError:
    files = new_files

with open(index_path, "w", encoding="utf-8") as f:
    json.dump({"files": files}, f, ensure_ascii=False, indent=2)

print(f"Generated {len(new_files)} irregulars and updated index.json.")
