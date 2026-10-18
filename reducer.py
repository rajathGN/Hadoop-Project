cat > reducer.py <<'EOF'

#!/usr/bin/env python3

import sys

client_courant = None
nb_transactions = 0
montant_total = 0.0
pays_counts = {}


def afficher_resultat(client_id, nb, total, counts):

    if client_id is None or nb == 0:
        return

    montant_moyen = total / nb

    pays_habituel = max(
        sorted(counts.keys()),
        key=lambda pays: counts[pays]
    )

    print("{}\t{}\t{:.2f}\t{:.2f}\t{}".format(
        client_id,
        nb,
        total,
        montant_moyen,
        pays_habituel
    ))


for line in sys.stdin:

    line = line.strip()

    if not line:
        continue

    parts = line.split("\t")

    if len(parts) != 3:
        continue

    client_id = parts[0]
    montant_str = parts[1]
    pays = parts[2]

    try:
        montant = float(montant_str)
    except ValueError:
        continue

    if client_courant is not None and client_id != client_courant:

        afficher_resultat(
            client_courant,
            nb_transactions,
            montant_total,
            pays_counts
        )

        nb_transactions = 0
        montant_total = 0.0
        pays_counts = {}

    client_courant = client_id

    nb_transactions += 1
    montant_total += montant

    if pays not in pays_counts:
        pays_counts[pays] = 0

    pays_counts[pays] += 1


afficher_resultat(
    client_courant,
    nb_transactions,
    montant_total,
    pays_counts
)
EOF
