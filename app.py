from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)


DATA_FILE = 'security-controls.xlsx'

def read_data(DATA_FILE):
    
    
    df = pd.read_excel(DATA_FILE)
    df['App Name'] = ['App' + str(i + 1) for i in range(len(df))]
    df.rename(columns={
        'Security Level': 'Type',
        'Level': 'Level',
        'Cloud Adoption Framework (CAF) capability': 'Control Areas',
        'Layer 2 Controls (Generic)': 'Layer 2 Controls (Generic)',
        'Controls': 'AWS Controls',
        'AWS-Sub-Controls': 'AWS Sub-Controls'
    }, inplace=True)
    return df.to_dict(orient='records')
    

def write_data(DATA_FILE, data_frame):
    
    data_frame.to_excel(DATA_FILE, index=False)

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/checklist', methods=['GET'])
def checklist():
    
    try:
        
        data = read_data(DATA_FILE)
        df = pd.DataFrame(data)
        df = df.fillna('N/A')
        search_query = request.args.get('search', '')

        
        if search_query:
            filtered_controls = df[df['Level'].str.contains(search_query, case=False, na=False)]
        else:
            filtered_controls = df
        
        
        filtered_controls_data = filtered_controls.to_dict(orient='records')

        
        initial_display_count = 10
        limited_controls = filtered_controls_data[:initial_display_count]

        
        all_controls_loaded = len(filtered_controls_data) <= initial_display_count

        
        return render_template('checklist.html', controls=limited_controls, all_controls_loaded=all_controls_loaded, search_query=search_query)

    except FileNotFoundError:
        return "Data file not found.", 404
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.route('/checklist/search', methods=['GET'])
def search_checklist():
    try:
        
        data = read_data(DATA_FILE)
        df = pd.DataFrame(data)
        df = df.fillna('N/A')  


        search = request.args.get('search', '').strip().lower()

        
        if search:
            controls = df[df['Level'].str.lower().str.contains(search)]
        else:
            controls = df

        
        controls_data = controls.to_dict('records')

        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  
            return jsonify(controls_data)  

        
        all_controls_loaded = len(controls_data) <= 10
        return render_template('checklist.html', controls=controls_data[:10], all_controls_loaded=all_controls_loaded)

    except Exception as e:
        print(f"Error in /checklist/search: {str(e)}")
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

    
@app.route('/checklist/show_more', methods=['GET'])
def show_more():
    offset = int(request.args.get('offset', 0))
    search = request.args.get('search', '')

    
    df = pd.read_excel(DATA_FILE)
    
    df['App Name'] = ['App' + str(i + 1) for i in range(len(df))]
    df.rename(columns={
        'Security Level': 'Type',
        'Level': 'Level',
        'Cloud Adoption Framework (CAF) capability': 'Control Areas',
        'Layer 2 Controls (Generic)': 'Layer 2 Controls (Generic)',
        'Controls': 'AWS Controls',
        'AWS-Sub-Controls': 'AWS Sub-Controls'
        }, inplace=True)

    
    if search:
        df = df[df['Type'].str.contains(search, case=False)]

    
    controls_data = df.iloc[offset:offset + 10].fillna('N/A').to_dict(orient='records')

    
    all_loaded = offset + 10 >= len(df)

    
    return jsonify({
        'controls': controls_data,
        'all_loaded': all_loaded
    })


if __name__ == '__main__':
    app.run(debug=True, port=5001)
