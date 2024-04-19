from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/medical-records-form')
def medical_records_form():
    return render_template('medical_records_form.html')

@app.route('/patients-form')
def patients_form():
    return render_template('patient_form.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
