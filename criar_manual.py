from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import HexColor

PROJETO_DIR = r"C:\ProjetoFilaCarregamento"
PDF_FILENAME = "Manual_Instalacao_Controle_Etanol.pdf"

c = canvas.Canvas(PDF_FILENAME, pagesize=A4)
width, height = A4

current_y = [4 * cm]

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=20,
    spaceAfter=20,
    alignment=TA_CENTER,
    textColor=HexColor('#073B4C'),
)
subtitle_style = ParagraphStyle(
    'CustomSubtitle',
    parent=styles['Heading2'],
    fontSize=13,
    spaceAfter=14,
    alignment=TA_CENTER,
    textColor=HexColor('#334155'),
)
heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=14,
    spaceBefore=20,
    spaceAfter=10,
    textColor=HexColor('#0E7490'),
)
subheading_style = ParagraphStyle(
    'CustomSubHeading',
    parent=styles['Heading3'],
    fontSize=12,
    spaceBefore=12,
    spaceAfter=8,
    textColor=HexColor('#124E63'),
)
body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['Normal'],
    fontSize=11,
    spaceAfter=8,
    alignment=TA_LEFT,
)
code_style = ParagraphStyle(
    'CustomCode',
    parent=styles['Code'],
    fontSize=10,
    spaceAfter=12,
    backColor=HexColor('#F1F5F9'),
    borderColor=HexColor('#CBD5E1'),
    borderWidth=0.5,
    borderPadding=4,
)
note_style = ParagraphStyle(
    'CustomNote',
    parent=styles['Normal'],
    fontSize=10,
    spaceAfter=8,
    textColor=HexColor('#64748B'),
    leftIndent=20,
)

MAX_Y = 24 * cm  # Limite antes de forçar nova página


def check_page():
    """Verifica se precisa criar nova página."""
    if current_y[0] >= MAX_Y:
        add_page()


def add_page():
    c.showPage()
    current_y[0] = 3 * cm


def write_text(text, style, x=2 * cm):
    check_page()
    p = Paragraph(text, style)
    pw, ph = p.wrapOn(c, width - 4 * cm, height)
    p.drawOn(c, x, height - current_y[0] - ph)
    current_y[0] += ph + 0.3 * cm


def add_title(text):
    check_page()
    p = Paragraph(text, title_style)
    pw, ph = p.wrapOn(c, width - 4 * cm, height)
    p.drawOn(c, 2 * cm, height - current_y[0] - ph)
    current_y[0] += ph + 0.5 * cm


def add_subtitle(text):
    write_text(text, subtitle_style)


def add_heading(text):
    check_page()
    write_text(text, heading_style)


def add_subheading(text):
    check_page()
    write_text(text, subheading_style)


def add_body(text):
    write_text(text, body_style)


def add_note(text):
    write_text(text, note_style)


def add_code(text):
    write_text(f"<font face='Courier'>{text}</font>", code_style, 2.5 * cm)


# ============================================================================
# CAPA
# ============================================================================
current_y[0] = 8 * cm
add_title("MANUAL DE INSTALAÇÃO E CONFIGURAÇÃO")
add_title("Sistema de Controle de Fila de Carregamento de Etanol")
current_y[0] += 1 * cm
add_subtitle(f"Diretório de instalação: {PROJETO_DIR}")
add_subtitle("Versão: Django 6.0.4 — Python 3.13+")
add_subtitle("Data: 24/04/2026")

add_page()

# ============================================================================
# 1. INTRODUÇÃO
# ============================================================================
add_heading("1. INTRODUÇÃO")
add_body(
    "Este manual descreve os procedimentos completos para instalar e configurar o "
    "Sistema de Controle de Fila de Carregamento de Etanol. O sistema foi desenvolvido "
    "em Django 6.0.4 e utiliza banco de dados SQLite, sendo adequado para ambientes "
    "com até 4 usuários simultâneos em rede local."
)
add_body(
    f"Todos os arquivos do projeto devem ser instalados na pasta "
    f"<b>{PROJETO_DIR}</b>."
)

