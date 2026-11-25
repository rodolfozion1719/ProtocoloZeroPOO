# Protocolo Zero - Protótipo
# O que a gente já tem: janela abrindo, jogador que anda com as setas e um robô que persegue o jogador.
# Controles: setas movem o jogador (um quadradinho por aperto), R reinicia.
# O texto do jogo aparece no título da janela (set_caption).

import pygame
from abc import ABC, abstractmethod

largura_tela = 800
altura_tela = 600
celula = 40 # tamanho de cada quadradinho do mapa (tudo anda de 40 em 40)

fundo = (15, 23, 42)
vermelho = (240, 60, 60)
ciano = (0, 200, 220)

class Entidade(ABC):
  def __init__(self, x, y, cor):
    self.x = x
    self.y = y
    self.cor = cor

  @abstractmethod
  def atualizar(self, dt, jogador):
    pass

  @abstractmethod
  def desenhar(self, tela):
    pass

  def mover(self, dx, dy):
    # Calcula a posição nova e só anda se ela ainda estiver dentro da janela.
    novo_x = self.x + dx
    novo_y = self.y + dy
    if novo_x >= 0 and novo_x + celula <= largura_tela and novo_y >= 0 and novo_y + celula <= altura_tela:
      self.x = novo_x
      self.y = novo_y


class Jogador(Entidade):
  def __init__(self, x, y):
    super().__init__(x, y, ciano)

  def atualizar(self, dt, jogador):
    # O jogador só anda quando uma tecla é apertada, então não há nada aqui.
    pass

  def desenhar(self, tela):
    # Quadrado um pouco menor que o quadradinho pra dar para ver o contorno.
    pygame.draw.rect(tela, self.cor, (self.x + 4, self.y + 4, celula - 8, celula - 8))


# Inimigo é a classe base dos inimigos. Ainda é abstrata, porque não escreve atualizar nem desenhar.
# Guarda o que todo inimigo tem: o intervalo entre os passos e o tempo acumulado.
class Inimigo(Entidade):
  def __init__(self, x, y, cor, intervalo):
    super().__init__(x, y, cor)
    self.intervalo = intervalo # de quanto em quanto tempo, em segundos, ele dá um passo
    self.tempo = 0 # tempo acumulado desde o último passo


class InimigoRobo(Inimigo):
  def __init__(self, x, y):
    super().__init__(x, y, vermelho, 0.5) # um passo a cada meio segundo

  def atualizar(self, dt, jogador):
    self.tempo += dt
    if self.tempo >= self.intervalo:
      self.tempo = 0
      # Anda um passo na direção do jogador: primeiro na horizontal, depois na vertical.
      if jogador.x > self.x:
        self.mover(celula, 0)
      elif jogador.x < self.x:
        self.mover(-celula, 0)
      elif jogador.y > self.y:
        self.mover(0, celula)
      elif jogador.y < self.y:
        self.mover(0, -celula)

  def desenhar(self, tela):
    # O robô é desenhado como círculo, para ficar diferente do jogador, que é  o quadrado.
    centro = (self.x + celula // 2, self.y + celula // 2)
    pygame.draw.circle(tela, self.cor, centro, celula // 2 - 4)


class Jogo:
  def __init__(self):
    pygame.init()
    self.tela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption("Protocolo Zero")
    self.relogio = pygame.time.Clock()
    self.rodando = True
    self.reiniciar()

  def reiniciar(self):
    # Cria jogador e robô novos. Serve para começar e também para reiniciar.
    self.jogador = Jogador(40, 40)
    self.robo = InimigoRobo(680, 480)
    self.pego = False # vira True quando o robô alcança o jogador

  def run(self):
    while self.rodando:
      dt = self.relogio.tick(60)/1000 # 60 frames por segundo (FPS)
      self.processar_evento()
      self.atualizar(dt)
      self.desenhar()
    pygame.quit()

  def processar_evento(self):
    for evento in pygame.event.get():
      if evento.type == pygame.QUIT:
        self.rodando = False
      elif evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_r:
          self.reiniciar()
        elif not self.pego: # depois de ser pego, as setas param de funcionar
          if evento.key == pygame.K_UP:
            self.jogador.mover(0, -celula)
          elif evento.key == pygame.K_DOWN:
            self.jogador.mover(0, celula)
          elif evento.key == pygame.K_LEFT:
            self.jogador.mover(-celula, 0)
          elif evento.key == pygame.K_RIGHT:
            self.jogador.mover(celula, 0)

  def atualizar(self, dt):
    if not self.pego:
      self.jogador.atualizar(dt, self.jogador)
      self.robo.atualizar(dt, self.jogador)
      # Como tudo anda de quadradinho em quadradinho, estar no mesmo lugar é a colisão.
      if self.jogador.x == self.robo.x and self.jogador.y == self.robo.y:
        self.pego = True

  def desenhar(self):
    self.tela.fill(fundo)
    self.robo.desenhar(self.tela)
    self.jogador.desenhar(self.tela) # por último, para ficar na frente
    if self.pego:
      pygame.display.set_caption("Protocolo Zero | O robô te pegou! Aperte R para reiniciar.")
    else:
      pygame.display.set_caption("Protocolo Zero | Setas movem. Fuja do robô.")
    pygame.display.flip()


if __name__ == "__main__":
  Jogo().run()