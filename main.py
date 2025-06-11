# Feito por Bernardo da Silva Neuls, RA: 1138654
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
from recursos.novas_funcoes import falar

print("Inicializando o Jogo! Criado por Bernardo Neuls")
print("Aperte Enter para iniciar o jogo")

pygame.init()
inicializarBancoDeDados()

# Configurações iniciais
tamanho = (1000, 700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho) 
pygame.display.set_caption("Ekko de Zaun")
icone = pygame.image.load("assets/icon.png")
pygame.display.set_icon(icone)

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)

# Carregar assets
ekko = pygame.image.load("assets/ekko.png.png")
fundo_start = pygame.image.load("assets/startbackground.png")
fundo_jogo = pygame.image.load("assets/zaunbackground.png")
fundo_dead = pygame.image.load("assets/deadbackground.png")
hexcore = pygame.image.load("assets/hexcore.png")
hexcore_sound = pygame.mixer.Sound("assets/hextechsoundeffect.wav")
explosao_sound = pygame.mixer.Sound("assets/explosao.wav")

# Fontes
fonte_menu = pygame.font.SysFont("comicsans", 18)
fonte_morte = pygame.font.SysFont("arial", 120)
fonte_pausa = pygame.font.SysFont("Arial", 72)

# Música
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
        
        # Desenhar tela
        tela.blit(fundo_start, (0, 0))
        
        # Mensagem de boas-vindas
        texto_boas_vindas = fonte_menu.render(f"Bem-vindo, {nome}!", True, branco)
        tela.blit(texto_boas_vindas, (400, 200))
        
        # Instruções
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
    # Janela para obter nome do jogador
    def obter_nome():
        global nome
        nome = entry_nome.get()
        if not nome:
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
        else:
            root.destroy()

    root = tk.Tk()
    root.title("Informe seu nickname")
    root.geometry("300x50")
    entry_nome = tk.Entry(root)
    entry_nome.pack()
    botao = tk.Button(root, text="Enviar", command=obter_nome)
    botao.pack()
    root.mainloop()

    if not tela_boas_vindas(nome):
        return
    
    # Variáveis do jogo
    posicaoXPersona = 250
    posicaoYPersona = 500
    movimentoXPersona = 0
    movimentoYPersona = 0
    posicaoXHexcore = 400
    posicaoYHexcore = -240
    velocidadeHexcore = 1
    pontos = 0
    pausado = False  # Variável de controle de pausa
    
    # Configurações do sol
    tamanho_sol = 50
    crescendo = True
    pos_sol_x = 900
    pos_sol_y = 100

    # Iniciar música e efeitos
    pygame.mixer.Sound.play(hexcore_sound)
    pygame.mixer.music.play(-1)

    # Loop principal do jogo
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            
            # Controle de pausa
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pausado = not pausado
                if pausado:
                    pygame.mixer.music.pause()
                    falar("Jogo pausado")
                else:
                    pygame.mixer.music.unpause()
                    falar("Jogo continuado")
                continue
            
            # Controles apenas se o jogo não estiver pausado
            if not pausado:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RIGHT:
                        movimentoXPersona = 15
                        movimentoYPersona = 0
                    elif evento.key == pygame.K_LEFT:
                        movimentoXPersona = -15
                        movimentoYPersona = 0
                elif evento.type == pygame.KEYUP:
                    if evento.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                        movimentoXPersona = 0

        # Se o jogo estiver pausado, exibe a tela de pausa
        if pausado:
            # Desenhar fundo
            tela.blit(fundo_jogo, (0, 0))
            
            # Desenhar elementos do jogo congelados
            tela.blit(ekko, (posicaoXPersona, posicaoYPersona))
            tela.blit(hexcore, (posicaoXHexcore, posicaoYHexcore))
            desenhar_sol(tela, pos_sol_x, pos_sol_y, int(tamanho_sol))
            
            # Exibir texto de pausa
            texto_pausa = fonte_pausa.render("PAUSADO", True, branco)
            tela.blit(texto_pausa, (tamanho[0]//2 - texto_pausa.get_width()//2, 
                                  tamanho[1]//2 - texto_pausa.get_height()//2))
            
            # Exibir pontos
            texto_pontos = fonte_menu.render(f"Pontos: {pontos}", True, branco)
            tela.blit(texto_pontos, (15, 15))
            
            pygame.display.update()
            relogio.tick(60)
            continue
        
        # Lógica do jogo quando não está pausado
        # Movimento do personagem
        posicaoXPersona += movimentoXPersona
        posicaoYPersona += movimentoYPersona
            
        # Limites da tela
        posicaoXPersona = max(0, min(posicaoXPersona, 550))
        posicaoYPersona = max(0, min(posicaoYPersona, 473))
        
        # Movimento do hexcore
        posicaoYHexcore += velocidadeHexcore
        if posicaoYHexcore > 550:
            posicaoYHexcore = -100
            pontos += 1
            velocidadeHexcore += 0.5
            posicaoXHexcore = random.randint(0, 800)
            pygame.mixer.Sound.play(hexcore_sound)

        # Animação do sol
        tamanho_sol += 0.1 if crescendo else -0.1
        if tamanho_sol >= 60:
            crescendo = False
        elif tamanho_sol <= 40:
            crescendo = True
        
        # Desenhar cena do jogo
        tela.blit(fundo_jogo, (0, 0))
        tela.blit(ekko, (posicaoXPersona, posicaoYPersona))
        tela.blit(hexcore, (posicaoXHexcore, posicaoYHexcore))
        desenhar_sol(tela, pos_sol_x, pos_sol_y, int(tamanho_sol))
        
        # UI
        texto_pontos = fonte_menu.render(f"Pontos: {pontos}", True, branco)
        tela.blit(texto_pontos, (15, 15))
        
        texto_instrucao = fonte_menu.render("Pressione ESPAÇO para pausar", True, branco)
        tela.blit(texto_instrucao, (15, 40))
        
        # Verificar colisão
        persona_rect = pygame.Rect(posicaoXPersona, posicaoYPersona, 50, 50)
        hexcore_rect = pygame.Rect(posicaoXHexcore, posicaoYHexcore, 50, 300)
        
        if persona_rect.colliderect(hexcore_rect):
            escreverDados(nome, pontos)
            dead()
        
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
                
                # Botão Sair
                elif 10 <= mouse_pos[0] <= 160 and 60 <= mouse_pos[1] <= 100:
                    pygame.quit()
                    return
        
        # Desenhar tela inicial
        tela.blit(fundo_start, (0, 0))
        
        # Desenhar botões
        pygame.draw.rect(tela, branco, (10, 10, 150, 40), border_radius=15)
        startTexto = fonte_menu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25, 12))
        
        pygame.draw.rect(tela, branco, (10, 60, 150, 40), border_radius=15)
        quitTexto = fonte_menu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25, 62))
        
        pygame.display.update()
        relogio.tick(60)

def dead():
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
                for botao in botoes.values():
                    if botao['rect'].collidepoint(mouse_pos):
                        botao['cor'] = (200, 200, 200)  # Efeito ao pressionar
            
            if evento.type == pygame.MOUSEBUTTONUP:
                for nome_botao, botao in botoes.items():
                    botao['cor'] = branco
                    if botao['rect'].collidepoint(mouse_pos):
                        if nome_botao == 'reiniciar':
                            jogar()
                            return
                        elif nome_botao == 'sair':
                            pygame.quit()
                            return
                        elif nome_botao == 'log':
                            mostrar_log()
        
        tela.blit(fundo_dead, (0, 0))
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
