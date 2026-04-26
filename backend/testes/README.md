# Pasta de Testes do SynchroAI Backend

Esta pasta contém todos os testes automatizados para a API SynchroAI.

## 📁 Estrutura

- `test_api.py` - Arquivo principal com 20 testes
- `requirements-dev.txt` - Dependências para rodar os testes
- `TESTES.md` - Documentação completa

## 🚀 Quick Start

```powershell
# 1. Instalar dependências
pip install -r requirements-dev.txt

# 2. Rodar servidor (em outro terminal)
uvicorn app.main:app --reload

# 3. Rodar testes
pytest test_api.py -v
```

## ✨ Característica Principal

✅ **Auto-cleanup**: Todos os dados criados durante os testes são removidos ao final!

Veja `TESTES.md` para detalhes completos.
