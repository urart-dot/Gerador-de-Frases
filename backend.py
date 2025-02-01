from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Dicionário extenso com palavras variadas (apenas algumas para exemplificar)
mapeamento = {
    "pt": {
        "31": "Lua", "99": "infinito", "19": "estrelas", "08": "neve", "59": "céu",
        "45": "amor", "23": "sol", "17": "flor", "87": "vento", "12": "chama", 
        "56": "mar", "77": "terra", "64": "paz", "29": "sombra", "11": "reflexo",
        "35": "chuva", "50": "montanha", "38": "sonho", "41": "aurora", "93": "escuro"
    },
    "en": {
        "31": "Moon", "99": "infinity", "19": "stars", "08": "snow", "59": "sky",
        "45": "love", "23": "sun", "17": "flower", "87": "wind", "12": "flame",
        "56": "sea", "77": "earth", "64": "peace", "29": "shadow", "11": "reflection",
        "35": "rain", "50": "mountain", "38": "dream", "41": "dawn", "93": "dark"
    }
}

# Palavra genérica de fallback
fallback = {
    "pt": "mistério",
    "en": "mystery"
}

# Templates de frases variadas
templates = [
    "O que está oculto sob o {0} revela-se nas {1} que dançam no {2}.",
    "Em um céu de {0}, as {1} se espalham como {2}.",
    "Sob o manto de {0}, as {1} brilham intensamente sobre o {2}.",
    "O {0} brilha, enquanto as {1} iluminam o {2}.",
    "Entre as {0}, as {1} encontram seu caminho pelo {2}.",
    "As {0} e as {1} se encontram no {2} com um toque de {3}.",
    "Nas {0} do {1}, o {2} se transforma em {3}.",
    "Enquanto o {0} repousa, as {1} se agitam ao sabor do {2}."
]

def codificar_numero(numero, idioma="pt"):
    if idioma not in ['pt', 'en']:
        return "Idioma não suportado."

    partes = [numero[i:i+2] for i in range(0, len(numero), 2)]
    dicionario = mapeamento[idioma]

    # Substitui códigos não encontrados por uma palavra genérica
    palavras = []
    for parte in partes:
        if parte in dicionario:
            palavras.append(dicionario[parte])
        else:
            palavras.append(fallback[idioma])  # Usa a palavra de fallback

    # Garantir que o número de palavras seja suficiente para os templates
    while len(palavras) < max(template.count("{") for template in templates):
        palavras.append(fallback[idioma])  # Adiciona fallback

    # Escolher um template aleatório
    template = random.choice(templates)
    return template.format(*palavras)

@app.route('/gerar-frase')
def gerar_frase():
    numero = request.args.get('numero', '')
    idioma = request.args.get('idioma', 'pt')

    # Verificar se o número tem 11 dígitos e é composto apenas por números
    numero = numero.strip()
    if not numero.isdigit() or len(numero) != 11:
        return jsonify({"erro": "Número inválido. Insira um número de 11 dígitos."}), 400

    frase = codificar_numero(numero, idioma=idioma)
    return jsonify({"frase": frase})

if __name__ == '__main__':
    app.run(debug=True)
