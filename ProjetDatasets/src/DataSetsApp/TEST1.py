from hugchat import ChatBot
import logging


logging.basicConfig(level=logging.DEBUG)

# Remplacez les cookies par ceux récupérés dans votre navigateur
cookies = {
    "__stripe_mid": "e52c8844-c887-48b8-92a7-e025ffc5fa15d00beb",
    "__stripe_sid": "237cef95-cc3a-4c20-83ab-f0965c1e112112a568",
    "_ga": "GA1.1.595100178.1701171646",
    "_ga_8Q63TH4CSL": "GS1.1.1713261232.20.0.1713261232.60.0.0",
    "aws-waf-token": "8f9777b6-1694-4d1a-a7f3-2d6edab5b486:CwoAkhk8Lu0UAQAA:jnue2acFVb8Zrzr7dMsDW7MiQgthMZ4CbDEIxuqnGrChU/LHtLiLR7cwlhTTWekGCNJtVQNjEWLp5xP1ZMqPZfVsbyajgJ8paZrRdpln5PxTpZUZiaVHUVTuxXffmzJKOhXow7Yu73tPq97CuwlsfGHD15e05ns/db7gLx3qPxfHRqTMLiz+jmywYboELYEWW16MDOnWKCT5i+KephFMatYRjgKn9+jL8kt5U4DQv2WyI6MtyCUVbw0ZjQz4PHgXlFc=",  # Remplacez par la valeur complète
    "token": "riPxAtqGXVWPcHdNyoUSkeRALvXvqnsFCjcAypfoufyUIQArLymINZSwmUNIvPPCVkEaKtskpjkezHRnmDfFrzCiPdvPBUPuxIecWMKcvcHxBcFgIRlYVEppiFWeErjB",
    "hf-chat": "803bcb69-f239-4ba1-92d7-d058995289a4"
}

try:
    # Initialisation du chatbot avec les cookies
    bot = ChatBot(cookies=cookies)
    
    # Récupération des modèles disponibles
    models = bot.get_remote_llms()
    print("Modèles récupérés avec succès :", models)
except Exception as e:
    # Affichage des erreurs en cas de problème
    print("Erreur lors de la récupération des modèles :", e)
