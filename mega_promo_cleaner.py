from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk
from datetime import datetime

import ctypes
import tkinter as tk
import psutil
import os
import shutil
import subprocess
import platform
import socket
import sys


def caminho_recurso(nome_arquivo):
    try:
        pasta_base = sys._MEIPASS
    except Exception:
        pasta_base = os.path.abspath(".")

    return os.path.join(pasta_base, nome_arquivo)


# =========================
# LIMPEZA
# =========================

def limpar_temp_usuario():
    pasta = os.getenv("TEMP")

    removidos = 0

    for item in os.listdir(pasta):

        caminho = os.path.join(pasta, item)

        try:

            if os.path.isfile(caminho):

                removidos += os.path.getsize(caminho)
                os.remove(caminho)

            elif os.path.isdir(caminho):

                try:

                    for dp, dn, arquivos in os.walk(caminho):

                        for arquivo in arquivos:

                            try:
                                removidos += os.path.getsize(
                                    os.path.join(dp, arquivo)
                                )
                            except:
                                pass

                    shutil.rmtree(caminho)

                except:
                    pass

        except:
            pass

    return removidos


def limpar_windows_temp():
    pasta = r"C:\Windows\Temp"

    removidos = 0

    if not os.path.exists(pasta):
        return removidos

    for item in os.listdir(pasta):

        caminho = os.path.join(pasta, item)

        try:

            if os.path.isfile(caminho):

                removidos += os.path.getsize(caminho)
                os.remove(caminho)

            elif os.path.isdir(caminho):

                try:

                    for dp, dn, arquivos in os.walk(caminho):

                        for arquivo in arquivos:

                            try:
                                removidos += os.path.getsize(
                                    os.path.join(dp, arquivo)
                                )
                            except:
                                pass

                    shutil.rmtree(caminho)

                except:
                    pass

        except:
            pass

    return removidos


def limpar_windows_update():
    pasta = r"C:\Windows\SoftwareDistribution\Download"

    removidos = 0

    if not os.path.exists(pasta):
        return removidos

    for item in os.listdir(pasta):

        caminho = os.path.join(pasta, item)

        try:

            if os.path.isfile(caminho):

                removidos += os.path.getsize(caminho)

                os.remove(caminho)

            elif os.path.isdir(caminho):

                shutil.rmtree(caminho)

        except:
            pass

    return removidos


def limpar_prefetch():
    pasta = r"C:\Windows\Prefetch"

    removidos = 0

    if not os.path.exists(pasta):
        return removidos

    for item in os.listdir(pasta):

        caminho = os.path.join(pasta, item)

        try:

            if os.path.isfile(caminho):
                removidos += os.path.getsize(caminho)

                os.remove(caminho)

        except:
            pass

    return removidos


def esvaziar_lixeira():
    try:
        # Tentar usar o comando nativo do Windows
        resultado = subprocess.run(
            ["cmd", "/c", "rd /s /q %systemdrive%\\$Recycle.bin"],
            shell=False,
            capture_output=True,
            timeout=10
        )

        if resultado.returncode != 0:
            raise RuntimeError("O comando do Windows falhou.")

        # Recriar a pasta de lixeira
        resultado = subprocess.run(
            ["cmd", "/c", "attrib +s +h %systemdrive%\\$Recycle.bin"],
            shell=False,
            capture_output=True,
            timeout=5
        )

        if resultado.returncode != 0:
            raise RuntimeError("Não foi possível recriar a Lixeira.")

        return True

    except Exception as e:
        print(f"Erro ao esvaziar lixeira: {e}")
        try:
            # Fallback alternativo
            subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-NonInteractive",
                    "-Command",
                    "Clear-RecycleBin -Force -Confirm:$false",
                ],
                shell=False,
                capture_output=True,
                timeout=10
            )
            return True
        except:
            return False


# =========================
# FUNÇÕES DA INTERFACE
# =========================

def atualizar_info():
    ram = psutil.virtual_memory()

    total, usado, livre = shutil.disk_usage("C:")

    lbl_ram.config(
        text=f"Uso de RAM: {ram.percent}%"
    )

    lbl_disco.config(
        text=f"Espaço Livre: {livre / (1024 ** 3):.2f} GB"
    )


