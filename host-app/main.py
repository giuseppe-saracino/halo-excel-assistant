import json
from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)

# Mock per funzioni Excel (da function-db)
FUNCTIONS_DB = {}

def load_functions():
    global FUNCTIONS_DB
    try:
        with open('../function-db/functions_it.json', 'r', encoding='utf-8-sig') as f:
            FUNCTIONS_DB = json.load(f)['functions']
        print('Funzioni caricate:', len(FUNCTIONS_DB))
    except Exception as e:
        print('Errore caricamento DB:', e)

@app.route('/excelContext', methods=['POST'])
def excel_context():
    data = request.json
    formula = data.get('formula', '')
    print('Ricevuto:', formula)
    
    # Parsing semplice: estrai nome funzione
    func_name = ''
    if '=' in formula:
        parts = formula[1:].split('(')[0].strip().upper()
        func_name = parts
    
    if func_name in FUNCTIONS_DB:
        func = FUNCTIONS_DB[func_name]
        response = {
            'function': func_name,
            'syntax': func['syntax'],
            'description': func['description'],
            'example': func['example']
        }
        # QUI: mock overlay Halo
        print('Manda a Halo:', response)
    else:
        response = {'error': 'Funzione non trovata'}
    
    return jsonify(response)

if __name__ == '__main__':
    load_functions()
    print('Host avviato su http://localhost:5000')
    app.run(debug=True, port=5000)