# ============================================================================
# 2. REQUISITOS DO SISTEMA
# ============================================================================
add_heading("2. REQUISITOS DO SISTEMA")
add_subheading("2.1 Hardware mínimo")
add_body("• Processador: Intel Core i3 ou equivalente")
add_body("• Memória RAM: 4 GB")
add_body("• Espaço em disco: 500 MB livres")
add_body("• Rede local com TCP/IP configurado")

add_subheading("2.2 Software necessário")
add_body("• Windows 10 ou Windows 11")
add_body("• Python 3.13 ou superior")
add_body("• Acesso administrativo ao Windows (para tarefa agendada)")
add_body("• Navegador web atualizado (Chrome, Edge ou Firefox)")

# ============================================================================
# 3. DOWNLOAD E INSTALAÇÃO DO PYTHON
# ============================================================================
add_heading("3. DOWNLOAD E INSTALAÇÃO DO PYTHON")
add_subheading("3.1 Baixar o Python")
add_body("<b>Passo 1:</b> Acesse o site oficial do Python:")
add_code("https://www.python.org/downloads/")
add_body("<b>Passo 2:</b> Clique no botão <b>\"Download Python 3.13.x\"</b> (versão mais recente).")
add_body("<b>Passo 3:</b> Salve o arquivo <b>python-3.13.x-amd64.exe</b> em local de fácil acesso.")

add_subheading("3.2 Instalar o Python")
add_body("<b>Passo 1:</b> Execute o instalador <b>python-3.13.x-amd64.exe</b> como Administrador.")
add_body(
    '<b>Passo 2:</b> <font color="red"><b>IMPORTANTE:</b></font> Na tela inicial, '
    'marque a opção <b>"Add python.exe to PATH"</b> (Adicionar Python ao PATH).'
)
add_body('<b>Passo 3:</b> Clique em <b>"Install Now"</b> (Instalar Agora).')
add_body("<b>Passo 4:</b> Aguarde a instalação finalizar e clique em <b>\"Close\"</b>.")

add_subheading("3.3 Verificar a instalação")
add_body("Abra o <b>Prompt de Comando</b> (cmd) ou <b>PowerShell</b> e execute:")
add_code("python --version")
add_body("O resultado deve ser algo como: <b>Python 3.13.x</b>")
add_body("Verifique também o pip (gerenciador de pacotes):")
add_code("pip --version")

# ============================================================================
# 4. COPIAR O PROJETO
# ============================================================================
add_heading("4. COPIAR ARQUIVOS DO PROJETO")
add_body(
    f"<b>Passo 1:</b> Crie a pasta <b>{PROJETO_DIR}</b> "
    f"(caso não exista)."
)
add_code(f'mkdir "{PROJETO_DIR}"')
add_body(
    f"<b>Passo 2:</b> Copie todos os arquivos do projeto para dentro de "
    f"<b>{PROJETO_DIR}</b>."
)
add_body(
    "A estrutura final deve conter pelo menos os seguintes arquivos e pastas:"
)
add_body(f"• {PROJETO_DIR}\\manage.py")
add_body(f"• {PROJETO_DIR}\\db.sqlite3")
add_body(f"• {PROJETO_DIR}\\controle_etanol\\ (pasta de configurações)")
add_body(f"• {PROJETO_DIR}\\core\\ (aplicação principal)")
add_body(f"• {PROJETO_DIR}\\templates\\ (templates HTML)")
add_body(f"• {PROJETO_DIR}\\staticfiles\\ (arquivos estáticos)")
add_body(f"• {PROJETO_DIR}\\iniciar_balanca.bat")
add_body(f"• {PROJETO_DIR}\\criar_tarefa_agendada.ps1")

# ============================================================================
# 5. INSTALAÇÃO DE DEPENDÊNCIAS (PACOTES PYTHON)
# ============================================================================
add_heading("5. INSTALAÇÃO DE DEPENDÊNCIAS (PACOTES PYTHON)")
add_body(
    "Abra o <b>Prompt de Comando</b> (cmd) ou <b>PowerShell</b> e execute os "
    "comandos abaixo, um por vez:"
)

