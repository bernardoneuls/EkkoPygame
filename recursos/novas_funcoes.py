import pygame
import datetime
import random
import speech_recognition as sr
import pyttsx3

def obter_data_hora():
    agora = datetime.datetime.now()
    return {
        'data': agora.strftime("%d/%m/%Y"),
        'hora': agora.strftime("%H:%M:%S")
    }

def desenhar_sol(tela, pos_x, pos_y, tamanho):
    pygame.draw.circle(tela, (255, 255, 0), (pos_x, pos_y), tamanho)

def ler_log():
    try:
        with open("log.dat", "r") as arquivo:
            return arquivo.readlines()
    except FileNotFoundError:
        return []

def salvar_log(nome, pontos):
    data_hora = obter_data_hora()
    with open("log.dat", "a") as arquivo:
        arquivo.write(f"{nome};{pontos};{data_hora['data']};{data_hora['hora']}\n")

def reconhecer_voz():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Diga algo...")
        audio = r.listen(source)
    
    try:
        texto = r.recognize_google(audio, language='pt-BR')
        return texto
    except Exception as e:
        print(e)
        return None

def falar(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()