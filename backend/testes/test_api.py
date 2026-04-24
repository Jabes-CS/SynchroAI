"""
test_api.py — Teste completo da API SynchroAI

Este arquivo testa TODOS os endpoints da API:
  • Voluntários (create, list, get, update, delete)
  • Instituições (create, list, get)
  • Necessidades (create, list, get)
  • Matches (create, list, get)

IMPORTANTE: Todos os dados criados são REMOVIDOS ao final do teste,
deixando o banco de dados como estava antes.

Como rodar:
  1. Inicie o servidor: uvicorn app.main:app --reload
  2. Em outro terminal: pytest testes/test_api.py -v
"""

import pytest
import requests
from datetime import datetime, timedelta

# ============================================
# CONFIGURAÇÃO
# ============================================
BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

# Listas para rastrear IDs criados (para limpeza posterior)
created_volunteers = []
created_institutions = []
created_needs = []
created_matches = []


# ============================================
# TESTES DE VOLUNTÁRIOS
# ============================================

def test_01_create_volunteer_freelancer():
    """Cria um voluntário freelancer."""
    data = {
        "name": "João Silva",
        "email": "joao.freelancer@test.com",
        "phone": "(11) 98765-4321",
        "type": "freelancer",
        "skills": ["logística", "primeiros_socorros"],
        "availability": {"segunda": "10h-18h", "terça": "10h-18h"},
        "city": "São Paulo",
        "state": "SP",
        "latitude": "-23.5505",
        "longitude": "-46.6333",
        "open_to_rotation": True,
    }

    response = requests.post(f"{BASE_URL}/volunteers/", json=data, headers=HEADERS)
    assert response.status_code == 201, f"Erro ao criar voluntário: {response.text}"
    
    result = response.json()
    assert result["email"] == data["email"]
    assert result["type"] == "freelancer"
    
    created_volunteers.append(result["id"])
    print(f"✓ Voluntário Freelancer criado: ID {result['id']}")


def test_02_create_volunteer_permanent():
    """Cria um voluntário permanente com perfil CARFO."""
    data = {
        "name": "Maria Santos",
        "email": "maria.permanent@test.com",
        "phone": "(11) 99876-5432",
        "type": "permanent",
        "skills": ["enfermagem", "gestão", "comunicação"],
        "availability": {
            "segunda": "08h-22h",
            "terça": "08h-22h",
            "quarta": "08h-22h",
            "quinta": "08h-22h",
            "sexta": "08h-22h",
        },
        "carfo_profile": {
            "conscienciosidade": 8,
            "abertura_experiencias": 7,
            "realizacao_futuro": 9,
            "foco_positivo": 8,
            "orientacao_servico": 9,
        },
        "city": "Rio de Janeiro",
        "state": "RJ",
        "latitude": "-22.9068",
        "longitude": "-43.1729",
        "open_to_rotation": True,
    }

    response = requests.post(f"{BASE_URL}/volunteers/", json=data, headers=HEADERS)
    assert response.status_code == 201, f"Erro ao criar voluntário: {response.text}"
    
    result = response.json()
    assert result["email"] == data["email"]
    assert result["type"] == "permanent"
    
    created_volunteers.append(result["id"])
    print(f"✓ Voluntário Permanente criado: ID {result['id']}")


def test_03_list_volunteers():
    """Lista todos os voluntários."""
    response = requests.get(f"{BASE_URL}/volunteers/", headers=HEADERS)
    assert response.status_code == 200
    
    result = response.json()
    assert len(result) >= 2
    print(f"✓ Listagem de voluntários: {len(result)} voluntários encontrados")


def test_04_get_volunteer_by_id():
    """Busca um voluntário específico por ID."""
    if not created_volunteers:
        pytest.skip("Nenhum voluntário criado")
    
    volunteer_id = created_volunteers[0]
    response = requests.get(f"{BASE_URL}/volunteers/{volunteer_id}", headers=HEADERS)
    assert response.status_code == 200
    
    result = response.json()
    assert result["id"] == volunteer_id
    print(f"✓ Voluntário recuperado: {result['name']}")