def limpar_temp():
    confirmado = messagebox.askyesno(
        "Confirmar limpeza",
        "Esta ação apagará arquivos temporários, o cache do Windows Update, o Prefetch e a Lixeira.\n\n"
        "Os arquivos removidos não poderão ser recuperados. Deseja continuar?",
        icon="warning",
    )

    if not confirmado:
        status.config(text="Limpeza cancelada.")
        return

    progress["value"] = 0

    status.config(
        text="Executando limpeza..."
    )

    janela.update()

    total = 0

    progress["value"] = 25
    janela.update()

    total += limpar_windows_temp()

    progress["value"] = 70
    janela.update()

    total += limpar_prefetch()

    progress["value"] = 85
    janela.update()

    total += limpar_windows_update()

    progress["value"] = 95
    janela.update()

    esvaziar_lixeira()

    progress["value"] = 100

    gb = total / (1024 ** 3)

    atualizar_info()

    messagebox.showinfo(
        "Concluído",
        f"Espaço recuperado: {gb:.2f} GB"
    )

    status.config(
        text=f"Limpeza concluída - {gb:.2f} GB recuperados"
    )


def limpar_lixeira():
    confirmado = messagebox.askyesno(
        "Confirmar limpeza da Lixeira",
        "A Lixeira será esvaziada permanentemente. Deseja continuar?",
        icon="warning",
    )

    if not confirmado:
        return

    if esvaziar_lixeira():

        messagebox.showinfo(
            "Sucesso",
            "Lixeira esvaziada."
        )

    else:

        messagebox.showerror(
            "Erro",
            "Não foi possível esvaziar a lixeira."
        )


def verificar_processos():
    janela_proc = tk.Toplevel(janela)

    janela_proc.title(
        "Top 10 Processos"
    )

    janela_proc.geometry(
        "700x500"
    )

    texto = scrolledtext.ScrolledText(
        janela_proc,
        width=80,
        height=25
    )

    texto.pack(
        padx=10,
        pady=10,
        fill="both",
        expand=True
    )

    processos = []

    for proc in psutil.process_iter(
            ['name', 'memory_info']
    ):

        try:

            memoria = (
                    proc.info['memory_info'].rss
                    / 1024 / 1024
            )

            processos.append(
                (
                    proc.info['name'],
                    memoria
                )
            )

        except:
            pass

    processos.sort(
        key=lambda x: x[1],
        reverse=True
    )

    texto.insert(
        tk.END,
        "TOP 10 PROCESSOS QUE MAIS CONSOMEM MEMÓRIA\n\n"
    )

    for nome, memoria in processos[:10]:
        texto.insert(
            tk.END,
            f"{nome} - {memoria:.2f} MB\n"
        )

    texto.config(
        state="disabled"
    )


def diagnostico_completo():
    ram = psutil.virtual_memory()

    total, usado, livre = shutil.disk_usage("C:")

    cpu = psutil.cpu_percent(
        interval=1
    )

    boot = datetime.fromtimestamp(
        psutil.boot_time()
    )

    uptime = datetime.now() - boot

    mensagem = f"""
COMPUTADOR: {socket.gethostname()}

SISTEMA:
{platform.system()} {platform.release()}

CPU:
{cpu}%

RAM:
{ram.percent}% usada

RAM LIVRE:
{ram.available / (1024 ** 3):.2f} GB

DISCO LIVRE:
{livre / (1024 ** 3):.2f} GB

TEMPO LIGADO:
{str(uptime).split('.')[0]}
"""

    messagebox.showinfo(
        "Diagnóstico Completo",
        mensagem
    )


