# https://www.scrapingbee.com/curl-converter/python/
import requests, json

from configuration import all_prompts

prompts = all_prompts['cancha24']

def transformNews( input_text, prompt ):

    headers = {
        # Already added when you pass json= but not when you pass data=
        # 'Content-Type': 'application/json',
        'Authorization': 'Bearer sk-...',
    }

    pr = prompt #'Parafrasear en estilo argentino el siguiente texto y expandirlo con opiniones coloridas y divertidas pero sin contenido politico:'

    input = input_text

    pr = pr + " '" + input + "'"
    # limit to 1400 tokens
    pr = ' '.join( pr.split(' ')[:1400] )

    json_data = {
        'model': 'text-davinci-003',
        'prompt': pr,
        'temperature': 0.7,
        'max_tokens': 2700,
    }

    response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=json_data)

    # Note: json_data will not be serialized by requests
    # exactly as it was in the original request.
    #data = '{"model": "text-davinci-003", "prompt": "Give the weather in Jun 25th, 1987 in Paris.", "temperature": 0, "max_tokens": 70}'
    #response = requests.post('https://api.openai.com/v1/completions', headers=headers, data=data)

    print(response.text)
    #print (json.loads(response.text)['choices'][0]['text'])
    resp = json.loads(response.text)['choices'][0]['text']
    if resp.startswith("'"):
        resp = resp[1:]
    if resp.endswith("'"):
        resp = resp[:-1]

    return resp




#prompt_body = prompts['body'] #'Parafrasear en estilo argentino el siguiente texto y expandirlo con opiniones coloridas, realistas, virales y populares pero sin contenido politico para hacer la noticia mas viral:'
#prompt_title = prompts['title']
#input = "PSG, Messi verso il rinnovo: ecco quando firma" #"Messi, l'Inter Miami sogna ancora. Neville: 'Perché no? Potrebbe succedere'"
#prompt = 'Parafrasear en estilo argentino el siguiente titulo y hacerlo mas viral y llamativo:'

if __name__ == '__main__':
    #prompt = prompt_body
    #print (transformNews(input, prompt=prompt))
    pass