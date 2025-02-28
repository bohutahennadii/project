import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

from analysis import (
    dictionaries,
    show_keys,
    show_dict_positive,
    show_dict_negative,
    update_key,
    update_dict,
    remove_key,
    remove_dict,
    translate,
    check_dict,
    ton_check,
    fetch_news
)

normal_text, site = st.tabs(["Normal text", "Site"])

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

with normal_text:
    text = st.text_input('Enter text')

    check = st.checkbox('Inversion normal')

    but = st.button('Apply normal')

    if but:
        text1, lang = translate(text)
    
        main_key = check_dict(text)

        emotion = ton_check(text, main_key, check)

        st.subheader(f"Рубрика: {main_key}")

        if emotion > 0:
            st.title(f"Тональність: +{emotion}% (позитивна)")
        elif emotion == 0:
            st.title(f"Тональність: {emotion}% (нейтральна)")
        else:
            st.title(f"Тональність: {emotion}% (негативна)")

        if lang:
            st.text("Текст статті:")
            
            st.text(text1)
        else:
            st.text("Оригінальний текст статті:")

            st.text(text)
            
            st.text("Перекладений текст:")

            st.text(text1)


with site:
    url = st.text_input('Enter url')
    
    check1 = st.checkbox('Inversion')

    but = st.button('Apply')

    if but:
        text = fetch_news(url)

        text1, lang = translate(text)
    
        main_key = check_dict(text1)

        emotion = ton_check(text1, main_key, check1)

        st.subheader(f"Рубрика: {main_key}")

        if emotion > 0:
            st.title(f"Тональність: +{emotion}% (позитивна)")
        elif emotion == 0:
            st.title(f"Тональність: {emotion}% (нейтральна)")
        else:
            st.title(f"Тональність: {emotion}% (негативна)")

        if lang:
            st.text("Текст статті:")
            
            st.text(text1)
        else:
            st.text("Оригінальний текст статті:")

            st.text(text)
            
            st.text("Перекладений текст:")

            st.text(text1)
