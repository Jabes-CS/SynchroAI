# 🧪 Guia de Testes - SynchroAI Backend

Este arquivo documenta como testar a API SynchroAI de forma completa e segura.

## 📋 O que o arquivo de testes faz

O arquivo `test_api.py` testa **TODOS os endpoints** da API:

✅ **Voluntários**
- Criar voluntário freelancer
- Criar voluntário permanente (com perfil CARFO)
- Listar voluntários
- Buscar voluntário por ID
- Atualizar voluntário
- Validar email duplicado

✅ **Instituições**
- Criar instituição (ONG)
- Criar instituição governamental
- Listar instituições
- Buscar instituição por ID

✅ **Necessidades**
- Criar necessidade vinculada a instituição
- Listar necessidades
- Buscar necessidade por ID

✅ **Matches**
- Criar match entre voluntário e necessidade
- Listar matches
- Buscar match por ID

✅ **Health Checks**
- Testar endpoint de saúde
- Testar endpoint raiz

## 🔄 Limpeza automática de dados

**IMPORTANTE:** Todos os dados criados durante os testes são **automaticamente removidos** ao final, deixando o banco de dados como estava antes. Isso garante que você possa rodar os testes múltiplas vezes sem poluir o banco.

## 🚀 Como usar

### 1. Instale as dependências de teste

```powershell
pip install -r testes/requirements-dev.txt
```

### 2. Inicie o servidor (em um terminal)

```powershell
uvicorn app.main:app --reload
```

Você deve ver:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 3. Rode os testes (em outro terminal)

Na pasta `backend/`:

```powershell
# Rodar TODOS os testes
pytest testes/test_api.py -v

# Rodar testes com mais detalhes
pytest testes/test_api.py -v -s

# Rodar um teste específico
pytest testes/test_api.py::test_01_create_volunteer_freelancer -v

# Rodar e exibir prints
pytest testes/test_api.py -v --capture=no
```

## 📊 Exemplo de saída

```
testes/test_api.py::test_01_create_volunteer_freelancer PASSED       [ 5%]
✓ Voluntário Freelancer criado: ID 1

testes/test_api.py::test_02_create_volunteer_permanent PASSED        [10%]
✓ Voluntário Permanente criado: ID 2

testes/test_api.py::test_03_list_volunteers PASSED                   [15%]
✓ Listagem de voluntários: 2 voluntários encontrados

...

testes/test_api.py::test_99_cleanup_all_data PASSED                  [100%]
============================================================
LIMPEZA DE DADOS - Removendo todos os registros de teste
============================================================
  ✓ Match 1 removido
  ✓ Voluntário 1 desativado
  ✓ Voluntário 2 desativado
  ✓ Instituição 1 removida
  ✓ Instituição 2 removida
============================================================
✓ LIMPEZA CONCLUÍDA - Banco voltou ao estado original
============================================================
```

## 🛠️ Opções úteis do pytest

```powershell
# Mostrar prints durante execução
pytest testes/test_api.py -v -s

# Parar no primeiro erro
pytest testes/test_api.py -x

# Mostrar os 3 testes mais lentos
pytest testes/test_api.py --durations=3

# Gerar relatório HTML
pytest testes/test_api.py --html=report.html --self-contained-html

# Rodar com mais verbosidade
pytest testes/test_api.py -vv
```

## ⚠️ Possíveis problemas

### Erro: "Connection refused"
**Solução:** Certifique-se de que o servidor está rodando:
```powershell
uvicorn app.main:app --reload
```

### Erro: "DATABASE_URL não encontrada"
**Solução:** Verifique se o arquivo `.env` está configurado corretamente na pasta `backend/`.

### Erro: "Module 'pytest' not found"
**Solução:** Instale as dependências de desenvolvimento:
```powershell
pip install -r testes/requirements-dev.txt
```

## 📝 Estrutura do teste

O arquivo segue a ordem:

1. **Setup** (testes 01-06): Criar voluntários
2. **Setup** (testes 07-10): Criar instituições
3. **Setup** (testes 11-14): Criar necessidades
4. **Setup** (testes 15-18): Criar matches
5. **Health** (testes 19-20): Testar endpoints especiais
6. **Teardown** (teste 99): Limpar TODOS os dados

## 🔐 Segurança

- Os testes usam **dados fictícios** que não afetam dados reais
- **Todos os dados são removidos** ao final
- O teste pode ser rodado **múltiplas vezes** sem risco
- Use em **desenvolvimento** e **testes**, não em produção

## 📚 Próximos passos

Depois de confirmar que todos os testes passam, você pode:

1. **Acessar o Swagger** em `http://localhost:8000/docs`
2. **Testar manualmente** endpoints específicos
3. **Adicionar mais testes** para casos de erro
4. **Integrar com CI/CD** (GitHub Actions, etc.)

## ✅ Checklist

- [ ] Instalar dependências: `pip install -r testes/requirements-dev.txt`
- [ ] Criar banco de dados em PostgreSQL
- [ ] Atualizar `.env` com `DATABASE_URL`
- [ ] Rodar `python create_tables.py`
- [ ] Iniciar servidor: `uvicorn app.main:app --reload`
- [ ] Rodar testes: `pytest testes/test_api.py -v`
- [ ] Verificar saída: todos os testes PASSED
- [ ] Confirmar limpeza de dados

---

**Dúvidas?** Consulte os comentários no arquivo `test_api.py` ou a documentação do [pytest](https://docs.pytest.org/).