add_subheading("5.1 Django (framework web)")
add_code("pip install django")
add_note("Framework web principal do sistema. Versão necessária: 6.0.4 ou superior.")

add_subheading("5.2 ReportLab (geração de relatórios PDF)")
add_code("pip install reportlab")
add_note("Biblioteca para gerar relatórios em formato PDF.")

add_subheading("5.3 OpenPyXL (geração de planilhas Excel)")
add_code("pip install openpyxl")
add_note("Biblioteca para gerar relatórios em formato Excel (.xlsx).")

add_subheading("5.4 WhiteNoise (arquivos estáticos em produção)")
add_code("pip install whitenoise")
add_note("Serve arquivos CSS/JS quando o modo DEBUG está desativado.")

add_subheading("5.5 Comando rápido — instalar tudo de uma vez")
add_body("Você pode instalar todas as dependências com um único comando:")
add_code("pip install django reportlab openpyxl whitenoise")

# ============================================================================
# 6. CONFIGURAÇÃO INICIAL DO SISTEMA
# ============================================================================
add_heading("6. CONFIGURAÇÃO INICIAL DO SISTEMA")
add_body(
    f"Abra o <b>Prompt de Comando</b> e navegue até a pasta do projeto:"
)
add_code(f'cd /d "{PROJETO_DIR}"')

add_subheading("6.1 Aplicar migrações do banco de dados")
add_body("Este comando cria/atualiza as tabelas no banco SQLite:")
add_code("python manage.py migrate")

add_subheading("6.2 Coletar arquivos estáticos")
add_body(
    "Este comando cria a pasta 'staticfiles' com os arquivos CSS e JS "
    "necessários para o sistema funcionar em modo de produção (DEBUG=False):"
)
add_code("python manage.py collectstatic --noinput")

add_subheading("6.3 Criar usuário administrador")
add_body("Para criar o primeiro usuário administrador do sistema:")
add_code("python manage.py createsuperuser")
add_body("<b>Passo 1:</b> Digite o nome de usuário (username)")
add_body("<b>Passo 2:</b> Digite o e-mail (opcional, pode deixar em branco)")
add_body("<b>Passo 3:</b> Digite e confirme a senha")
add_note(
    "Guarde as credenciais em local seguro. Este será o usuário principal "
    "com acesso ao painel administrativo."
)

# ============================================================================
# 7. CONFIGURAÇÕES DO SETTINGS.PY
# ============================================================================
add_heading("7. CONFIGURAÇÕES DO SISTEMA (settings.py)")
add_body(
    "As seguintes configurações já estão aplicadas no arquivo "
    "<b>controle_etanol/settings.py</b>:"
)

add_body("<b>DEBUG = False</b>")
add_body(
    "Modo de produção ativado. Erros detalhados são ocultados por segurança. "
    "Arquivos estáticos servidos pelo WhiteNoise."
)

add_body("<b>ALLOWED_HOSTS</b>")
add_body(
    "Configurado para aceitar conexões de: 192.168.0.14, 192.168.0.25, "
    "192.168.0.*, localhost e 127.0.0.1."
)
add_note(
    "Se o IP do servidor for diferente, edite o ALLOWED_HOSTS no arquivo "
    "settings.py e adicione o IP correto."
)

add_body("<b>LANGUAGE_CODE = pt-br</b>")
add_body("Interface em português brasileiro.")

add_body("<b>TIME_ZONE = America/Campo_Grande</b>")
add_body("Fuso horário de Mato Grosso do Sul.")

add_body("<b>SESSION_COOKIE_AGE = 7200</b>")
add_body("Sessão expira após 2 horas de inatividade.")

# ============================================================================
# 8. INICIAR O SERVIDOR
# ============================================================================
add_heading("8. INICIAR O SERVIDOR")
add_body(
    f"Abra o <b>Prompt de Comando</b> e navegue até a pasta do projeto:"
)
add_code(f'cd /d "{PROJETO_DIR}"')

add_subheading("8.1 Modo padrão (apenas localhost)")
add_code("python manage.py runserver")
add_body("Acesse: <b>http://localhost:8000</b>")

