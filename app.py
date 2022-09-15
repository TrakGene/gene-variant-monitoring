from flask import Flask, request, url_for, redirect, render_template  ## importing necessary libraries
import pickle  ## pickle for loading model
import pandas as pd  ## to convert the input data into a dataframe for giving as a input to the model
from sklearn import preprocessing
import requests
le = preprocessing.LabelEncoder()

'''url = 'http://localhost:8089/tables'
r = requests.get(url)
json = r.json()
json.keys()
data = pd.DataFrame(json['table_name')'''

app = Flask(__name__)  ## setting up flask name
filename = 'gsoc_data.csv'
data = pd.read_csv(filename, na_values = '-')

model = pickle.load(open("gsoc.pkl", "rb"))  ##loading model


@app.route('/')  ## Defining main index route
def home():
    return render_template("index.html")  ## showing index.html as homepage


@app.route('/predict', methods=['POST', 'GET'])  ## this route will be called when predict button is called
def predict():
    # int_features=[float(x) for x in request.form.values()]
    text1 = request.form['1']  ## Fetching each input field value one by one
    text2 = request.form['2']

    dicti = {'gene_name':text1, 'identifier':text2}
    df = pd.DataFrame(dicti, index = [0])
    
    test_data = pd.concat([data, df], axis=0, ignore_index=True)
    test_data['gene_name']=le.fit_transform(test_data['gene_name']).astype('str')
    test_data['identifier']=le.fit_transform(test_data['identifier']).astype('str')
    input_data = test_data.iloc[[-1], [0,1]]
    
    
    '''row_df = pd.DataFrame([pd.Series(
        [text1, text2])])        ### Creating a dataframe using all the values
    row_df = row_df.apply(le.fit_transform)
    print(row_df)'''
    
    output = model.predict(input_data)  ## Predicting the output
    
    if output == 0:
        return render_template('index.html',
                               pred='The gene variant is likely benign'.format(
                                   output))  ## Returning the message for use on the same index.html page
    elif output == 1:
        return render_template('index.html', pred='The gene variant is likely pathogenic'.format(output))
    else:
        return render_template('index.html', pred='The gene variant is uncertain'.format(output))


if __name__ == '__main__':
    app.run(debug=True)  ## Running the app as debug==True
