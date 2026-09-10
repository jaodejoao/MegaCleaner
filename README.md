# 🧹 MegaCleaner

Aplicativo desenvolvido em Python para realizar limpeza e diagnóstico do Windows de forma simples e rápida.

> **Atenção:** este aplicativo apaga permanentemente arquivos temporários, o cache do Windows Update, arquivos do Prefetch e o conteúdo da Lixeira. Confirme os arquivos antes de executar a limpeza e use-o apenas em computadores sob sua responsabilidade.

O MegaCleaner é destinado ao Windows. Algumas ações podem exigir execução com privilégios de administrador.

## Funcionalidades

- Limpeza de arquivos temporários
- Limpeza da pasta Windows Temp
- Limpeza do cache do Windows Update
- Limpeza da pasta Prefetch
- Esvaziamento da Lixeira
- Monitoramento de uso da memória RAM
- Verificação do espaço livre em disco
- Diagnóstico completo do computador
- Exibição dos processos que mais consomem memória
- Geração de relatório do sistema

## Tecnologias

- Python
- Tkinter
- Pillow
- Psutil

## Como executar

Instale as dependências:

```bash
pip install -r requirements.txt
```

Depois execute:

```bash
python mega_promo_cleaner.py
```

## Licença

Projeto desenvolvido para estudos e uso interno. Nenhuma licença de reutilização foi definida atualmente.