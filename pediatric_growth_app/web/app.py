from flask import Flask, render_template, request, jsonify
import sys
sys.path.append('..')
from growth_assessment import comprehensive_assessment

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/assess', methods=['POST'])
def assess():
    try:
        data = request.json
        gender = data.get('gender')
        age_years = int(data.get('age_years', 0))
        age_months = int(data.get('age_months', 0))
        height = float(data.get('height'))
        weight = float(data.get('weight'))
        
        result = comprehensive_assessment(gender, age_years, age_months, height, weight)
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
