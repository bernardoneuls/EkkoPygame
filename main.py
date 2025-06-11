#Feito por Bernardo da Silva Neuls, RA: 1138654
#Foi usado as hashtags apenas em novas funções não implementadas no código original
import time
import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
import json
from recursos.funcoes import inicializarBancoDeDados
from recursos.funcoes import escreverDados
from recursos.novas_funcoes import desenhar_sol
from recursos.novas_funcoes import salvar_log
from recursos.novas_funcoes import reconhecer_voz
from recursos.novas_funcoes import falar
print("Inicializando o Jogo! Criado por Bernardo Neuls")
print("Aperte Enter para iniciar o jogo")
pygame.init()
inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("Ekko de Zaun")
icone  = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0 )
ekko = pygame.image.load("assets/ekko.png.png")
fundo_start = pygame.image.load("assets/startbackground.png")
fundo_jogo= pygame.image.load("assets/zaunbackground.png")
fundo_dead = pygame.image.load("assets/deadbackground.png")
hexcore = pygame.image.load("assets/hexcore.png")
hexcore_sound = pygame.mixer.Sound("assets/hextechsoundeffect.wav")
explosao_sound = pygame.mixer.Sound("assets/explosao.wav")
fonte_menu = pygame.font.SysFont("comicsans",18)
fonte_morte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("assets/ekkosoundtrack.mp3.mp3")

