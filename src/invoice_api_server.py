from flask import Flask, request, jsonify
from invoice_extractor import process_file
import os

cwd = os.getcwd()
app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

@app.route('/parse', methods=['POST'])
def parse():
    '''API endpoint to extract PDF data'''
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    f = request.files['file']
    
    if f.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not f.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are supported'}), 400

    try:
        input_file = os.path.join(cwd, f.filename)
        f.save(input_file)

        data = process_file(input_file)
        os.remove(input_file)

        return jsonify(data)
    
    except Exception as e:
        if 'input_file' in locals() and os.path.exists(input_file):
            os.remove(input_file)
        
        return jsonify({'error': f'Failed to process file: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
