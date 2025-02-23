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

normal_text, site, video = st.tabs(["Normal text", "Site", "Video"])

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
        text = translate(text)
    
        main_key = check_dict(text)

        emotion = ton_check(text, main_key, check)

        st.subheader(f"Рубрика: {main_key}")

        if emotion > 0:
            st.title(f"Тональність: +{emotion}% (позитивна)")
        elif emotion == 0:
            st.title(f"Тональність: {emotion}% (нейтральна)")
        else:
            st.title(f"Тональність: {emotion}% (негативна)")

        st.text("Текст:")

        st.text(text)


with site:
    url = st.text_input('Enter url')
    
    check1 = st.checkbox('Inversion')

    but = st.button('Apply')

    if but:
        text = fetch_news(url)

        text = translate(text)
    
        main_key = check_dict(text)

        emotion = ton_check(text, main_key, check1)

        st.subheader(f"Рубрика: {main_key}")

        if emotion > 0:
            st.title(f"Тональність: +{emotion}% (позитивна)")
        elif emotion == 0:
            st.title(f"Тональність: {emotion}% (нейтральна)")
        else:
            st.title(f"Тональність: {emotion}% (негативна)")

        st.text("Текст статті:")

        st.text(text)

with video:
    url = st.text_input('Enter video url')

    check2 = st.checkbox('Video inversion')
    
    but = st.button('Video apply')

    if but:
        parsed_url = urlparse(url)

        video_id = parse_qs(parsed_url.query).get("v", [None])[0]

        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        for transcript in transcript_list:
            try:
                subtitles = transcript.fetch()
                full_text = "\n".join([t["text"] for t in subtitles])
                break
            except Exception as e:
                st.text(f"Не вдалося отримати субтитри: {e}")

        full_text = translate(full_text)
        
        main_key = check_dict(full_text)

        emotion = ton_check(full_text, main_key, check2)

        st.subheader(f"Рубрика: {main_key}")

        if emotion > 0:
            st.title(f"Тональність: +{emotion}% (позитивна)")
        elif emotion == 0:
            st.title(f"Тональність: {emotion}% (нейтральна)")
        else:
            st.title(f"Тональність: {emotion}% (негативна)")

        st.text("Текст відео:")

        st.text(full_text)
