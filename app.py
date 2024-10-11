from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)


DATA_FILE = 'security-controls.xlsx'

def read_data(DATA_FILE):
    if os.path.exists(DATA_FILE):
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
        print(df.to_dict(orient='records'))
        return df.to_dict(orient='records')
    else:
        raise FileNotFoundError("Data file not found.")
    

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


@app.route('/checklist/update', methods=['GET', 'POST'])
def update_checklist():
    if request.method == 'POST':
        try:
            
            type_data = request.form.getlist('type[]')
            level_data = request.form.getlist('level[]')
            control_area_data = request.form.getlist('control_area[]')
            layer2_controls_data = request.form.getlist('layer2_controls[]')
            aws_controls_data = request.form.getlist('aws_controls[]')
            aws_sub_controls_data = request.form.getlist('aws_sub_controls[]')
            
            
            df = pd.read_excel(DATA_FILE) 
            
            print("Type of df after reading file:", type(df))
            
            if isinstance(df, list):
                print("Error: df is a list, expected a DataFrame")
                return "Error: Data from file is not a valid DataFrame", 500
            
            new_app_index = len(df) + 1

            
            new_rows = []
            for i in range(len(type_data)):
                new_rows.append({
                    'Security Level': type_data[i] if type_data[i] else 'N/A',  
                    'Level': level_data[i] if level_data[i] else 'N/A',
                    'Cloud Adoption Framework (CAF) capability': control_area_data[i] if control_area_data[i] else 'N/A',  
                    'Layer 2 Controls (Generic)': layer2_controls_data[i] if layer2_controls_data[i] else 'N/A',
                    'Controls': aws_controls_data[i] if aws_controls_data[i] else 'N/A',
                    'AWS-Sub-Controls': aws_sub_controls_data[i] if aws_sub_controls_data[i] else 'N/A'
                })
            print(type_data, level_data, control_area_data, layer2_controls_data, aws_controls_data, aws_sub_controls_data)
            
            new_df = pd.DataFrame(new_rows)
            print(new_rows)
            print(new_df)
            
            expected_columns = ['Level', 'Security Level', 'Cloud Adoption Framework (CAF) capability', 
                                'Layer 2 Controls (Generic)', 'Controls', 'AWS-Sub-Controls']
            
            if set(new_df.columns).issubset(set(df.columns)) and not new_df.empty:
                df = pd.concat([df, new_df], ignore_index=True)
            else:
                print("New DataFrame has incorrect columns or is empty")

            df[expected_columns].to_excel(DATA_FILE, index=False)

            
            df.to_excel(DATA_FILE, index=False)

            return redirect(url_for('update_checklist', success=True))
        except Exception as e:
            return str(e), 500

    
    app_count = len(pd.read_excel(DATA_FILE)) + 1
    success = request.args.get('success', False)
    return render_template('update-checklist.html', app_count=app_count, success=success)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
