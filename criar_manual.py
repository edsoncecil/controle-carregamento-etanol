from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_CENTER, TA_LEFT

c = canvas.Canvas("Manual_Installacao_Controle_Etanol.pdf", pagesize=A4)
width, height = A4

current_y = [4*cm]  # Use list to modify in nested functions

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
add_body("Este manual descreve os procedimentos necessários para instalar e configurar o sistema de controle de etanol (weighbridge). O sistema foi desenvolvido em Django e utiliza banco de dados SQLite, sendo adequado para ambientes com até 4 usuários simultâneos.")

add_heading("2. REQUISITOS DO SISTEMA")
add_body("• Python 3.8 ou superior")
add_body("• Django 6.0.4")
add_body("• Windows 10/11 (para servidor)")
add_body("• Rede local com TCP/IP configurado")
add_body("• Acesso administrativo ao Windows (para tarefa agendada)")

add_heading("3. CONFIGURAÇÕES APLICADAS")
add_body("As seguintes configurações foram aplicadas ao arquivo settings.py:")

add_body("<b>DEBUG = False</b>")
add_body("Desabilita o modo de depuração do Django. Isso é essencial para ambientes de produção, pois oculta mensagens de erro detalhadas que poderiam expor informações sensíveis do sistema.")

add_body("<b>SECRET_KEY</b>")
add_body("Uma chave secreta segura foi gerada automaticamente. Esta chave é usada para criptografar sessões e tokens de segurança no Django.")

add_body("<b>ALLOWED_HOSTS</b>")
add_body("Configurado para aceitar conexões dos IPs: 192.168.0.25, 192.168.0.*, localhost e 127.0.0.1")

add_page()

add_heading("4. SCRIPT DE AUTO-INICIALIZAÇÃO")
add_body("Para que o sistema inicie automaticamente junto com o Windows, foi criado um script batch que deve ser configurado como tarefa agendada.")

add_body("<b>Passo 1:</b> Execute o PowerShell como Administrador")
add_body("Clique com o botão direito no menu Iniciar e selecione 'Windows PowerShell (Administrador)'")

add_body("<b>Passo 2:</b> Execute o script de criação da tarefa")
add_code("powershell -ExecutionPolicy Bypass -File C:\\Users\\edson\\Downloads\\balanca\\criar_tarefa_agendada.ps1")

add_body("Este comando criará uma tarefa agendada chamada 'Django_Balanca' que será executada automaticamente a cada vez que o Windows iniciar.")

add_heading("5. COMO GERAR NOVA SECRET_KEY")
add_body("Se por algum motivo você precisar gerar uma nova SECRET_KEY, siga os passos abaixo:")

add_body("<b>Passo 1:</b> Abra o terminal (prompt de comando)")
add_body("<b>Passo 2:</b> Execute o seguinte comando:")
add_code('python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"')

add_body("<b>Passo 3:</b> Copie a chave gerada")
add_body("<b>Passo 4:</b> Atualize o arquivo controle_etanol/settings.py substituindo o valor de SECRET_KEY pela nova chave")

add_page()

add_heading("6. ACESSO DOS USUÁRIOS")
add_body("Após o servidor estar em execução, os usuários da rede interna poderão acessar o sistema através do seguinte endereço:")

add_code("http://192.168.0.25:8000")

add_body("Para acesso ao painel administrativo, utilize:")
add_code("http://192.168.0.25:8000/admin/")

add_heading("7. CRIAR USUÁRIO ADMINISTRADOR")
add_body("Para criar um novo usuário administrador, execute os seguintes passos:")

add_body("<b>Passo 1:</b> Abra o terminal no diretório do projeto")
add_body("<b>Passo 2:</b> Execute:")
add_code("python manage.py createsuperuser")

add_body("<b>Passo 3:</b> Siga as instruções na tela para definir username e senha")

add_heading("8. INICIAR O SERVIDOR MANUALMENTE")
add_body("Se você preferir iniciar o servidor manualmente (sem auto-inicialização), execute:")

add_code("python manage.py runserver 0.0.0.0:8000")

add_body("O servidor estará disponível em http://localhost:8000")

add_page()

add_heading("9. TROUBLESHOOTING")
add_body("<b>Problema:</b> Usuários não conseguem acessar")
add_body("<b>Solução:</b> Verifique se o firewall do Windows permite conexões na porta 8000. Caso não permita, crie uma regra de entrada.")

add_body("<b>Problema:</b> Erro 'Access Denied' ao criar tarefa agendada")
add_body("<b>Solução:</b> Execute o PowerShell como Administrador")

add_body("<b>Problema:</b> Página não carrega")
add_body("<b>Solução:</b> Verifique se o servidor está em execução. Reinicie com: python manage.py runserver 0.0.0.0:8000")

add_body("<b>Problema:</b> ALLOWED_HOSTS erro")
add_body("<b>Solução:</b> Adicione o IP do computador ao ALLOWED_HOSTS em settings.py")

add_heading("10. INFORMAÇÕES ADICIONAIS")
add_body("<b>Arquivo de configuração:</b> controle_etanol/settings.py")
add_body("<b>Diretório do projeto:</b> C:\\Users\\edson\\Downloads\\balanca")
add_body("<b>Banco de dados:</b> db.sqlite3")
add_body("<b>Porta padrão:</b> 8000")

add_body("---")
add_body("Manual gerado em 13/04/2026")
add_body("Sistema: Controle Etanol - Django 6.0.4")

c.save()
print("Manual criado com sucesso: Manual_Installacao_Controle_Etanol.pdf")