# 🔹 Klíčová slova pro filtrování článků
KEYWORDS = [
    "armáda české republiky", "armáda", "armády", "armádní", "armádních",
    "vojáci", "vojáků", "vojákům", "voják",
    "AČR", "obrana", "ministerstvo obrany", "vojenské", "vojenská", "vojenští",
    "vojenské cvičení", "armadní cvičení",
    "česká armáda", "generální štáb", "gš ačr",
    "náčelník generálního štábu", "mo čr", "ministerstvo obrany čr",
    "vojenská policie", "vojenské zpravodajství", "vojenské správy",
    "vojenský útvar", "vojenská akademie", "aktivní záloha",
    "vojenská služba", "branná povinnost", "vojenský rozpočet",
    "pozemní síly", "chemici", "ženisté", "spojaři", "logistika armády",
    "vojenský výcvik", "vojenské školy", "vojenské stipendium",
    "vojenský lékař"
]

def contains_keywords(text):
    """Ověří, zda text obsahuje některé z klíčových slov"""
    return any(keyword.lower() in text.lower() for keyword in KEYWORDS)