add_subheading("8.2 Modo rede (todos os dispositivos da rede local)")
add_code("python manage.py runserver 0.0.0.0:8000")
add_body("Acesse de outros computadores: <b>http://IP_DO_SERVIDOR:8000</b>")
add_body("Exemplo: <b>http://192.168.0.14:8000</b>")

add_subheading("8.3 Inicialização rápida via BAT")
add_body(
    f"Utilize o arquivo <b>iniciar_balanca.bat</b> na pasta do projeto "
    f"para iniciar o servidor com duplo-clique."
)

add_subheading("8.4 Painel administrativo")
add_body("Para acessar o painel admin do Django:")
add_code("http://localhost:8000/admin/")

# ============================================================================
# 9. ACESSO VIA REDE LOCAL
# ============================================================================
add_heading("9. ACESSO VIA REDE LOCAL")
add_body(
    "Outros computadores na rede local podem acessar o sistema através do "
    "IP do servidor (computador onde o sistema está instalado)."
)
add_body("Exemplo de acesso via navegador:")
add_code("http://192.168.0.14:8000")

add_subheading("9.1 Liberar porta no Firewall do Windows")
add_body(
    "<b>Passo 1:</b> Abra o <b>Painel de Controle</b> → "
    "<b>Sistema e Segurança</b> → <b>Firewall do Windows Defender</b>"
)
add_body("<b>Passo 2:</b> Clique em <b>\"Configurações avançadas\"</b>")
add_body("<b>Passo 3:</b> Clique em <b>\"Regras de Entrada\"</b> → <b>\"Nova Regra\"</b>")
add_body("<b>Passo 4:</b> Selecione <b>\"Porta\"</b> → Avançar")
add_body("<b>Passo 5:</b> Selecione <b>\"TCP\"</b> e digite <b>8000</b> → Avançar")
add_body("<b>Passo 6:</b> Selecione <b>\"Permitir a conexão\"</b> → Avançar")
add_body('<b>Passo 7:</b> Marque <b>Domínio</b>, <b>Particular</b> e <b>Público</b> → Avançar')
add_body('<b>Passo 8:</b> Dê o nome <b>"Django Fila Carregamento"</b> → Concluir')

add_note(
    "Alternativamente, execute o seguinte comando no PowerShell como Administrador:"
)
add_code(
    'New-NetFirewallRule -DisplayName "Django Fila Carregamento" '
    '-Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow'
)

# ============================================================================
# 10. AUTO-INICIALIZAÇÃO COM O WINDOWS
# ============================================================================
add_heading("10. AUTO-INICIALIZAÇÃO COM O WINDOWS (OPCIONAL)")
add_body(
    "Para que o sistema inicie automaticamente quando o Windows ligar:"
)

add_subheading("10.1 Usando o script PowerShell")
add_body("<b>Passo 1:</b> Abra o <b>PowerShell como Administrador</b>")
add_body("<b>Passo 2:</b> Execute o comando abaixo:")
add_code(
    f'powershell -ExecutionPolicy Bypass -File "{PROJETO_DIR}\\criar_tarefa_agendada.ps1"'
)
add_body(
    "Este comando cria uma tarefa agendada chamada <b>'Django_Balanca'</b> "
    "que inicia automaticamente com o Windows."
)

add_subheading("10.2 Verificar a tarefa agendada")
add_body(
    "Abra o <b>Agendador de Tarefas</b> do Windows (taskschd.msc) e verifique "
    "se a tarefa <b>'Django_Balanca'</b> aparece na lista."
)

# ============================================================================
# 11. RESUMO DE TODOS OS COMANDOS
# ============================================================================
add_heading("11. RESUMO DE TODOS OS COMANDOS")
add_body(
    "Abaixo está a sequência completa de comandos para uma instalação do zero:"
)
add_body("")

add_body("<b>1. Verificar Python instalado:</b>")
add_code("python --version")

add_body("<b>2. Instalar dependências Python:</b>")
add_code("pip install django reportlab openpyxl whitenoise")

add_body(f"<b>3. Acessar pasta do projeto:</b>")
add_code(f'cd /d "{PROJETO_DIR}"')