def gerar_relatorio():
    ram = psutil.virtual_memory()

    total, usado, livre = shutil.disk_usage("C:")

    cpu = psutil.cpu_percent(
        interval=1
    )

    arquivo = (
        f"Relatorio_"
        f"{datetime.now().strftime('%d%m%Y_%H%M%S')}.txt"
    )

    desktop = os.path.join(
        os.path.expanduser("~"),
        "Desktop"
    )

    caminho = os.path.join(
        desktop,
        arquivo
    )

    with open(
            caminho,
            "w",
            encoding="utf-8"
    ) as f:
        f.write(
            f"Computador: {socket.gethostname()}\n"
        )

        f.write(
            f"Sistema: "
            f"{platform.system()} "
            f"{platform.release()}\n"
        )

        f.write(
            f"CPU: {cpu}%\n"
        )

        f.write(
            f"RAM: {ram.percent}%\n"
        )

        f.write(
            f"RAM Livre: "
            f"{ram.available / (1024 ** 3):.2f} GB\n"
        )

        f.write(
            f"Disco Livre: "
            f"{livre / (1024 ** 3):.2f} GB\n"
        )

        f.write(
            f"Data: "
            f"{datetime.now()}\n"
        )

    messagebox.showinfo(
        "Relatório",
        f"Relatório salvo em:\n\n{caminho}"
    )


# =========================
# JANELA - INTERFACE MODERNA
# =========================

janela = tk.Tk()

janela.title("Mega Cleaner")
janela.geometry("520x750")
janela.resizable(False, False)

try:
    janela.iconbitmap(caminho_recurso("icon.ico"))
except Exception:
    pass

# Variaveis de cores
COR_FUNDO = "#F8FAFC"
COR_PRIMARIA = "#F97316"
COR_PRIMARIA_ESCURO = "#EA580C"
COR_PRIMARIA_CLARO = "#FB923C"
COR_SECUNDARIA = "#EC4899"
COR_SUCESSO = "#10B981"
COR_TEXTO = "#1E293B"
COR_TEXTO_MUTED = "#64748B"
COR_CARD = "#FFFFFF"
COR_BORDA = "#E2E8F0"

janela.configure(bg=COR_FUNDO)

# Barra de progresso
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Moderno.Horizontal.TProgressbar",
    troughcolor=COR_BORDA,
    background=COR_PRIMARIA,
    bordercolor=COR_BORDA,
    lightcolor=COR_PRIMARIA,
    darkcolor=COR_PRIMARIA_ESCURO,
    thickness=14
)

# Container principal
main_container = tk.Frame(janela, bg=COR_FUNDO)
main_container.pack(fill="both", expand=True, padx=0, pady=0)

# ===== HEADER =====
header_frame = tk.Frame(main_container, bg=COR_PRIMARIA, height=160)
header_frame.pack(fill="x")
header_frame.pack_propagate(False)

# Logo e Título no Header
header_content = tk.Frame(header_frame, bg=COR_PRIMARIA)
header_content.pack(fill="both", expand=True, padx=24, pady=20)

# Logo
logo_img = Image.open(caminho_recurso("logo.png"))
logo_img = logo_img.resize((100, 100))
logo_tk = ImageTk.PhotoImage(logo_img)

logo_label = tk.Label(header_content, image=logo_tk, bg=COR_PRIMARIA)
logo_label.pack(side="left", padx=(0, 20))

# Textos do header
header_text = tk.Frame(header_content, bg=COR_PRIMARIA)
header_text.pack(side="left", fill="both", expand=True)

titulo = tk.Label(
    header_text,
    text="MEGA CLEANER",
    font=("Segoe UI", 30, "bold"),
    bg=COR_PRIMARIA,
    fg="white"
)
titulo.pack(anchor="w")

subtitulo = tk.Label(
    header_text,
    text="LIMPEZA DE ARQUIVOS",
    font=("Segoe UI", 15, "bold"),
    bg=COR_PRIMARIA,
    fg="white"
)
subtitulo.pack(anchor="w", pady=(0, 0))

desc = tk.Label(
    header_text,
    text="Limpeza e diagnóstico do computador",
    font=("Segoe UI", 13),
    bg=COR_PRIMARIA,
    fg="white"
)
desc.pack(anchor="w")

