import time
import requests

TOKEN = '8642596911:AAFXqw8l1z7_VlAWtk2eh220BzrVKSxAvT0'
CHAT_ID = '8466838584'
ANTHROPIC_KEY = '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'

alertes = set()

def analyser(situation):
    try:
        r = requests.post('https://api.anthropic.com/v1/messages',
            headers={
                'x-api-key': ANTHROPIC_KEY,
                'anthropic-version': '2023-06-01',
                'content-type': 'application/json'
            },
            json={
                'model': 'claude-sonnet-4-6',
                'max_tokens': 300,
                'messages': [{'role': 'user', 'content': f'Tu es Colos+, assistant portefeuille de Jean-Luc. Portefeuille Bitpanda: P1 Or (XAU, règle absolue no-sell), P2 ETFs (DBXW/PSWD/VWCE), P3 Actions IA (NVDA/MU/EQQQ/GOOGL). PRU MU: $779, PRU NVDA: $189, PRU GOOGL: $340. Alertes MU: stop $950, partiel $1500, sortie $1800. Situation actuelle: {situation}. Donne une analyse courte et une recommandation claire et directe en français, max 5 lignes.'}]
            }, timeout=20)
        return r.json()['content'][0]['text']
    except Exception as e:
        return situation

def envoyer(msg):
    try:
        requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage',
                      json={'chat_id': CHAT_ID, 'text': msg})
    except:
        pass

def get_prix(symbol):
    try:
        r = requests.get(f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}',
                        headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        return r.json()['chart']['result'][0]['meta']['regularMarketPrice']
    except:
        return None

def verifier():
    mu = get_prix('MU')
    nvda = get_prix('NVDA')

    if mu:
        print(f'MU=${mu:.2f}', end='  ')
        if mu <= 950 and 'MU-950' not in alertes:
            alertes.add('MU-950')
            analyse = analyser(f'MU (Micron Technology) vient de passer sous $950 a ${mu:.2f}. Stop psychologique atteint. Gap comble = these invalidee.')
            envoyer(f'🔴 COLOS+ ALERTE MU\n\n{analyse}')
        if mu > 950: alertes.discard('MU-950')

        if mu >= 1500 and 'MU-1500' not in alertes:
            alertes.add('MU-1500')
            analyse = analyser(f'MU (Micron Technology) atteint $1500 a ${mu:.2f}. Seuil prise partielle 30%.')
            envoyer(f'🟡 COLOS+ ALERTE MU\n\n{analyse}')
        if mu < 1500: alertes.discard('MU-1500')

        if mu >= 1800 and 'MU-1800' not in alertes:
            alertes.add('MU-1800')
            analyse = analyser(f'MU (Micron Technology) atteint $1800 a ${mu:.2f}. Seuil sortie totale.')
            envoyer(f'🟢 COLOS+ ALERTE MU\n\n{analyse}')
        if mu < 1800: alertes.discard('MU-1800')

    if nvda:
        print(f'NVDA=${nvda:.2f}')
        if nvda < 180 and 'NVDA-180' not in alertes:
            alertes.add('NVDA-180')
            analyse = analyser(f'NVDA (NVIDIA) passe sous $180 a ${nvda:.2f}. Opportunite DCA potentielle. PRU actuel $189.')
            envoyer(f'🟡 COLOS+ ALERTE NVDA\n\n{analyse}')
        if nvda >= 180: alertes.discard('NVDA-180')

envoyer('⚡ Colos+ IA actif 24h/24\nAlertes avec analyse Claude integree')
print('Surveillance IA demarree...')
while True:
    verifier()
    time.sleep(60)
