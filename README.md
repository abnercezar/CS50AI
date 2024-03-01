# CS50AI - 2023
### Introdução do CS50 à Inteligência Artificial com Python
![Harvard](https://github.com/abnercezar/CS50x/assets/102832541/96a8e6ab-d1a2-40b0-8b16-21db0b3dbd7e)

### Site CS50AI: 
https://cs50.harvard.edu/ai/2023/
____
## Sobre este curso
Este curso explora os conceitos e algoritmos que estão na base da inteligência artificial moderna, mergulhando nas ideias que dão origem a tecnologias como motores de jogos, reconhecimento de escrita e tradução automática. Por meio de projetos práticos, os alunos ganham exposição à teoria por trás de algoritmos de busca de gráficos, classificação, otimização, aprendizado de máquina, grandes modelos de linguagem e outros tópicos de inteligência artificial à medida que os incorporam em seus próprios programas Python. Ao final do curso, os alunos adquirem experiência em bibliotecas para aprendizado de máquina, bem como conhecimento dos princípios de inteligência artificial que lhes permitem projetar seus próprios sistemas inteligentes.
____
## Aprendizados
- Algoritmos de pesquisa gráfica
- Busca adversária
- Representação do conhecimento
- Inferência lógica
- Teoria da probabilidade
- Redes Bayesianas
- Modelos de Markov
- Satisfação de restrição
- Aprendizado de máquina
- Aprendizagem por reforço
- Redes neurais
- Processamento de linguagem natural
____


# Semana 0: Pesquisa
### Graus:
### Escreva um programa que determine quantos “graus de separação” dois atores estão separados.
![image](https://github.com/abnercezar/CS50AI/assets/102832541/6a7bc5b5-f974-459f-b928-59de97a78e79)

- Você deve encontrar o caminho mais curto entre dois nós.
- Você irá usar o banco de dados do IMDb, e você deverá encontrar como dois atores se conectam no elenco do mesmo filme.
- A solução é baseada na Pesquisa em Largura (BFS) porque a tarefa requer o caminho mais curto entre os nós
- Para implementar a pesquisa a fronteira usada é uma fila, e criei um algoritimo de busca em largura que é empregado para encontrar o caminho mais curto no grafo.


____
### Tic-Tac-Toe:
![image](https://github.com/abnercezar/CS50AI/assets/102832541/1e5591b6-37ed-48ec-b946-c0e7584014c9)
Para você obter este tabuleiro deverá instalar o Pygame: 
Documentação: [Pygame News](https://www.pygame.org/news)

- Usando a função Minimax, que é uma das mais importantes, a IA deve jogar Tic-Tac-Toe de maneira ideal.
- O tabuleiro é fornecido para você (runner.py), porém é necessário implementar uma função Minimax na sua(tictactoe.py) entre outras não menos importantes. Sua IA deve fazer uma cópia do tabuleiro e calcular todas as possíveis jogadas do seu oponente. Ela deve até permitir que você empate, mas não pode permitir que você a vença.
  #### Bug:
  Não há consistência nos padrões de movimento da sua IA. Certifique-se de revisar as expectativas da especificação.
  valid_actions, best_move nem sempre são selecionados/implementados corretamente.
  
  #### Lembre-se a depuração é essencial nesta atividade!

  ____
# Semana 1: Conhecimento
  ### Knights:
 - Escreva um programa para resolver quebra-cabeças lógicos.
 - Não há necessidade de entender tudo neste arquivo, mas observe que ele define diversas classes para diferentes tipos de conectivos lógicos. Essas classes podem ser compostas umas dentro das outras, portanto, uma expressão como And(Not(A), Or(B, C))representa a sentença lógica afirmando que o símbolo Anão é verdadeiro e que o símbolo Bou símbolo Cé verdadeiro (onde “ou” aqui se refere a inclusivo, não exclusivo ou).
- A seguir estão quatro bases de conhecimento diferentes, knowledge0, knowledge1, knowledge2e knowledge3, que conterão o conhecimento necessário para deduzir as soluções para os próximos quebra-cabeças 0, 1, 2 e 3, respectivamente. Observe que, por enquanto, cada uma dessas bases de conhecimento está vazia. É aí que você entra!
- O quebra-cabeça 0 é o quebra-cabeça do plano de fundo. Ele contém um único caractere, A.
- A diz “Eu sou um cavaleiro e um valete”.
- O quebra-cabeça 1 tem dois personagens: A e B.
- A diz “Nós dois somos patifes”.
- B não diz nada.
- O quebra-cabeça 2 tem dois personagens: A e B.
- A diz “Somos do mesmo tipo”.
- B diz “Somos de tipos diferentes”.
- O quebra-cabeça 3 tem três personagens: A, B e C.
- A diz “Eu sou um cavaleiro”. ou “Eu sou um patife.”, mas você não sabe qual.
- B diz “A disse 'Eu sou um patife'”.
- B então diz “C é um patife”.
- C diz “A é um cavaleiro”.
Em cada um dos quebra-cabeças acima, cada personagem é um cavaleiro ou um valete. Cada frase dita por um cavaleiro é verdadeira e cada frase dita por um patife é falsa.

### Minesweeper:
![image](https://github.com/abnercezar/CS50AI/assets/102832541/fd5601a3-3c3a-4c45-9c3e-8bdcbe862e7e)
Para você obter este tabuleiro deverá instalar o Pygame: 
Documentação: [Pygame News](https://www.pygame.org/news)
### Escreva uma IA para jogar o Campo Minado.
- Campo Minado é um jogo de quebra-cabeça que consiste em uma grade de células, onde algumas das células contêm “minas” escondidas. Clicar em uma célula que contém uma mina detona a mina e faz com que o usuário perca o jogo. Clicar em uma célula “segura” (ou seja, uma célula que não contém uma mina) revela um número que indica quantas células vizinhas – onde um vizinho é uma célula que está um quadrado à esquerda, à direita, acima, abaixo ou diagonal da célula dada – contém uma mina.

- Neste jogo Campo Minado 3x3, por exemplo, os três 1valores indicam que cada uma dessas células possui uma célula vizinha que é uma mina. Os quatro 0valores indicam que cada uma dessas células não possui nenhuma mina vizinha.
Dada esta informação, um jogador lógico poderia concluir que deve haver uma mina na célula inferior direita e que não há nenhuma mina na célula superior esquerda, pois somente nesse caso os rótulos numéricos em cada uma das outras células seriam preciso.

- O objetivo do jogo é sinalizar (ou seja, identificar) cada uma das minas. Em muitas implementações do jogo, incluindo a deste projeto, o jogador pode sinalizar uma mina clicando com o botão direito em uma célula (ou clicando com dois dedos, dependendo do computador).

- Sua principal função é a add_knownledge :
Esta função deve:
            1) marque a célula como um movimento que foi feito
            2) marque a célula como segura
            3) adicionar uma nova frase à base de conhecimento da IA
               com base no valor de `cell` e `count`
            4) marque quaisquer células adicionais como seguras ou como minas
               se puder ser concluído com base na base de conhecimento da IA
            5) adicionar novas frases à base de conhecimento da IA
               se eles podem ser inferidos a partir do conhecimento existente

### Lembre-se a depuração é essencial nesta atividade!
____
# Semana 2: Incerteza
____
![Thisiscs50](https://github.com/abnercezar/CS50x/assets/102832541/05954b62-d45d-4b1e-bac4-52d3c744cf57)



Observe que este repositório é para armazenar meus projetos e arquivos do curso CS50AI da Universidade de Harvard. Não se destina a compartilhar respostas ou encorajar a desonestidade acadêmica. Se você estiver matriculado no momento, conclua as tarefas de forma independente e consulte os materiais do curso.
