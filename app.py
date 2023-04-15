from flask import Flask, render_template, redirect, request
import pickle
import pandas as pd

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        model = pickle.load(open('model_.pkl', 'rb'))
        age=0
        bmi=0
        try:
               age = float(request.form['age'])
               bmi = float(request.form['bmi'])
        except(Exception):
               result='Age and BMI are must be numeric' 
               return render_template('index.html',prediction=result)      
               
        
        children =int(request.form['children'])
        sex = request.form['sex']
        smoker = request.form['smoker']
        region = request.form['region']
        
        if sex == 'Male':
                sex_female = 0
                sex_male = 1
        else:
                sex_female = 1
                sex_male = 0
        if smoker == 'Yes':
                smoker_no = 0
                smoker_yes = 1
        else:
                smoker_no = 1
                smoker_yes = 0
        if region == 'North East':
                region_northeast = 1
                region_northwest = 0
                region_southeast = 0
                region_southwest = 0
        elif region == 'North West':
                region_northeast = 0
                region_northwest = 1
                region_southeast = 0
                region_southwest = 0
        elif region == 'South East':
                region_northeast = 0
                region_northwest = 0
                region_southeast = 1
                region_southwest = 0
        else:
                region_northeast = 0
                region_northwest = 0
                region_southeast = 0
                region_southwest = 1

        x=[age, bmi, children,sex_female,sex_male,smoker_no,smoker_yes,region_northeast,region_northwest,region_southeast,region_southwest]
        output = model.predict(pd.DataFrame([x],columns=['age', 'bmi', 'children', 'sex_female', 'sex_male', 'smoker_no',
       'smoker_yes', 'region_northeast', 'region_northwest',
       'region_southeast', 'region_southwest']))[0]
        output=round(float(output),2) 
        result = 'Your Insurance is {}'.format(output)
        return render_template('index.html', prediction=result)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