# ===== CONTEÚDO PRINCIPAL =====
content_container = tk.Frame(main_container, bg=COR_FUNDO)
content_container.pack(fill="both", expand=True, padx=20, pady=20)

# Card de Status
status_card = tk.Frame(
    content_container,
    bg=COR_CARD,
    highlightbackground=COR_BORDA,
    highlightthickness=1
)
status_card.pack(fill="x", pady=(0, 20))

status_titulo = tk.Label(
    status_card,
    text="📊 Status do Sistema",
    bg=COR_CARD,
    fg=COR_TEXTO,
    font=("Segoe UI", 11, "bold"),
    padx=20,
    pady=12
)
status_titulo.pack(anchor="w")

status_content = tk.Frame(status_card, bg=COR_CARD)
status_content.pack(fill="x", padx=16, pady=(0, 16))

lbl_ram = tk.Label(
    status_content,
    text="",
    bg="#F1F5F9",
    fg=COR_TEXTO,
    font=("Segoe UI", 10, "bold"),
    padx=12,
    pady=10,
    anchor="w",
    justify="left"
)
lbl_ram.pack(fill="x", pady=(0, 8))

lbl_disco = tk.Label(
    status_content,
    text="",
    bg="#F9F4F1",
    fg=COR_TEXTO,
    font=("Segoe UI", 10, "bold"),
    padx=12,
    pady=10,
    anchor="w",
    justify="left"
)
lbl_disco.pack(fill="x")

# Card de Ações
acoes_card = tk.Frame(
    content_container,
    bg=COR_CARD,
    highlightbackground=COR_BORDA,
    highlightthickness=1
)
acoes_card.pack(fill="x", pady=(0, 20))

acoes_titulo = tk.Label(
    acoes_card,
    text="⚙️ Ações Disponíveis",
    bg=COR_CARD,
    fg=COR_TEXTO,
    font=("Segoe UI", 11, "bold"),
    padx=16,
    pady=12
)
acoes_titulo.pack(anchor="w")

botoes_container = tk.Frame(acoes_card, bg=COR_CARD)
botoes_container.pack(fill="x", padx=16, pady=(0, 16))


def criar_botao_moderno(parent, texto, comando, emoji=""):
    """Cria um botão moderno com estilo"""
    cor_bg = "#FFEDD5"
    cor_fg = COR_PRIMARIA
    cor_hover = "#FED7AA"

    botao = tk.Button(
        parent,
        text=f"{emoji} {texto}".strip(),
        command=comando,
        bg=cor_bg,
        fg=cor_fg,
        font=("Segoe UI", 9, "bold"),
        activebackground=cor_hover,
        activeforeground=COR_PRIMARIA,
        cursor="hand2",
        relief="flat",
        bd=0,
        padx=12,
        pady=10,
        highlightthickness=0
    )

    def on_enter(e):
        botao.config(bg=cor_hover, fg=COR_PRIMARIA)

    def on_leave(e):
        botao.config(bg=cor_bg, fg=cor_fg)

    botao.bind("<Enter>", on_enter)
    botao.bind("<Leave>", on_leave)

    botao.pack(fill="x", pady=5)
    return botao


criar_botao_moderno(botoes_container, "Limpar Temporários", limpar_temp, "🧹")
criar_botao_moderno(botoes_container, "Esvaziar Lixeira", limpar_lixeira, "🗑️")
criar_botao_moderno(botoes_container, "Verificar Processos", verificar_processos, "⚡")
criar_botao_moderno(botoes_container, "Diagnóstico Completo", diagnostico_completo, "🔍")
criar_botao_moderno(botoes_container, "Gerar Relatório", gerar_relatorio, "📄")

# Barra de progresso
progress = ttk.Progressbar(
    content_container,
    style="Moderno.Horizontal.TProgressbar",
    mode="determinate"
)
progress.pack(fill="x", pady=(0, 12))

# Status
status = tk.Label(
    content_container,
    text="✨ Aguardando ação...",
    bg=COR_FUNDO,
    fg=COR_TEXTO_MUTED,
    font=("Segoe UI", 9, "bold")
)
status.pack()

atualizar_info()

janela.mainloop()