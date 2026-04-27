# reimport_all.ps1 — Reimporta todas as tools e agentes do SynchroAI

Write-Host "[1/2] Reimportando tools..." -ForegroundColor Cyan

$tools = @(
    "buscar_voluntarios",
    "listar_necessidades",
    "criar_match",
    "pontuar_voluntario",
    "criar_voluntario"
)

foreach ($tool in $tools) {
    Write-Host "  -> $tool" -ForegroundColor Yellow
    orchestrate tools import -k python -f "../watsonx/tools/$tool.py" -r "../watsonx/tools/requirements.txt"
}

Write-Host "`n[2/2] Reimportando agentes (especialistas primeiro)..." -ForegroundColor Cyan

$agents = @(
    "perfilador",
    "pareador",
    "bem-estar",
    "pontuacao",
    "coordenador"
)

foreach ($agent in $agents) {
    Write-Host "  -> $agent" -ForegroundColor Yellow
    orchestrate agents import -f "../watsonx/agents/$agent.yaml"
}

Write-Host "`nReimportacao concluida!" -ForegroundColor Green