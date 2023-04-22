import streamlit as st
import speech_recognition as sr
import pyttsx3
import openai
import playsound

# Insira sua chave de API aqui
openai.api_key = st.secrets['api_key_openai']

contexto = 'Crie uma história infantil.'
temperature = 0.7
limiteModelo = 4096

# Define a função para obter a resposta do ChatGPT
def get_chat_response(prompt):
    print('chamando chatGPT')
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=limiteModelo - len(prompt),
        top_p=1,
        frequency_penalty=0.2,
        presence_penalty=0,
        temperature=temperature,
    )
    message = response.choices[0].text.strip()
    return message

# Define a função para tocar o som
def play_sound(filename):
    playsound.playsound(filename)

with st.sidebar:
    st.header('Orientação de uso')
    st.write('1 - Ao ouvir o beep, fale uma ideia para a criação da história infantil.')
    st.write('2 - Aguarde a fala da história criada pelo chatGPT')
   
    st.header('Sobre')
    st.write('Detalhe sobre este projeto pode ser encontrado em: ')


# título
Title = f'Criador de História Infantil (ChatGPT)'
st.title(Title)            

# ativa o microfone
mic = sr.Recognizer()

with sr.Microphone() as source:
    engine = pyttsx3.init()
    engine.setProperty('voice', 'com.apple.speech.synthesis.voice.luciana')
    #Chama um algoritmo de reducao de ruidos no som
    mic.adjust_for_ambient_noise(source)

    print("Fale alguma coisa.")
    # Toca o som de indicação para o usuário começar a falar
    play_sound('beep-07a.wav')

    audio = mic.listen(source)

    try:
        frase = mic.recognize_google(audio, language='pt-BR')
        print('você falou: ' + frase)    
        # fala o que escutou
        engine.say(frase)
        engine.runAndWait()
        # libera os recursos do microfone
        # mic.stop()   ??? precisa
        
        response = get_chat_response(contexto + ' ' + frase)
        print(response) 
        st.write(response)
        engine.say(response)
        engine.runAndWait()
                
    except sr.UnknownValueError:
        print('algo deu errado')
        engine.say("Desculpe, eu não entendi")
        engine.runAndWait()

# mic.stop()        
# engine.stop()