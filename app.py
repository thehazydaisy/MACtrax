from flask import Flask, render_template, request, send_file
import parser   # Import the parser module directly

import subprocess
subprocess.call(['pip', 'list'])  # Print installed packages

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        choice = request.form['choice']
        if choice == 'direct':
            urls_input = request.form['urls']
            urls = [url.strip() for url in urls_input.split(',')]
        elif choice == 'file':
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                urls = [line.strip() for line in uploaded_file.readlines()]
            else:
                return "No file selected."
        else:
            return "Invalid choice."

        output_file = 'extracted_data.txt'
        success_file = 'successful_urls.txt' 
        parser.parse_mac_addresses_and_dates(urls, output_file, success_file) 
        return send_file(output_file, as_attachment=True)
    else:
        return render_template('index.html') 

if __name__ == '__main__':
    app.run(debug=True)