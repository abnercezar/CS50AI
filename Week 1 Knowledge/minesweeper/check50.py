import check50

@check50.check()
def exists():
    """Verifica se o arquivo Minesweeper.py existe."""
    check50.exists("Minesweeper.py")

@check50.check(exists)
def test1():
    """Testa a funcionalidade 1 do jogo Minesweeper."""
    # Adicione aqui o código para testar a funcionalidade 1 do jogo

@check50.check(exists)
def test2():
    """Testa a funcionalidade 2 do jogo Minesweeper."""
    # Adicione aqui o código para testar a funcionalidade 2 do jogo

# Continue adicionando funções de teste conforme necessário
