import csv

# FICHIERS
input_file = "/Users/rajath077/Desktop/semestre 11/hadood/projet/donnees_moyen/projet/transactions.csv"


clean_file = "/Users/rajath077/Desktop/semestre 11/hadood/projet/rendu/clean_files/transactions_clean.csv"

rejects_file = "/Users/rajath077/Desktop/semestre 11/hadood/projet/rendu/clean_files/transactions_rejects.csv"


"""
mal formée            -> reject
transaction_id vide   -> reject
doublon               -> reject
client_id vide        -> reject
pays vide             -> reject
montant vide          -> reject
montant non numérique -> reject
montant négatif       -> conservé dans clean + signalé
"""


# COMPTEURS

stats = {
    "total": 0,
    "mal_formees": 0,
    "transaction_id_manquants": 0,
    "client_id_manquants": 0,
    "pays_manquants": 0,
    "montants_manquants": 0,
    "montants_invalides": 0,
    "montants_negatifs": 0,
    "doublons": 0,
    "valides": 0
}

# Pour détecter les transaction_id déjà rencontrés
seen_transactions = set()


# LECTURE / NETTOYAGE

with open(input_file, "r", encoding="utf-8") as infile, \
     open(clean_file, "w", encoding="utf-8", newline="") as clean_out, \
     open(rejects_file, "w", encoding="utf-8", newline="") as rejects_out:

    reader = csv.reader(infile)
    writer_clean = csv.writer(clean_out)
    writer_rejects = csv.writer(rejects_out)

    # Lire l'en-tête
    header = next(reader)

    # Écrire l'en-tête dans les deux fichiers
    writer_clean.writerow(header)
    writer_rejects.writerow(header + ["raison_rejet"])

    for row in reader:

        stats["total"] += 1

        # 1. Ligne mal formée

        if len(row) != 9:
            stats["mal_formees"] += 1
            writer_rejects.writerow(row + ["ligne mal formee"])
            continue

        (
            transaction_id,
            horodatage,
            client_id,
            marchand_id,
            categorie,
            montant_str,
            devise,
            pays,
            canal
        ) = row

        rejetee = False
        raisons_rejet = []

        # 2. transaction_id

        if not transaction_id.strip():
            stats["transaction_id_manquants"] += 1
            rejetee = True
            raisons_rejet.append("transaction_id manquant")

        elif transaction_id in seen_transactions:
            stats["doublons"] += 1
            rejetee = True
            raisons_rejet.append("doublon transaction_id")

        else:
            seen_transactions.add(transaction_id)

        # 3. client_id

        if not client_id.strip():
            stats["client_id_manquants"] += 1
            rejetee = True
            raisons_rejet.append("client_id manquant")

        # 4. pays

        if not pays.strip():
            stats["pays_manquants"] += 1
            rejetee = True
            raisons_rejet.append("pays manquant")

        # 5. montant

        if not montant_str.strip():
            stats["montants_manquants"] += 1
            rejetee = True
            raisons_rejet.append("montant manquant")

        else:
            try:
                montant = float(montant_str)

                # On garde les montants négatifs :
                # ils seront analysés ensuite dans Hive.
                if montant < 0:
                    stats["montants_negatifs"] += 1

            except ValueError:
                stats["montants_invalides"] += 1
                rejetee = True
                raisons_rejet.append("montant non numerique")

        # 6. Écriture du résultat


        if rejetee:
            writer_rejects.writerow(
                row + ["; ".join(raisons_rejet)]
            )

        else:
            writer_clean.writerow(row)
            stats["valides"] += 1



# RAPPORT


print("_" * 55)
print("RAPPORT DE QUALITE DES DONNEES - SUJET B")
print("_" * 55)

print(f"Nombre total de transactions : {stats['total']}")
print(f"Lignes mal formees           : {stats['mal_formees']}")
print(f"Transaction_id manquants     : {stats['transaction_id_manquants']}")
print(f"Client_id manquants          : {stats['client_id_manquants']}")
print(f"Pays manquants               : {stats['pays_manquants']}")
print(f"Montants manquants           : {stats['montants_manquants']}")
print(f"Montants non numeriques      : {stats['montants_invalides']}")
print(f"Montants negatifs signales   : {stats['montants_negatifs']}")
print(f"Doublons                     : {stats['doublons']}")

print("-" * 55)

print(f"Lignes conservees en clean   : {stats['valides']}")
print(f"Lignes rejetees              : {stats['total'] - stats['valides']}")

print("" * 55)