add_body("<b>4. Aplicar migrações do banco:</b>")
add_code("python manage.py migrate")

add_body("<b>5. Coletar arquivos estáticos:</b>")
add_code("python manage.py collectstatic --noinput")

add_body("<b>6. Criar usuário administrador:</b>")
add_code("python manage.py createsuperuser")

add_body("<b>7. Iniciar o servidor (modo rede):</b>")
add_code("python manage.py runserver 0.0.0.0:8000")

# ============================================================================
# 12. TROUBLESHOOTING
# ============================================================================
add_heading("12. RESOLUÇÃO DE PROBLEMAS")

add_body("<b>Problema:</b> Comando 'python' não reconhecido")
add_body(
    "<b>Solução:</b> O Python não foi adicionado ao PATH. Reinstale o Python "
    "marcando a opção \"Add python.exe to PATH\"."
)

add_body("<b>Problema:</b> Erro 'ModuleNotFoundError'")
add_body(
    "<b>Solução:</b> Um ou mais pacotes não foram instalados. Execute: "
    "<font face='Courier'>pip install django reportlab openpyxl whitenoise</font>"
)

add_body("<b>Problema:</b> Página sem estilização (CSS/JS não carrega)")
add_body(
    "<b>Solução:</b> Execute: "
    "<font face='Courier'>python manage.py collectstatic --noinput</font>"
)

add_body("<b>Problema:</b> Não consigo acessar de outro computador na rede")
add_body(
    "<b>Solução:</b> Verifique se o firewall permite conexões na porta 8000 "
    "(ver seção 9.1) e se o servidor foi iniciado com "
    "<font face='Courier'>0.0.0.0:8000</font>."
)

add_body("<b>Problema:</b> Erro 'ALLOWED_HOSTS'")
add_body(
    "<b>Solução:</b> Adicione o IP do computador ao ALLOWED_HOSTS em "
    "<font face='Courier'>controle_etanol/settings.py</font>"
)

add_body("<b>Problema:</b> Erro 'Access Denied' ao criar tarefa agendada")
add_body("<b>Solução:</b> Execute o PowerShell como Administrador.")

add_body("<b>Problema:</b> Esqueci a senha do administrador")
add_body(
    "<b>Solução:</b> Execute: "
    f"<font face='Courier'>cd /d \"{PROJETO_DIR}\" &amp;&amp; "
    f"python manage.py changepassword NOME_USUARIO</font>"
)

# ============================================================================
# 13. INFORMAÇÕES ADICIONAIS
# ============================================================================
add_heading("13. INFORMAÇÕES ADICIONAIS")
add_body(f"<b>Diretório do projeto:</b> {PROJETO_DIR}")
add_body("<b>Arquivo de configuração:</b> controle_etanol\\settings.py")
add_body("<b>Banco de dados:</b> db.sqlite3")
add_body("<b>Pasta de arquivos estáticos:</b> staticfiles\\")
add_body("<b>Porta padrão:</b> 8000")
add_body("<b>Framework:</b> Django 6.0.4")
add_body("<b>Python:</b> 3.13+")
add_body("<b>Banco de dados:</b> SQLite 3")

add_heading("14. ESTRUTURA DO PROJETO")
add_body(f"• controle_etanol\\ — Configurações do projeto Django (settings.py, urls.py)")
add_body("• core\\ — Aplicação principal (modelos, views, admin, formulários)")
add_body("• templates\\ — Templates HTML do sistema")
add_body("• staticfiles\\ — Arquivos estáticos coletados (CSS, JS, imagens)")
add_body("• db.sqlite3 — Banco de dados SQLite")
add_body("• manage.py — Comando de gerenciamento Django")
add_body("• iniciar_balanca.bat — Script para iniciar o servidor")
add_body("• criar_tarefa_agendada.ps1 — Script para auto-inicialização")

add_body("—" * 40)
add_body("Manual gerado em 24/04/2026")
add_body("Sistema: Controle de Fila de Carregamento de Etanol — Django 6.0.4")

c.save()
print(f"Manual criado com sucesso: {PDF_FILENAME}")