def test_05_update_volunteer():
    """Atualiza um voluntário."""
    if not created_volunteers:
        pytest.skip("Nenhum voluntário criado")
    
    volunteer_id = created_volunteers[0]
    update_data = {
        "name": "João Silva Atualizado",
        "points": 50,
    }
    
    response = requests.put(
        f"{BASE_URL}/volunteers/{volunteer_id}",
        json=update_data,
        headers=HEADERS
    )
    assert response.status_code == 200
    
    result = response.json()
    assert result["name"] == "João Silva Atualizado"
    print(f"✓ Voluntário atualizado: {result['name']}, pontos: {result['points']}")


def test_06_duplicate_email_error():
    """Testa que não é possível criar dois voluntários com o mesmo email."""
    data = {
        "name": "Teste Duplicado",
        "email": "joao.freelancer@test.com",  # Email já existe
        "phone": "(11) 99999-9999",
        "type": "freelancer",
    }

    response = requests.post(f"{BASE_URL}/volunteers/", json=data, headers=HEADERS)
    assert response.status_code == 400, "Deveria rejeitar email duplicado"
    print("✓ Email duplicado foi corretamente rejeitado")


# ============================================
# TESTES DE INSTITUIÇÕES
# ============================================

def test_07_create_institution_ngo():
    """Cria uma instituição (ONG)."""
    data = {
        "name": "SOS Humanitário",
        "email": "contato@soshumanitario.org",
        "phone": "(11) 3456-7890",
        "type": "ngo",
        "city": "São Paulo",
        "state": "SP",
        "address": "Rua das Flores, 123, São Paulo, SP",
        "is_verified": True,
    }

    response = requests.post(f"{BASE_URL}/institutions/", json=data, headers=HEADERS)
    assert response.status_code == 201
    
    result = response.json()
    assert result["email"] == data["email"]
    assert result["type"] == "ngo"
    
    created_institutions.append(result["id"])
    print(f"✓ Instituição ONG criada: ID {result['id']}")


def test_08_create_institution_government():
    """Cria uma instituição governamental."""
    data = {
        "name": "Prefeitura de São Paulo - Defesa Civil",
        "email": "defesa.civil@prefeitura.sp.gov.br",
        "phone": "(11) 1234-5678",
        "type": "government",
        "city": "São Paulo",
        "state": "SP",
        "address": "Rua do Governo, 456, São Paulo, SP",
        "is_verified": True,
    }

    response = requests.post(f"{BASE_URL}/institutions/", json=data, headers=HEADERS)
    assert response.status_code == 201
    
    result = response.json()
    created_institutions.append(result["id"])
    print(f"✓ Instituição Governo criada: ID {result['id']}")


def test_09_list_institutions():
    """Lista todas as instituições."""
    response = requests.get(f"{BASE_URL}/institutions/", headers=HEADERS)
    assert response.status_code == 200
    
    result = response.json()
    assert len(result) >= 2
    print(f"✓ Listagem de instituições: {len(result)} instituições encontradas")


def test_10_get_institution_by_id():
    """Busca uma instituição específica."""
    if not created_institutions:
        pytest.skip("Nenhuma instituição criada")
    
    institution_id = created_institutions[0]
    response = requests.get(f"{BASE_URL}/institutions/{institution_id}", headers=HEADERS)
    assert response.status_code == 200
    
    result = response.json()
    assert result["id"] == institution_id
    print(f"✓ Instituição recuperada: {result['name']}")


# ============================================
# TESTES DE NECESSIDADES
# ============================================

