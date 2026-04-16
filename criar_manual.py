from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER, TA_LEFT

c = canvas.Canvas("Manual_Installacao_Controle_Etanol.pdf", pagesize=A4)
width, height = A4

current_y = [4*cm]

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=18,
    spaceAfter=20,
    alignment=TA_CENTER,
    textColor='#1a1a1a'
)
heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=14,
    spaceBefore=20,
    spaceAfter=10,
    textColor='#2c5282'
)
body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['Normal'],
    fontSize=11,
    spaceAfter=8,
    alignment=TA_LEFT
)
code_style = ParagraphStyle(
    'CustomCode',
    parent=styles['Code'],
    fontSize=10,
    spaceAfter=12
)

def add_page():
    c.showPage()
    current_y[0] = 3*cm

def write_text(text, style, x=2*cm):
    p = Paragraph(text, style)
    p.wrapOn(c, width - 4*cm, height)
    p.drawOn(c, x, height - current_y[0] - 1.5*cm)
    current_y[0] += 1.5*cm + (len(text) // 80) * 0.4*cm

def add_title(text):
    p = Paragraph(text, title_style)
    p.wrapOn(c, width - 4*cm, height)
    p.drawOn(c, 2*cm, height - current_y[0] - 2*cm)
    current_y[0] += 2.5*cm

def add_heading(text):
    p = Paragraph(text, heading_style)
    p.wrapOn(c, width - 4*cm, height)
    p.drawOn(c, 2*cm, height - current_y[0] - 1.5*cm)
    current_y[0] += 2*cm

def add_body(text):
    write_text(text, body_style)

def add_code(text):
    write_text(f"<font face='Courier'>{text}</font>", code_style, 2.5*cm)
    current_y[0] += 0.5*cm

add_title("MANUAL DE INSTALAÇÃO E CONFIGURAÇÃO")
add_title("Sistema de Controle de Etanol")

current_y[0] = 6*cm
add_heading("1. INTRODUÇÃO")
add_body("Este manual descreve os procedimentos necessários para instalar e configurar o sistema de controle de etanol (weighbridge/balanca). O sistema foi desenvolvido em Django 6.0.4 e utiliza banco de dados SQLite, sendo adequado para ambientes com até 4 usuários simultâneos.")

add_heading("2. REQUISITOS DO SISTEMA")
add_body("• Python 3.8 ou superior")
add_body("• Django 6.0.4")
add_body("• Biblioteca ReportLab (para geração de relatórios PDF)")
add_body("• Biblioteca WhiteNoise (para arquivos estáticos em produção)")
add_body("• Windows 10/11 (para servidor)")
add_body("• Rede local com TCP/IP configurado")
add_body("• Acesso administrativo ao Windows (para tarefa agendada)")

add_page()

add_heading("3. INSTALAÇÃO DE DEPENDÊNCIAS")
add_body("Após clonar ou copiar o projeto, instale as dependências Python necessárias:")

add_body("<b>Passo 1:</b> Abra o terminal no diretório do projeto")
add_body("<b>Passo 2:</b> Execute os seguintes comandos:")

add_code("pip install django")
add_code("pip install reportlab")
add_code("pip install whitenoise")

add_body("<b>Passo 3:</b> Execute o comando collectstatic para coletar os arquivos estáticos:")
add_code("python manage.py collectstatic --noinput")

add_body("Este comando cria a pasta 'staticfiles' com os arquivos CSS e JS necessários para o admin e outras partes do sistema funcionarem corretamente com DEBUG=False.")

add_heading("4. CONFIGURAÇÕES DO SISTEMA")
add_body("As seguintes configurações foram aplicadas ao arquivo settings.py:")

add_body("<b>DEBUG = False</b>")
add_body("Modo de produção ativado. Os arquivos estáticos são servidos pelo WhiteNoise. Erros detalhados são ocultados por segurança.")

add_body("<b>SECRET_KEY</b>")
add_body("Chave secreta para criptografar sessões e tokens de segurança.")

add_body("<b>ALLOWED_HOSTS</b>")
add_body("Configurado para aceitar conexões dos IPs: 192.168.0.25, 192.168.0.*, localhost e 127.0.0.1")

add_body("<b>STATIC_ROOT e WhiteNoise</b>")
add_body("Arquivos estáticos coletados em 'staticfiles/' e servidos pelo WhiteNoise em modo de produção.")

add_body("<b>LANGUAGE_CODE = pt-br</b>")
add_body("Interface em português brasileiro.")

add_body("<b>TIME_ZONE = America/Campo_Grande</b>")
add_body("Fuso horário de Mato Grosso do Sul.")

add_page()

add_heading("5. CONFIGURAÇÃO DO BANCO DE DADOS")
add_body("O sistema utiliza SQLite (db.sqlite3). Para aplicar migrações:")

add_code("python manage.py migrate")

add_body("Para criar o banco de dados com dados iniciais (se houver):")
add_code("python manage.py loaddata initial_data.json")

add_heading("6. CRIAR USUÁRIO ADMINISTRADOR")
add_body("Para criar um usuário administrador do sistema:")

add_body("<b>Passo 1:</b> Execute o comando:")
add_code("python manage.py createsuperuser")

add_body("<b>Passo 2:</b> Digite o nome de usuário (username)")
add_body("<b>Passo 3:</b> Digite o e-mail (opcional)")
add_body("<b>Passo 4:</b> Digite e confirme a senha")

add_page()

add_heading("7. INICIAR O SERVIDOR")
add_body("Para iniciar o servidor Django:")

add_body("<b>Modo padrão (apenas localhost):</b>")
add_code("python manage.py runserver")

add_body("<b>Modo rede (todos os dispositivos):</b>")
add_code("python manage.py runserver 0.0.0.0:8000")

add_body("O servidor estará disponível em:")
add_code("http://localhost:8000")
add_code("http://127.0.0.1:8000")

add_body("Para acesso ao painel administrativo:")
add_code("http://localhost:8000/admin/")

add_heading("8. ACESSO VIA REDE LOCAL")
add_body("Outros computadores na rede podem acessar através do IP do servidor:")

add_code("http://192.168.0.25:8000/admin/")

add_body("Obs: Certifique-se que o firewall do Windows permite conexões na porta 8000.")

add_page()

add_heading("9. SCRIPT DE AUTO-INICIALIZAÇÃO (OPCIONAL)")
add_body("Para que o sistema inicie automaticamente com o Windows:")

add_body("<b>Passo 1:</b> Execute o PowerShell como Administrador")
add_body("<b>Passo 2:</b> Execute:")
add_code("powershell -ExecutionPolicy Bypass -File C:\\Users\\edson\\Downloads\\balanca\\criar_tarefa_agendada.ps1")

add_body("Este comando cria uma tarefa agendada chamada 'Django_Balanca' que inicia automaticamente com o Windows.")

add_heading("10. TROUBLESHOOTING")
add_body("<b>Problema:</b> Página do admin sem estilização (CSS quebrado)")
add_body("<b>Solução:</b> Execute: python manage.py collectstatic")

add_body("<b>Problema:</b> Usuários não conseguem acessar pela rede")
add_body("<b>Solução:</b> Verifique se o firewall permite conexões na porta 8000")

add_body("<b>Problema:</b> Erro 'Access Denied' ao criar tarefa agendada")
add_body("<b>Solução:</b> Execute o PowerShell como Administrador")

add_body("<b>Problema:</b> ALLOWED_HOSTS erro")
add_body("<b>Solução:</b> Adicione o IP do computador ao ALLOWED_HOSTS em settings.py")

add_body("<b>Problema:</b> Erro 'ModuleNotFoundError'")
add_body("<b>Solução:</b> Verifique se todas as dependências foram instaladas (pip install django reportlab whitenoise)")

add_page()

add_heading("11. INFORMAÇÕES ADICIONAIS")
add_body("<b>Arquivo de configuração:</b> controle_etanol/settings.py")
add_body("<b>Diretório do projeto:</b> C:\\Users\\edson\\Downloads\\balanca")
add_body("<b>Banco de dados:</b> db.sqlite3")
add_body("<b>Pasta arquivos estáticos:</b> staticfiles/")
add_body("<b>Porta padrão:</b> 8000")
add_body("<b>Framework:</b> Django 6.0.4")
add_body("<b>Python:</b> 3.8+")

add_heading("12. ESTRUTURA DO PROJETO")
add_body("• controle_etanol/ - Configurações do projeto Django")
add_body("• core/ - Aplicação principal (modelos, views, admin)")
add_body("• db.sqlite3 - Banco de dados SQLite")
add_body("• staticfiles/ - Arquivos estáticos coletados")
add_body("• manage.py - Comando de gerenciamento Django")

add_body("---")
add_body("Manual gerado em 15/04/2026")
add_body("Sistema: Controle Etanol - Django 6.0.4")

c.save()
print("Manual criado com sucesso: Manual_Installacao_Controle_Etanol.pdf")