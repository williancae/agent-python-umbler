#!/usr/bin/env bash
# export.sh
# Script completo para gerar arquivos de conteúdo e estrutura do projeto

set -euo pipefail

echo "🚀 Iniciando exportação dos arquivos do projeto..."

# Parte 1: Exportar arquivos TS de apps/
OUTPUT="app.txt"
: > "$OUTPUT"

find app \
  \( -path '*/.venv/*' -o -path '*/__pycache__/*' \) -prune -o \
 -type f -name '*.py' -print0 | while IFS= read -r -d '' FILE; do
  {
    echo "======== $FILE ========="
    cat "$FILE"
    echo "\n"
  } >> "$OUTPUT"
done
echo "\n✅ $OUTPUT"


# Parte 4: Gerar a estrutura de diretórios
OUTPUT="struct.txt"

# Verifica se o comando tree está instalado
if ! command -v tree &> /dev/null; then
    echo "⚠️ Comando 'tree' não encontrado. Instalando..."

    # Detecta o sistema operacional e instala o tree
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update && sudo apt-get install -y tree
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install tree
    else
        echo "❌ Sistema operacional não suportado para instalação automática. Por favor, instale o comando 'tree' manualmente."
        exit 1
    fi
fi

# Executa o comando tree para gerar a estrutura
tree . -I "node_modules|dist|.venv|__pycache__" > "$OUTPUT"
echo "\n✅ $OUTPUT \n"

echo "🎉 Exportação concluída! Todos os arquivos foram gerados com sucesso."