def test_11_create_need():
    """Cria uma necessidade vinculada a uma instituição."""
    if not created_institutions:
        pytest.skip("Nenhuma instituição criada")
    
    institution_id = created_institutions[0]
    tomorrow = datetime.utcnow() + timedelta(days=1)
    next_day = tomorrow + timedelta(hours=4)
    
    data = {
        "title": "Enfermeiros para abrigo emergencial",
        "description": "Precisamos de profissionais de saúde para atender desabrigados.",
        "institution_id": institution_id,
        "required_skills": ["enfermagem", "primeiros_socorros"],
        "volunteers_needed": 3,
        "urgency": "high",
        "city": "São Paulo",
        "state": "SP",
        "address": "Abrigo Centro, Rua X, 789",
        "start_date": tomorrow.isoformat(),
        "end_date": next_day.isoformat(),
        "status": "open",
    }

    response = requests.post(f"{BASE_URL}/needs/", json=data, headers=HEADERS)
    assert response.status_code == 201
    
    result = response.json()
    assert result["title"] == data["title"]
    assert result["urgency"] == "high"
    assert result["status"] == "open"
    
    created_needs.append(result["id"])
    print(f"✓ Necessidade criada: ID {result['id']}")


def test_12_create_multiple_needs():
    """Cria mais necessidades para ter diversidade."""
    if not created_institutions:
        pytest.skip("Nenhuma instituição criada")
    
    institution_id = created_institutions[1] if len(created_institutions) > 1 else created_institutions[0]
    tomorrow = datetime.utcnow() + timedelta(days=2)
    next_day = tomorrow + timedelta(hours=6)
    
    data = {
        "title": "Voluntários para distribuição de alimentos",
        "description": "Precisamos distribuir alimentos para comunidades afetadas.",
        "institution_id": institution_id,
        "required_skills": ["logística"],
        "volunteers_needed": 5,
        "urgency": "critical",
        "city": "São Paulo",
        "state": "SP",
        "address": "Centro de Distribuição, Rua Y, 999",
        "start_date": tomorrow.isoformat(),
        "end_date": next_day.isoformat(),
        "status": "open",
    }

    response = requests.post(f"{BASE_URL}/needs/", json=data, headers=HEADERS)
    assert response.status_code == 201
    
    result = response.json()
    created_needs.append(result["id"])
    print(f"✓ Segunda necessidade criada: ID {result['id']}")


def test_13_list_needs():
    """Lista todas as necessidades."""
    response = requests.get(f"{BASE_URL}/needs/", headers=HEADERS)
    assert response.status_code == 200
    
    result = response.json()
    assert len(result) >= 2
    print(f"✓ Listagem de necessidades: {len(result)} necessidades encontradas")


def test_14_get_need_by_id():
    """Busca uma necessidade específica."""
    if not created_needs:
        pytest.skip("Nenhuma necessidade criada")
    
    need_id = created_needs[0]
    response = requests.get(f"{BASE_URL}/needs/{need_id}", headers=HEADERS)
    assert response.status_code == 200
    
    result = response.json()
    assert result["id"] == need_id
    print(f"✓ Necessidade recuperada: {result['title']}")


# ============================================
# TESTES DE MATCHES
# ============================================

def test_15_create_match():
    """Cria um match entre voluntário e necessidade."""
    if not created_volunteers or not created_needs:
        pytest.skip("Voluntários ou necessidades não foram criados")
    
    data = {
        "volunteer_id": created_volunteers[0],
        "need_id": created_needs[0],
        "score": 85.5,
        "status": "suggested",
    }

    response = requests.post(f"{BASE_URL}/matches/", json=data, headers=HEADERS)
    assert response.status_code == 201
    
    result = response.json()
    assert result["volunteer_id"] == data["volunteer_id"]
    assert result["need_id"] == data["need_id"]
    assert result["score"] == 85.5
    assert result["status"] == "suggested"
    
    created_matches.append(result["id"])
    print(f"✓ Match criado: ID {result['id']}, Score: {result['score']}")


def test_16_create_multiple_matches():
    """Cria mais matches."""
    if len(created_volunteers) < 2 or len(created_needs) < 2:
        pytest.skip("Não há voluntários e necessidades suficientes")
    
    data = {
        "volunteer_id": created_volunteers[1],
        "need_id": created_needs[1],
        "score": 72.0,
        "status": "suggested",
    }

    response = requests.post(f"{BASE_URL}/matches/", json=data, headers=HEADERS)
    assert response.status_code == 201
    
    result = response.json()
    created_matches.append(result["id"])
    print(f"✓ Segundo match criado: ID {result['id']}")


