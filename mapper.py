cat > mapper.py <<'EOF'

#!/usr/bin/env python3

import sys
import csv

reader = csv.reader(sys.stdin)

for row in reader:

    if not row:
        continue

    # Ignorer l'en-tête
    if row[0] == "transaction_id":
        continue

    # Le fichier doit avoir 9 colonnes
    if len(row) != 9:
        continue

    client_id = row[2].strip()
    montant = row[5].strip()
    pays = row[7].strip()

    if client_id == "" or montant == "" or pays == "":
        continue

    try:
        float(montant)
    except ValueError:
        continue

    print("{}\t{}\t{}".format(client_id, montant, pays))
EOF