def tela_boas_vindas(nome):
    falar(f"Bem-vindo {nome}! Use as setas para mover o Ekko e desvie dos hexcores. Boa sorte!")
    
    larguraButtonStart = 150
    alturaButtonStart = 40
    startButton = pygame.Rect(425, 450, larguraButtonStart, alturaButtonStart)
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return False
            
            if evento.type == pygame.MOUSEBUTTONDOWN and startButton.collidepoint(mouse_pos):
                larguraButtonStart = 140
                alturaButtonStart = 35
            
            if evento.type == pygame.MOUSEBUTTONUP and startButton.collidepoint(mouse_pos):
                return True
        
        #Desenhar tela
        tela.blit(fundo_start, (0, 0))
        
        #Mensagem de boas-vindas
        texto_boas_vindas = fonte_menu.render(f"Bem-vindo, {nome}!", True, branco)
        tela.blit(texto_boas_vindas, (400, 200))
        
        #Instruções
        instrucoes = [
            "Como Jogar:",
            "- Use as setas para mover Ekko",
            "- Desvie dos Hexcores que caem",
            "- Cada Hexcore desviado = 1 ponto",
            "- O jogo acelera com o tempo",
            "- Pressione ESPAÇO para pausar"
        ]
        
        for i, linha in enumerate(instrucoes):
            texto = fonte_menu.render(linha, True, branco)
            tela.blit(texto, (400, 250 + i * 30))
        
        # Botão
        startButton = pygame.draw.rect(tela, branco, (425, 450, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonte_menu.render("Iniciar Jogo", True, preto)
        tela.blit(startTexto, (450, 460))
        
        pygame.display.update()
        relogio.tick(60)

def jogar():
    largura_janela = 300
    altura_janela = 50
    def obter_nome():
        global nome
        nome = entry_nome.get()
        if not nome:
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
        else:
            root.destroy()

    root = tk.Tk()
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    pos_x = (largura_tela - largura_janela) // 2
    pos_y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    root.title("Informe seu nickname")
    root.protocol("WM_DELETE_WINDOW", obter_nome)

    entry_nome = tk.Entry(root)
    entry_nome.pack()

    botao = tk.Button(root, text="Enviar", command=obter_nome)
    botao.pack()

    root.mainloop()

    if not tela_boas_vindas(nome):
        return
    posicaoXPersona = 250
    posicaoYPersona = 500
    movimentoXPersona  = 0
    movimentoYPersona  = 0
    posicaoXHexcore = 400
    posicaoYHexcore = -240
    velocidadeHexcore = 1
    pygame.mixer.Sound.play(hexcore_sound)
    pygame.mixer.music.play(-1)
    pontos = 0
    larguraPersona = 50
    alturaPersona = 50
    larguaHexcore  = 50
    alturaHexcore  = 300
    dificuldade  = 30

#Configurações do sol
    tamanho_sol = 50
    crescendo = True
    pos_sol_x = 900
    pos_sol_y = 100


    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado
                    falar("Jogo pausado" if pausado else "Jogo continuado")
                #Movimento em um eixo por vez
                elif evento.key == pygame.K_RIGHT and movimentoYPersona == 0:
                    movimentoXPersona = 15
                    movimentoYPersona = 0
                elif evento.key == pygame.K_LEFT and movimentoYPersona == 0:
                    movimentoXPersona = -15
                    movimentoYPersona = 0
            elif evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    movimentoXPersona = 0
                elif evento.key in [pygame.K_UP, pygame.K_DOWN]:
                    movimentoYPersona = 0
                pygame.display.update()
                relogio.tick(60)
                continue
                
        posicaoXPersona = posicaoXPersona + movimentoXPersona            
        posicaoYPersona = posicaoYPersona + movimentoYPersona            
        
        if posicaoXPersona < 0 :
            posicaoXPersona = 15
        elif posicaoXPersona >550:
            posicaoXPersona = 540
            
        if posicaoYPersona < 0 :
            posicaoYPersona = 15
        elif posicaoYPersona > 473:
            posicaoYPersona = 463
        
            
        tela.fill(branco)
        tela.blit(fundo_jogo, (0,0) )
        
        tela.blit( ekko, (posicaoXPersona, posicaoYPersona) )
        
        posicaoYHexcore = posicaoYHexcore + velocidadeHexcore
        if posicaoYHexcore > 550:
            posicaoYHexcore = -100
            pontos = pontos + 1
            velocidadeHexcore = velocidadeHexcore + 1
            posicaoXHexcore = random.randint(0,800)
            pygame.mixer.Sound.play(hexcore_sound)

        #Animação do sol
        tamanho_sol += 0.1 if crescendo else -0.1
        if tamanho_sol >= 60:
            crescendo = False
        elif tamanho_sol <= 40:
            crescendo = True
            
        tela.blit( hexcore, (posicaoXHexcore, posicaoYHexcore) )
        
        texto = fonte_menu.render("Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (15,15))
        
        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+alturaPersona))
        pixelsHexcoreX = list(range(posicaoXHexcore, posicaoXHexcore + larguaHexcore))
        pixelsHexcoreY = list(range(posicaoYHexcore, posicaoYHexcore + alturaHexcore))
        #UI
        texto_pontos = fonte_menu.render(f"Pontos: {pontos}", True, branco)
        tela.blit(texto_pontos, (15, 15))
        
        texto_pausa = fonte_menu.render("Pressione ESPAÇO para pausar", True, branco)
        tela.blit(texto_pausa, (15, 40))
        
        desenhar_sol(tela, pos_sol_x, pos_sol_y, int(tamanho_sol))
        #Colisão
        persona_rect = pygame.Rect(posicaoXPersona, posicaoYPersona, 250, 127)
        hexcore_rect = pygame.Rect(posicaoXHexcore, posicaoYHexcore, 50, 250)
        
        if persona_rect.colliderect(hexcore_rect):
            dead()
        
        os.system("cls")
        if  len( list( set(pixelsHexcoreY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixelsHexcoreX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                escreverDados(nome, pontos)
                dead()
                
            else:
                print("Ainda Vivo, mas por pouco!")
        else:
            print("Ainda Vivo")
        
        pygame.display.update()
        relogio.tick(60)


def start():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Botão Iniciar
                if 10 <= mouse_pos[0] <= 160 and 10 <= mouse_pos[1] <= 50:
                    jogar()
                
                #Botão Sair
                elif 10 <= mouse_pos[0] <= 160 and 60 <= mouse_pos[1] <= 100:
                    pygame.quit()
                    return
        
        #Desenhar tela inicial
        tela.blit(fundo_start, (0,0))
        
        #Desenhar botão Iniciar
        pygame.draw.rect(tela, branco, (10, 10, 150, 40), border_radius=15)
        startTexto = fonte_menu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        #Desenhar botão Sair
        pygame.draw.rect(tela, branco, (10, 60, 150, 40), border_radius=15)
        quitTexto = fonte_menu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))
        
        pygame.display.update()
        relogio.tick(60)


def dead():
     #Captura reação por voz
    falar("Anomalia te infectou, Ekko. Adeus.")
    time.sleep(1)
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosao_sound)
    
    # Configurações dos botões
    botoes = {
        'reiniciar': {'rect': pygame.Rect(350, 400, 300, 50), 'texto': "Jogar Novamente", 'cor': branco},
        'sair': {'rect': pygame.Rect(350, 470, 300, 50), 'texto': "Sair do Jogo", 'cor': branco},
        'log': {'rect': pygame.Rect(350, 540, 300, 50), 'texto': "Ver Pontuações", 'cor': branco}
    }
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for nome_botao, botao in botoes.items():
                    if botao['rect'].collidepoint(mouse_pos):
                        botao['cor'] = (200, 200, 200)  # Cinza claro quando pressionado
            
            if evento.type == pygame.MOUSEBUTTONUP:
                for nome_botao, botao in botoes.items():
                    botao['cor'] = branco  # Volta ao branco
                    if botao['rect'].collidepoint(mouse_pos):
                        if nome_botao == 'reiniciar':
                            jogar()
                            return
                        elif nome_botao == 'sair':
                            pygame.quit()
                            return
                        elif nome_botao == 'log':
                            mostrar_log()
        
        # Desenhar tela de morte
        tela.blit(fundo_dead, (0, 0))
        
        # Texto "Você Morreu"
        texto_morte = fonte_morte.render("Você Morreu!", True, (255, 0, 0))
        tela.blit(texto_morte, (250, 200))
        
        # Desenhar botões
        for botao in botoes.values():
            pygame.draw.rect(tela, botao['cor'], botao['rect'], border_radius=10)
            texto = fonte_menu.render(botao['texto'], True, preto)
            tela.blit(texto, (botao['rect'].x + 50, botao['rect'].y + 15))
        
        pygame.display.update()
        relogio.tick(60)

def mostrar_log():
    root = tk.Tk()
    root.title("Histórico de Partidas")
    root.geometry("600x400")
    
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)
    
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, width=80, font=('Arial', 12))
    listbox.pack(fill=tk.BOTH, expand=True)
    
    scrollbar.config(command=listbox.yview)
    
    try:
        with open("base.atitus", "r") as f:
            log_partidas = json.load(f)
            for nome_jogador, dados in log_partidas.items():
                listbox.insert(tk.END, f"{nome_jogador}: {dados[0]} pontos em {dados[1]}")
    except Exception as e:
        listbox.insert(tk.END, "Nenhum registro encontrado" if "No such file" in str(e) else f"Erro: {str(e)}")
    
    tk.Button(root, text="Fechar", command=root.destroy).pack(pady=10)
    root.mainloop()

start()
