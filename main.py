pip install bs4
import streamlit as st
import requests
from bs4 import BeautifulSoup
from googletrans import Translator, LANGUAGES
import re
import string
import ast

url = st.text_input('Enter url')

dict = st.sidebar.selectbox('Select', ['Військово-політичне керівництво України всіх рівнів','Правоохоронні органи України','Збройні сили України',
                                       'Соціально-політична ситуація в регіонах України (відношення до мобілізації, соціально-економічна стабільність тощо)','Проросійські релігійні організації на території України',
                                       'Проросійські рухи, формування концепції «руського миру»','Міжнародний імідж України в ЄС (англійська, німецька, польська, румунська, французька, угорська, українська, російська мови)',
                                       'Міжнародний імідж України в США, Канаді та Великобританії (англійська мова)','Міжнародний імідж України в країнах Африки (англійська, французька арабська мови)',
                                       'Міжнародний імідж України в країнах Азії (російська, китайська, турецька, арабська, грузинська, казахська, фарсі, киргизька, таджицька, узбецька, японська, корейська мови)',
                                       'Україна в інформаційному просторі російської федерації','Україна в інформаційному просторі республіки білорусь',
                                       'Соціально-економічна, політична, військова ситуація в російській федерації (відношення до вищого керівництва, мобілізації, погіршення економічного становища тощо)'])

type = st.sidebar.selectbox('Select', ['Keywords', 'Dictionary'])

if type == 'Dictionary':
    type2 = st.sidebar.selectbox('Select', ['Positive', 'Negative'])

word = st.sidebar.text_input('Enter word')

apply = st.sidebar.button('Add')

rem = st.sidebar.button('Remove')

all = st.sidebar.button('Show all')

def dictionaries(string):
    dict = {'Військово-політичне керівництво України всіх рівнів':0,'Правоохоронні органи України':1,'Збройні сили України':2,
                                       'Соціально-політична ситуація в регіонах України (відношення до мобілізації, соціально-економічна стабільність тощо)':3,'Проросійські релігійні організації на території України':4,
                                       'Проросійські рухи, формування концепції «руського миру»':5,'Міжнародний імідж України в ЄС (англійська, німецька, польська, румунська, французька, угорська, українська, російська мови)':6,
                                       'Міжнародний імідж України в США, Канаді та Великобританії (англійська мова)':7,'Міжнародний імідж України в країнах Африки (англійська, французька арабська мови)':8,
                                       'Міжнародний імідж України в країнах Азії (російська, китайська, турецька, арабська, грузинська, казахська, фарсі, киргизька, таджицька, узбецька, японська, корейська мови)':9,
                                       'Україна в інформаційному просторі російської федерації':10,'Україна в інформаційному просторі республіки білорусь':11,
                                       'Соціально-економічна, політична, військова ситуація в російській федерації (відношення до вищого керівництва, мобілізації, погіршення економічного становища тощо)':12}
    key = dict.get(string) + 1
    return key


def fetch_news(url):
    response = requests.get(url)

    # Перевірте статус відповіді; 200 означає, що все гаразд
    if response.status_code != 200:
        print(f'Failed to retrieve the page with status code: {response.status_code}')
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Збір новин
    text = []
    final_text = ""
    for article in soup.find_all('p'):
        headline_text = article.text.strip()
        if headline_text:  # Перевірка на наявність тексту
            text.append(headline_text)
    for i in range(len(text)):
        final_text = final_text + text[i] + '\n'
    
    return final_text
    
def show_keys(key):
    string = 'keywords/keywords_' + str(key) + '.txt'

    with open(string) as f: 
        data = f.read()

    return data

def show_dict_positive(key):
    string = 'dictionaries/positive/dict_' + str(key) + '.txt'

    with open(string) as f: 
        data = f.read()

    return data

def show_dict_negative(key):
    string = 'dictionaries/negative/dict_' + str(key) + '.txt'

    with open(string) as f: 
        data = f.read()

    return data

def save_dict(key, text, type):
    if type == "Positive":
        string = 'dictionaries/positive/dict_' + str(key) + '.txt'
    else:
        string = 'dictionaries/negative/dict_' + str(key) + '.txt'

    with open(string,'w') as data:  
      data.write(str(text))

def update_dict(key, string, type):
    if type == "Positive":
        data = show_dict_positive(key)
    else:
        data = show_dict_negative(key)
    
    data = ast.literal_eval(data)

    data.append(string)

    save_dict(key, data, type)

    st.sidebar.write(data)

