from flask import Flask, render_template, request, send_file
from googleapiclient.discovery import build
import pandas as pd
import os
import io

app = Flask(__name__)

def google_search(search_term, api_key, cse_id, num_results, **kwargs):
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=search_term, cx=cse_id, num=num_results, **kwargs).execute()
        return res.get('items', [])  # Return empty list if 'items' is not present
    except Exception as e:
        print(f"Error during Google Search: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        search_query = request.form['query']
        num_results = int(request.form['num_results']) # Get num_results from the form
        api_key = os.environ.get('GOOGLE_API_KEY')
        cse_id = os.environ.get('GOOGLE_CSE_ID')

        if not api_key or not cse_id:
            return "Error: API Key or CSE ID not configured."

        search_results = google_search(search_query, api_key, cse_id, num_results)

        if search_results is not None:
            for result in search_results:
                results.append({
                    'Title': result.get('title', ''),
                    'Link': result.get('link', ''),
                    'Snippet': result.get('snippet', '')
                })

    return render_template('index.html', results=results)

@app.route('/download', methods=['POST'])
def download():
    # Get data from the form (same as in the index route)
    search_query = request.form['query']
    num_results = int(request.form['num_results'])
    api_key = os.environ.get('GOOGLE_API_KEY')
    cse_id = os.environ.get('GOOGLE_CSE_ID')
    search_results = google_search(search_query, api_key, cse_id, num_results)
    data = []

    if search_results:
        for result in search_results:
            data.append({
                'Title': result.get('title', ''),
                'Link': result.get('link', ''),
                'Snippet': result.get('snippet', '')
            })

        df = pd.DataFrame(data)
        excel_file = io.BytesIO()
        df.to_excel(excel_file, index=False)
        excel_file.seek(0)  # Rewind to the beginning of the file

        return send_file(
            excel_file,
            as_attachment=True,
            download_name=f"google_search_results_{search_query.replace(' ', '_')}.xlsx",
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    else:
         return "No results to download."

if __name__ == '__main__':
    app.run(debug=True) # Use debug=True for development