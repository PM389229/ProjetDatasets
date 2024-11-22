import requests
import json
import re

# Définir les cookies
cookies = {
    "__stripe_mid": "e52c8844-c887-48b8-92a7-e025ffc5fa15d00beb",
    "__stripe_sid": "237cef95-cc3a-4c20-83ab-f0965c1e112112a568",
    "_ga": "GA1.1.595100178.1701171646",
    "_ga_8Q63TH4CSL": "GS1.1.1713261232.20.0.1713261232.60.0.0",
    "aws-waf-token": "8f9777b6-1694-4d1a-a7f3-2d6edab5b486:CwoAkhk8Lu0UAQAA:jnue2acFVb8Zrzr7dMsDW7MiQgthMZ4CbDEIxuqnGrChU/LHtLiLR7cwlhTTWekGCNJtVQNjEWLp5xP1ZMqPZfVsbyajgJ8paZrRdpln5PxTpZUZiaVHUVTuxXffmzJKOhXow7Yu73tPq97CuwlsfGHD15e05ns/db7gLx3qPxfHRqTMLiz+jmywYboELYEWW16MDOnWKCT5i+KephFMatYRjgKn9+jL8kt5U4DQv2WyI6MtyCUVbw0ZjQz4PHgXlFc=",
    "token": "riPxAtqGXVWPcHdNyoUSkeRALvXvqnsFCjcAypfoufyUIQArLymINZSwmUNIvPPCVkEaKtskpjkezHRnmDfFrzCiPdvPBUPuxIecWMKcvcHxBcFgIRlYVEppiFWeErjB",
    "hf-chat": "803bcb69-f239-4ba1-92d7-d058995289a4"
}

# Faire la requête
response = requests.get("https://huggingface.co/chat/__data.json", cookies=cookies)

# Vérifier si la requête a réussi
if response.status_code == 200:
    print("Requête réussie. Vérifions le contenu JSON...")

    # Vérifier le type de contenu
    content_type = response.headers.get("Content-Type", "")
    print("Content-Type :", content_type)

    # Afficher la réponse brute pour diagnostic
    print("Contenu brut :")
    print(response.text)

    # Essayer d'extraire le JSON
    try:
        data = response.json()
        print("Données JSON analysées :")
        print(json.dumps(data, indent=2))
    except ValueError as e:
        print("Erreur JSONDecodeError :", e)

        # Extraire manuellement le JSON si nécessaire
        match = re.search(r"\{.*\}", response.text, re.DOTALL)
        if match:
            valid_json = match.group(0)
            data = json.loads(valid_json)
            print("JSON extrait et analysé :")
            print(json.dumps(data, indent=2))
        else:
            print("Impossible de trouver un JSON valide dans la réponse.")
else:
    print("Erreur HTTP :", response.status_code)
