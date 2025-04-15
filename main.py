import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

from analysis import (
    dictionaries,
    get_articles,
    show_keys,
    show_articles,
    show_dict_positive,
    show_dict_negative,
    update_key,
    update_articles,
    update_dict,
    remove_key,
    remove_articles,
    remove_dict,
    translate,
    check_dict,
    check_articles,
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

type = st.sidebar.selectbox('Select', ['Keywords', 'Dictionary', 'Article'])

if type == 'Dictionary':
    type2 = st.sidebar.selectbox('Select', ['Positive', 'Negative'])

if type == 'Article':
    articles = st.sidebar.selectbox('Select', ['Конституція України, частина четверта статті 32', 'Цивільний кодекс України, стаття 278', 'Закон України "Про телебачення і радіомовлення", стаття 7', 
                                               'Закон України "Про друковані засоби масової інформації (пресу) в Україні", статті 3, 18', 'Кодекс України про адміністративні правопорушення, стаття 173-1',
                                               'Кримінальний кодекс України, стаття 109', 'Кримінальний кодекс України, стаття 259', 'Кримінальний кодекс України, стаття 182',
                                               'Кримінальний кодекс України, стаття 168', 'Кримінальний кодекс України Стаття 232. Розголошення комерційної або банківської таємниці',
                                               'Кримінальний кодекс України Стаття 161. Порушення рівноправності громадян залежно від їх расової, національної належності, релігійних переконань, інвалідності та за іншими ознаками',
                                               'Закон України «Про медіа» Стаття 36. Обмеження щодо змісту інформації'])

word = st.sidebar.text_input('Enter word')

apply = st.sidebar.button('Add')

rem = st.sidebar.button('Remove')

all = st.sidebar.button('Show all')

if all:
    if type == 'Keywords':
        key = dictionaries(dict)
        text = show_keys(key)
        st.sidebar.write(text)
    
    if type == 'Dictionary':
        key = dictionaries(dict)
        if type2 == 'Positive':
            text = show_dict_positive(key)

        else:
            text = show_dict_negative(key)

        st.sidebar.write(text)

    if type == 'Article':
        key = get_articles(articles)
        text = show_articles(key)
        st.sidebar.write(text)
    
if apply:
    if type == 'Keywords':
        key = dictionaries(dict)
        update_key(key, word)
    
    if type == 'Dictionary':
        key = dictionaries(dict)
        if type2 == 'Positive':
            update_dict(key, word, type2)
        else:
            update_dict(key, word, type2)

    if type == 'Article':
        key = get_articles(articles)
        update_articles(key, word)

if rem: 
    if type == 'Keywords':
        key = dictionaries(dict)
        remove_key(key, word)
    
    if type == 'Dictionary':
        key = dictionaries(dict)
        if type2 == 'Positive':
            remove_dict(key, word, type2)
        else:
            remove_dict(key, word, type2)

    if type == 'Article':
        key = get_articles(articles)
        remove_articles(key, word)

with normal_text:
    text = st.text_input('Enter text')

    check = st.checkbox('Inversion normal')

    but = st.button('Apply normal')

    if but:
        text1, lang = translate(text)
    
        main_key = check_dict(text1)

        emotion = ton_check(text1, main_key, check)

        article = check_articles(text1)
        
        st.markdown(
            f"""
            <style>
            .floating-article {{
                position: fixed;
                top: 350px; /* Висота, де ти хочеш показати */
                right: 120px; /* Відступ від правого краю */
                padding: 6px 12px;
                border-radius: 8px;
                z-index: 9999;
                width: 250px;
            }}
            </style>

            <div class="floating-article">
                Назва статті закону чи кодексу: {article}
            </div>
            """,
            unsafe_allow_html=True
        )
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

        article = check_articles(text1)

        st.subheader(f"Рубрика: {main_key}")

        if emotion > 0:
            st.title(f"Тональність: +{emotion}% (позитивна)")
        elif emotion == 0:
            st.title(f"Тональність: {emotion}% (нейтральна)")
        else:
            st.title(f"Тональність: {emotion}% (негативна)")

        st.subheader(f"Назва статті закону чи кодексу: {article}")

        if lang:
            st.text("Текст статті:")
            
            st.text(text1)
        else:
            st.text("Оригінальний текст статті:")

            st.text(text)
            
            st.text("Перекладений текст:")

            st.text(text1)
