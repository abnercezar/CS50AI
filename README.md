# CS50AI - 2024
### Introdução do CS50 à Inteligência Artificial com Python
![Harvard](https://github.com/abnercezar/CS50x/assets/102832541/96a8e6ab-d1a2-40b0-8b16-21db0b3dbd7e)

### Site CS50AI: 
https://cs50.harvard.edu/ai/2024/
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
- Para implementar a pesquisa, a fronteira usada é uma fila, e crie um algoritimo de busca em largura que é empregado para encontrar o caminho mais curto no grafo.


____
### Tic-Tac-Toe:
![image](https://github.com/abnercezar/CS50AI/assets/102832541/1e5591b6-37ed-48ec-b946-c0e7584014c9)

Para você obter este tabuleiro deverá instalar o Pygame: 
Documentação: [Pygame News](https://www.pygame.org/news)

- Usando a função Minimax, que é uma das mais importantes, a IA deve jogar Tic-Tac-Toe de maneira ideal.
- O tabuleiro é fornecido para você (runner.py), porém é necessário implementar uma função Minimax na sua(tictactoe.py) entre outras não menos importantes. Sua IA deve fazer uma cópia do tabuleiro e calcular todas as possíveis jogadas do seu oponente. Ela pode até permitir que o oponente empate, mas não pode permitir que ele a vença.
  
  #### OBS: A depuração é essencial nesta atividade!

  ____
# Semana 1: Conhecimento
  ### Knights:
 ### Escreva um programa para resolver quebra-cabeças lógicos.
 - Não há necessidade de entender tudo neste arquivo, mas observe que ele define diversas classes para diferentes tipos de conectivos lógicos. Essas classes podem ser compostas umas dentro das outras, portanto, uma expressão como And(Not(A), Or(B, C))representa a sentença lógica afirmando que o símbolo A não é verdadeiro e que o símbolo B ou símbolo C é verdadeiro (onde “ou” aqui se refere a inclusivo, não exclusivo ou).
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

 
Uma das principais função deve ser a add_knowledge e ela deverá:
1. Marcar a célula como um movimento que foi feito
2. Marcar a célula como segura
3. Adicionar uma nova frase à base de conhecimento da IA com base no valor de `cell` e `count`
4. Marcar quaisquer células adicionais como seguras ou como minas se puder ser concluído com base na base de conhecimento da IA
5. Adicionar novas frases à base de conhecimento da IA se eles podem ser inferidos a partir do conhecimento existente

 #### OBS: A depuração é essencial nesta atividade!
____
# Semana 2: Incerteza
### Pagerank
![image](https://github.com/abnercezar/CS50AI/assets/102832541/be8bcf94-ef53-4fe3-a152-36112d726c45)
### Escreva uma IA para classificar as páginas da web por importância.

Quando mecanismos de pesquisa como o Google exibem resultados de pesquisa, eles o fazem colocando páginas mais “importantes” e de maior qualidade em uma posição superior nos resultados de pesquisa do que páginas menos importantes. Mas como o mecanismo de busca sabe quais páginas são mais importantes que outras páginas?

Uma heurística pode ser que uma página “importante” seja aquela para a qual muitas outras páginas têm links, já que é razoável imaginar que mais sites terão links para uma página da Web de qualidade superior do que para uma página da Web de qualidade inferior. Poderíamos, portanto, imaginar um sistema onde cada página recebe uma classificação de acordo com o número de links recebidos de outras páginas, e classificações mais altas sinalizariam maior importância.

Mas esta definição não é perfeita: se alguém quiser fazer com que sua página pareça mais importante, então, sob esse sistema, ele poderia simplesmente criar muitas outras páginas com links para a página desejada para aumentar artificialmente sua classificação.

Por esse motivo, o algoritmo PageRank foi criado pelos cofundadores do Google (incluindo Larry Page, que deu nome ao algoritmo). No algoritmo do PageRank, um site é mais importante se estiver vinculado a outros sites importantes, e links de sites menos importantes têm menos peso. Esta definição parece um pouco circular, mas acontece que existem múltiplas estratégias para calcular essas classificações.

Para o desenvolvimento deste algoritimo, você precisará de algumas funções:

def crawl:
    Analise um diretório de páginas HTML e verifique links para outras páginas.
    Retorne um dicionário onde cada chave é uma página e os valores são
    uma lista de todas as outras páginas do corpus vinculadas pela página.

def transition_model:
    Retornar uma distribuição de probabilidade sobre qual página visitar em seguida,
    dada uma página atual.
    Com probabilidade `damping_factor`, escolha um link aleatoriamente
    vinculado por `página`. Com probabilidade `1 - fator de amortecimento`, escolha
    um link escolhido aleatoriamente em todas as páginas do corpus.

def sample_pagerank:
    Retorne valores de PageRank para cada página amostrando `n` páginas
    de acordo com o modelo de transição, começando com uma página aleatória.
    Retorne um dicionário onde as chaves são nomes de páginas e os valores são
    seu valor estimado de PageRank (um valor entre 0 e 1). Todos
    Os valores do PageRank devem somar 1.

def iterate_pagerank:
    Retorne valores de PageRank para cada página atualizando iterativamente
    Valores do PageRank até a convergência.
    Retorne um dicionário onde as chaves são nomes de páginas e os valores são
    seu valor estimado de PageRank (um valor entre 0 e 1). Todos
    Os valores do PageRank devem somar 1. 

____

### Heredity
![image](https://github.com/abnercezar/CS50AI/assets/102832541/a9ab42c1-6835-4e67-966f-435937f502ed)

### Escreva uma IA para avaliar a probabilidade de uma pessoa ter uma característica genética específica.

Para resolver esta tarefa você precisará tarbalhar duramente na função joint_probability
A joint_probability função deve ter como entrada um dicionário de pessoas, junto com dados sobre quem tem quantas cópias de cada um dos genes e quem apresenta a característica. 

A função deve retornar a probabilidade conjunta de todos esses eventos ocorrerem.

Calcule e retorne uma probabilidade conjunta.
  A probabilidade retornada deve ser a probabilidade de que
      * todos no conjunto `one_gene` possuem uma cópia do gene, e
      * todos no conjunto `two_genes` possuem duas cópias do gene, e
      * todos que não estão em `one_gene` ou `two_gene` não possuem o gene, e
      * todos no conjunto `have_trait` possuem a característica, e
      * todos que não estão no set` have_trait` não possuem a característica. 
      
  def inherit_prob:
     É uma função auxiliar de joint_probability
     Retorna a probabilidade de um pai dar uma cópia do gene mutado ao filho.
    Leva:
    - parent_name - o nome do pai
    - one_gene - conjunto de pessoas que possuem 1 cópia do gene
    - two_genes - conjunto de pessoas que possuem duas cópias do gene.

  def update:
    Adicione às `probabilidades` uma nova probabilidade conjunta `p`.
    Cada pessoa deve ter suas distribuições de “genes” e “características” atualizadas.
    Qual valor para cada distribuição é atualizado depende se
    a pessoa está em `have_gene` e `have_trait`, respectivamente.

  def normalize:
    Atualize as `probabilidades` de modo que cada distribuição de probabilidade
    é normalizado (ou seja, soma 1, com proporções relativas iguais).
____

# Semana 3 Otimização

### Palavras Cruzadas
![image](https://github.com/abnercezar/CS50AI/assets/102832541/86adc928-077f-46e5-8b80-f247cd3c45e4)

### Escreva uma IA para gerar palavras cruzadas.
Meu desafio maior nesta semana foi que todos os meus testes estavam passando, e meu código estava correto, 
mas o arquivo `OpensSans-Regular.ttf` não havia sido baixado, junto com a pasta `crossword`, por este motivo ao executar este trecho meu código quebrava.


![image](https://github.com/abnercezar/CS50AI/assets/102832541/46ffe2f2-963b-40d8-b44f-d015dd47e943)

____

# Semana 4 Aprendizado

### Compras
![image](https://github.com/abnercezar/CS50AI/assets/102832541/d7d57afb-4f5f-404b-a566-ce814a7c9788)

### Escreva uma IA para prever se os clientes de compras online concluirão uma compra.

Nesta semana a função principal é `load_data`, onde você precisará carregar os dados de compra de um arquivo CSV `filename` e converter-os em uma lista de evidências e uma lista de rótulos. 
 E retornar uma tupla (evidências, rótulos). A evidência deve ser uma lista de listas onde cada lista contém os seguintes valores em ordem:
- Administrativo, na íntegra
        - Administrative_Duration, um número de ponto flutuante
        - Informativo, na íntegra
        - Informational_Duration, um número de ponto flutuante
        - ProductRelated, um número inteiro
        - ProductRelated_Duration, um número de ponto flutuante
        - BounceRates, um número de ponto flutuante
        - ExitRates, um número de ponto flutuante
        - PageValues, um número de ponto flutuante
        - SpecialDay, um número de ponto flutuante
        - Mês, um índice de 1 (janeiro) a 12 (dezembro)
        - Sistemas Operacionais, um número inteiro
        - Navegador, um número inteiro
        - Região, um número inteiro
        - TrafficType, um número inteiro
        - VisitorType, um número inteiro 1 (Returning_Visitor), 2 (New_Visitor) ou 3 (Outro)
        - Fim de semana, um número inteiro 0 (se for falso) ou 1 (se for verdadeiro)

    Os rótulos devem ser a lista correspondente de rótulos, onde cada rótulo
    é 1 se Receita for verdadeira e 0 caso contrário.

- Você também deverá implementar a fução `train_mode` que fará o seguinte:
Dada uma lista de listas de evidências e uma lista de rótulos, retorne um
    modelo ajustado de k-vizinho mais próximo (k = 1) treinado nos dados.

- E deverá implementar por último a função `evaluate` que fará o seguinte:
Dada uma lista de rótulos reais e uma lista de rótulos previstos,
    retornar uma tupla (sensibilidade, especificidade).

    Suponha que cada rótulo seja 1 (positivo) ou 0 (negativo).

    `sensibilidade` deve ser um valor de ponto flutuante de 0 a 1
    representando a "taxa positiva verdadeira": a proporção de
    rótulos positivos reais que foram identificados com precisão.

    `especificidade` deve ser um valor de ponto flutuante de 0 a 1
    representando a "taxa verdadeiramente negativa": a proporção de
    rótulos negativos reais que foram identificados com precisão.

____
![Thisiscs50](https://github.com/abnercezar/CS50x/assets/102832541/05954b62-d45d-4b1e-bac4-52d3c744cf57)



Observe que este repositório é para armazenar meus projetos e arquivos do curso CS50AI da Universidade de Harvard. Não se destina a compartilhar respostas ou encorajar a desonestidade acadêmica. Se você estiver matriculado no momento, conclua as tarefas de forma independente e consulte os materiais do curso.
