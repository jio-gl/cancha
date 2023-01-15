# https://www.scrapingbee.com/curl-converter/python/
import requests, json

# pip install -U deep-translator
from deep_translator import GoogleTranslator

headers = {
    # Already added when you pass json= but not when you pass data=
    # 'Content-Type': 'application/json',
    'Authorization': 'Bearer sk-...',
}

input = '''''
A caccia di un nuovo commissario tecnico. Dopo aver accettato le dimissioni di Tite, 
una volta finita l'avventura al Mondiale in Qatar, il Brasile si è messo alla caccia di una nuova guida per la squadra nazionale. 
L'idea, fin da subito, è stata quella di puntare su un profilo di prima fascia, blasonato, motivo per il quale il primo allenatore contattato è stato Pep Guardiola. 
Il catalano ha ascoltato, ringraziato e rifiutato, vuole restare al Manchester City, con il quale ha rinnovato fino al 2025, per provare a vincere la Champions League.
'''

input = '''
Clamorose rivelazioni sulla rottura fra il Barcellona e le due ex-bandiere Leo Messi e Gerard Piqué sono state svelate oggi da El Periodico, che ha pubblicato gli screen delle chat interne della dirigenza del club catalano con l'avvocato Roman Gomez Ponti, Oscar Grau e il presidente Joseph Maria Bartomeu in prima linea nelle trattative, tutt'altro che semplici, per il rinnovo della Pulce e la riduzione dell'ingaggio del difensore. Lo scambio di messaggi arriva in risposta alle notizie uscite a mezzo stampa e per cui i dirigenti del Barcellona hanno incolpato l'ex-presidente Joan Laporta.

INSULTI SENZA FRENI A MESSI - È soprattutto l'avvocato Ramon Gomez Ponti ad usare la mano pesante con la stella argentina definita in un whatsapp prima "Topo di fogna" e poi "nano ormonato che deve al Barcellona la vita". All'epoca dei fatti Messi stava trattando il rinnovo, mai concretizzatisi con il club catalano, ma soprattutto c'era in ballo la trattativa per la riduzione degli ingaggi in seguito alla Pandemia Covid con Gomez che sottolinea la richiesta di Messi: "Abbiamo sofferto una dittatura di acquisti, cessioni e rinnovi solo per lui e ora mi scrive: "Abbassa gli stipendi di tutti, ma non a me e a Luis (Suarez)".
BORDATA ANCHE A PIQUE' - Gli insulti non si limitano però, come detto, al solo Messi, perché in altre conversazioni arrivano insulti importanti anche per Gerard Piqué, anche lui ex-capitano e oggi svincolatosi dal Barcellona a stagione in corso. Sempre Ramon Gomez Ponti parlando del suo contratto ribaidsce che: "Dobbiamo filtrare (ridurre) i suoi contratti. Continua ad avere pochi scrupoli ed è un grandissimo figlio di p...". 

FUTURO IN ARABIA CONTRO CR7? - Intanto, secondo il quotidiano catalano Mundo Deportivo, Messi avrebbe ricevuto un'offerta da 300 milioni di euro all'anno per andare a giocare in Arabia Saudita all'Al-Hilal, club rivale dell'Al-Nassr, dove gioca Cristiano Ronaldo. 
'''

print(input)
print('-'*80)
input = GoogleTranslator(source='auto', target='es').translate(input)
print(input)
print('-'*80)

inst = 'Paraphrase this news article and add more colourful opinions.' # and expand it with more colourful comments and opinions.'
inst = 'Parafrasear en estilo de Argentina y expandir la noticia con más opiniones coloridas.'

json_data = {
  "model": "text-davinci-edit-001",
  "input": input,
  "instruction": inst,
}


response = requests.post('https://api.openai.com/v1/edits', headers=headers, json=json_data)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"model": "text-davinci-003", "prompt": "Give the weather in Jun 25th, 1987 in Paris.", "temperature": 0, "max_tokens": 70}'
#response = requests.post('https://api.openai.com/v1/completions', headers=headers, data=data)

print(response.text)
print('-'*80)
text = json.loads(response.text)['choices'][0]['text']
print (text)
print('-'*80)
#texto = GoogleTranslator(source='auto', target='es').translate(text)

#print (texto)