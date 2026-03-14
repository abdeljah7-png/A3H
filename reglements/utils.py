from num2words import num2words


def montant_en_lettres(montant):

    dinars = int(montant)
    millimes = int(round((montant - dinars) * 1000))

    texte_dinars = num2words(dinars, lang="fr")

    return f"{texte_dinars} dinars {millimes:03d} millimes"