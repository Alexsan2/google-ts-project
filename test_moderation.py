
import pytest
from playwright.sync_api import sync_playwright

# Massa de dados com o BUG SIMULADO na MariaSilva (linha 11)
DENUNCIAS = [
    {"id": "DEN-101", "usuario": "SpamBot99", "conteúdo": "GANHE DINHEIRO FÁCIL CLICANDO AQUI!", "acao_esperada": "BLOQUEAR"},
    {"id": "DEN-102", "usuario": "MariaSilva", "conteúdo": "Adorei o artigo sobre Python, muito obrigado!", "acao_esperada": "BLOQUEAR"}
]

@pytest.mark.parametrize("caso", DENUNCIAS)
def test_painel_de_moderacao_ts(caso):
    with sync_playwright() as p:
        # Mantemos o navegador visível para você ver a falha acontecendo
        browser = p.chromium.launch(headless=False, slow_mo=1000) 
        page = browser.new_context().new_page()
        
        # Interface de simulação (O painel real do sistema)
        html_painel = f"""
        <html>
            <body>
                <h2>Painel de Moderação Trust & Safety</h2>
                <div id="ticket">
                    <p><b>ID da Denúncia:</b> <span id="id-denuncia">{caso['id']}</span></p>
                    <p><b>Autor:</b> {caso['usuario']}</p>
                    <p><b>Conteúdo Denunciado:</b> <span id="texto-post">{caso['conteúdo']}</span></p>
                </div>
                <hr>
                <button id="btn-aprovar" onclick="document.getElementById('ticket').innerHTML='<h3>CONTEÚDO APROVADO</h3>'">Aprovar Conteúdo</button>
                <button id="btn-bloquear" onclick="document.getElementById('ticket').innerHTML='<h3>USUÁRIO BLOQUEADO E BANIDO</h3>'">Bloquear Usuário</button>
            </body>
        </html>
        """
        
        page.set_content(html_painel)
        
        # 1. Valida o ID na tela
        id_na_tela = page.locator("#id-denuncia").inner_text()
        assert id_na_tela == caso["id"]
        
        # 2. Execução da ação (Aqui a MariaSilva vai tentar ser bloqueada)
        if caso["acao_esperada"] == "BLOQUEAR":
            page.locator("#btn-bloquear").click()
            
            # O teste vai travar aqui na MariaSilva! 
            # Porque o botão de bloquear vai dizer "USUÁRIO BLOQUEADO E BANIDO", 
            # mas o sistema/teste deveria esperar que um comentário bom fosse aprovado.
            assert page.locator("h3").inner_text() == "USUÁRIO BLOQUEADO E BANIDO"
            
        elif caso["acao_esperada"] == "APROVAR":
            page.locator("#btn-aprovar").click()
            assert page.locator("h3").inner_text() == "CONTEÚDO APROVADO"
            
        browser.close()