def remove_dict(key, string, type):
    if type == "Positive":
        data = show_dict_positive(key)
    else:
        data = show_dict_negative(key)
    
    data = ast.literal_eval(data)

    data.remove(string)

    save_dict(key, data, type)

    st.sidebar.write(data)

def update_key(key, string):
    data = show_keys(key)

    data = ast.literal_eval(data)

    data.append(string)

    save_keys(key, data)

    st.sidebar.write(data)

def remove_key(key, string):
    data = show_keys(key)

    data = ast.literal_eval(data)

    data.remove(string)

    save_keys(key, data)

    st.sidebar.write(data)

def save_keys(key, text):
    string = 'keywords/keywords_' + str(key) + '.txt'

    with open(string,'w') as data:  
      data.write(str(text))

def check_dict(text):
    dict = ['Військово-політичне керівництво України всіх рівнів','Правоохоронні органи України','Збройні сили України',
                                       'Соціально-політична ситуація в регіонах України (відношення до мобілізації, соціально-економічна стабільність тощо)','Проросійські релігійні організації на території України',
                                       'Проросійські рухи, формування концепції «руського миру»','Міжнародний імідж України в ЄС (англійська, німецька, польська, румунська, французька, угорська, українська, російська мови)',
                                       'Міжнародний імідж України в США, Канаді та Великобританії (англійська мова)','Міжнародний імідж України в країнах Африки (англійська, французька арабська мови)',
                                       'Міжнародний імідж України в країнах Азії (російська, китайська, турецька, арабська, грузинська, казахська, фарсі, киргизька, таджицька, узбецька, японська, корейська мови)',
                                       'Україна в інформаційному просторі російської федерації','Україна в інформаційному просторі республіки білорусь',
                                       'Соціально-економічна, політична, військова ситуація в російській федерації (відношення до вищого керівництва, мобілізації, погіршення економічного становища тощо)']
    result = []
    for i in range(13):
        keys = show_keys(i + 1)
        keys = ast.literal_eval(keys)
        text = str.lower(text)

        for i in range(len(keys)):
            keys[i] = str.lower(keys[i])
        
        nums = 0

        for i in range(len(keys)):
            if keys[i] in text:
                nums += 1
        
        result.append(nums)
    
    max_ind = result.index(max(result))
    return dict[max_ind]

def ton_check(text, main_key):
    text = str.lower(text)

    key = dictionaries(main_key)
    
    positive = show_dict_positive(key)
    negative = show_dict_negative(key)
    
    positive = ast.literal_eval(positive)
    negative = ast.literal_eval(negative)
    
    for i in range(len(positive)):
        positive[i] = str.lower(positive[i])

    for i in range(len(negative)):
        negative[i] = str.lower(negative[i])
    
    pos_nums = 0

    neg_nums = 0

    for i in range(len(positive)):
        if positive[i] in text:
            pos_nums += 1

    for i in range(len(negative)):
        if negative[i] in text:
            neg_nums += 1

    result = (pos_nums - neg_nums) * 10
    
    if result > 100:
        result = 100
    elif result < -100:
        result = -100
    
    if check:
        result *= -1

    return result

def translate(text):
    translator = Translator()

    detected = translator.detect(text)
    
    if detected.lang != 'uk':
        translated_text = translator.translate(text, dest='uk')
        return translated_text.text
    else: 
        return text 
    

check = st.checkbox('Inversion')

but = st.button('Apply')

if all:
    key = dictionaries(dict)

    if type == 'Keywords':
        text = show_keys(key)
        st.sidebar.write(text)

    else:
        if type2 == 'Positive':
            text = show_dict_positive(key)

        else:
            text = show_dict_negative(key)

        st.sidebar.write(text)
    
if apply:
    key = dictionaries(dict)

    if type == 'Keywords':
        update_key(key, word)
    else:
        if type2 == 'Positive':
            update_dict(key, word, type2)
        else:
            update_dict(key, word, type2)

if rem: 
    key = dictionaries(dict)

    if type == 'Keywords':
        remove_key(key, word)
    else:
        if type2 == 'Positive':
            remove_dict(key, word, type2)
        else:
            remove_dict(key, word, type2)

if but:
    text = fetch_news(url)

    text = translate(text)
    
    main_key = check_dict(text)

    emotion = ton_check(text, main_key)

    st.subheader(f"Рубрика: {main_key}")

    if emotion > 0:
        st.title(f"Тональність: +{emotion}% (позитивна)")
    elif emotion == 0:
        st.title(f"Тональність: {emotion}% (нейтральна)")
    else:
        st.title(f"Тональність: {emotion}% (негативна)")

    st.text("Текст статті:")

    st.text(text)
