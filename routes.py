from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import os


main = Blueprint('main', __name__)


DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), 'security-controls.xlsx')


def load_data():
    try:
        df = pd.read_excel(DATA_FILE_PATH)
        return df
    except FileNotFoundError:
        return pd.DataFrame() 


@main.route('/')
def homepage():
    return render_template('index.html', title='Cloudhub Security Hub')

@main.route('/checklist', methods=['GET'])
def checklist():
    df = load_data()
    
    
    offset = int(request.args.get('offset', 0))
    limit = 10  
    
    
    controls = df.iloc[offset:offset + limit].to_dict(orient='records')
    
    
    all_controls_loaded = len(controls) < limit

    return render_template('checklist.html', controls=controls, all_controls_loaded=all_controls_loaded)




@main.route('/checklist/show_more', methods=['GET'])
def show_more_controls():
    
    try:
        df = load_data()

        
        offset = int(request.args.get('offset', 0))
        limit = 10  

        
        controls = df.iloc[offset:offset + limit].to_dict(orient='records')

        
        all_loaded = len(df) <= offset + limit

        return jsonify({
            'controls': controls,
            'all_loaded': all_loaded
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/checklist/search', methods=['POST'])
def search_controls():
    search_query = request.form.get('search_query', '').lower()  
    df = load_data()
    
    
    filtered_controls = df[df['Security Level'].str.lower().str.contains(search_query)].to_dict(orient='records')

    return jsonify(filtered_controls)


@main.route('/error')
def error_page():
    return render_template('error.html', message="An error occurred.")
