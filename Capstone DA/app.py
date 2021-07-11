from flask import Flask,render_template,url_for,request, jsonify
import re
import pandas as pd
import spacy
from spacy import displacy
import en_core_web_md
import json 

# @TASK : Load model bahasa 
nlp = en_core_web_md.load()
# END OF TASK 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/process',methods=["POST"])
def process():
    if request.method == 'POST':
        choice = request.form['taskoption']
        rawtext = request.form['rawtext']
        doc = nlp(rawtext)
        d = []
        
        if (len(doc.ents) > 0):
            for ent in doc.ents:
                d.append((ent.label_, ent.text))
                df = pd.DataFrame(d, columns=['category', 'value'])

                # @TASK : COMPLETE THE FOLLOWING CODES
                ORG_named_entity = df[(df['category'] == 'ORG')]['value'] # Subset semua entitas dengan kategori 'ORG'
                PERSON_named_entity = df[(df['category'] == 'PERSON')]['value'] # Subset semua entitas dengan kategori 'PERSON'
                GPE_named_entity = df[(df['category'] == 'GPE')]['value'] # Subset semua entitas dengan kategori 'GPE'
                MONEY_named_entity = df[(df['category'] == 'MONEY')]['value'] # Subset semua entitas dengan kategori 'MONEY'
                # END OF TASK 

            if choice == 'organization':
                results = ORG_named_entity
                num_of_results = len(results)
            elif choice == 'person':
                results = PERSON_named_entity
                num_of_results = len(results)
            elif choice == 'geopolitical':
                results = GPE_named_entity
                num_of_results = len(results)
            elif choice == 'money':
                results = MONEY_named_entity
                num_of_results = len(results)
            elif choice == 'Select Category':
                results = pd.DataFrame()
                num_of_results = len(results)
        else:
            results = pd.DataFrame()
            num_of_results = len(results)

    return render_template("index.html",results=results,num_of_results = num_of_results, original_text = rawtext)


@app.route('/get_entities',methods=['POST'])
def get_entities():
    # ambil data dari json yang diterima endpoint
    data = request.get_json()
    
    # ambil nilai teks dari data
    text = data['text']

    # modelkan teks dengan model scipy 
    doc = nlp(text)
    
    # membuat pasangan label dan nilai entitas
    d = []

    # transform pasangan label menjadi dataframe 
    if (len(doc.ents) > 0):
        for ent in doc.ents:
            d.append((ent.label_, ent.text))
            df = pd.DataFrame(d, columns=['category', 'value'])
    else:
        df = pd.DataFrame()

    return(df.to_json())


@app.route('/get_entities_normalized',methods=['POST'])
def get_entities_normalized():
    # ambil data dari json yang diterima endpoint
    data = request.get_json()
    
    # ambil nilai teks dari data
    text = data['text']

    # modelkan teks dengan model scipy 
    doc = nlp(text)
    
    # membuat pasangan label dan nilai entitas
    d = []

    # transform pasangan label menjadi dataframe 
    if (len(doc.ents) > 0):
        for ent in doc.ents:
            d.append((ent.label_, ent.text))
            df = pd.DataFrame(d, columns=['category', 'value'])
    else:
        df = pd.DataFrame()

    dn = []

    dn.append(('ORG', df[df['category']=='ORG']['value'].tolist()))
    dfn = pd.DataFrame(dn, columns=['category', 'value'])

    dn.append(('PERSON', df[df['category']=='PERSON']['value'].tolist()))
    dfn = pd.DataFrame(dn, columns=['category', 'value'])

    dn.append(('GPE', df[df['category']=='GPE']['value'].tolist()))
    dfn = pd.DataFrame(dn, columns=['category', 'value'])

    return(dfn.to_json(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)