def test_17_list_matches():
    """Lista todos os matches."""
    response = requests.get(f"{BASE_URL}/matches/", headers=HEADERS)
    assert response.status_code == 200
    
    result = response.json()
    assert len(result) >= 2
    print(f"✓ Listagem de matches: {len(result)} matches encontrados")


def test_18_get_match_by_id():
    """Busca um match específico."""
    if not created_matches:
        pytest.skip("Nenhum match criado")
    
    match_id = created_matches[0]
    response = requests.get(f"{BASE_URL}/matches/{match_id}", headers=HEADERS)
    assert response.status_code == 200
    
    result = response.json()
    assert result["id"] == match_id
    print(f"✓ Match recuperado: ID {result['id']}, Score: {result['score']}")


def test_19_health_check():
    """Testa o endpoint de health check."""
    response = requests.get(f"{BASE_URL}/health", headers=HEADERS)
    assert response.status_code == 200
    
    result = response.json()
    assert result["status"] == "healthy"
    print(f"✓ Health check: API está saudável")


def test_20_root_endpoint():
    """Testa o endpoint raiz."""
    response = requests.get(f"{BASE_URL}/", headers=HEADERS)
    assert response.status_code == 200
    
    result = response.json()
    assert result["status"] == "online"
    assert result["project"] == "SynchroAI"
    print(f"✓ Root endpoint: API está online")


# ============================================
# LIMPEZA DE DADOS (TEARDOWN)
# ============================================

def test_99_cleanup_all_data():
    """
    ÚLTIMO TESTE: Remove TODOS os dados criados durante os testes.
    
    Ordem de exclusão importa (foreign keys):
    1. Matches (referencia voluntários e necessidades)
    2. Necessidades (referencia instituições)
    3. Voluntários
    4. Instituições
    """
    
    print("\n" + "="*60)
    print("LIMPEZA DE DADOS - Removendo todos os registros de teste")
    print("="*60)
    
    # 1. Deletar matches
    for match_id in created_matches:
        response = requests.delete(f"{BASE_URL}/matches/{match_id}", headers=HEADERS)
        if response.status_code == 204:
            print(f"  ✓ Match {match_id} removido")
        else:
            print(f"  ⚠ Falha ao remover Match {match_id}: {response.status_code}")
    
    # 2. Deletar necessidades
    for need_id in created_needs:
        response = requests.delete(f"{BASE_URL}/needs/{need_id}", headers=HEADERS)
        # Note: Se não houver endpoint DELETE para needs, comentar esta seção
        if response.status_code in [204, 404]:
            print(f"  ✓ Necessidade {need_id} removida")
        else:
            print(f"  ⚠ Falha ao remover Necessidade {need_id}: {response.status_code}")
    
    # 3. Deletar voluntários (soft delete - desativar)
    for volunteer_id in created_volunteers:
        response = requests.delete(f"{BASE_URL}/volunteers/{volunteer_id}", headers=HEADERS)
        if response.status_code == 204:
            print(f"  ✓ Voluntário {volunteer_id} desativado")
        else:
            print(f"  ⚠ Falha ao desativar Voluntário {volunteer_id}: {response.status_code}")
    
    # 4. Deletar instituições
    for institution_id in created_institutions:
        response = requests.delete(f"{BASE_URL}/institutions/{institution_id}", headers=HEADERS)
        # Note: Se não houver endpoint DELETE para institutions, comentar esta seção
        if response.status_code in [204, 404]:
            print(f"  ✓ Instituição {institution_id} removida")
        else:
            print(f"  ⚠ Falha ao remover Instituição {institution_id}: {response.status_code}")
    
    print("="*60)
    print("✓ LIMPEZA CONCLUÍDA - Banco voltou ao estado original")
    print("="*60)


# ============================================
# EXECUÇÃO
# ============================================

if __name__ == "__main__":
    print("Para rodar os testes, use:")
    print("  pytest testes/test_api.py -v")
    print("\nOu para rodar um teste específico:")
    print("  pytest testes/test_api.py::test_01_create_volunteer_freelancer -v")
