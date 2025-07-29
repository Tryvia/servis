# Dashboard de Tickets Freshdesk

Este projeto cria um dashboard visual para exibir tickets do Freshdesk em tempo real, com gráficos e separação por empresas e tipos.

## Funcionalidades

- **Execução automática do script PowerShell**: O dashboard executa o script `freshdesk_export_tickets_clean.ps1` para buscar os dados mais recentes
- **Visualização em tempo real**: Interface responsiva que atualiza os dados automaticamente
- **Gráficos interativos**: Visualizações por status, prioridade, empresa e tipo
- **Lista organizada**: Tickets separados por empresa com informações detalhadas
- **Atualização manual**: Botão para forçar atualização dos dados

## Estrutura do Projeto

```
freshdesk-dashboard/
├── freshdesk-api/                    # Backend Flask
│   ├── src/
│   │   ├── static/
│   │   │   └── index.html           # Interface do dashboard
│   │   ├── routes/
│   │   │   ├── tickets.py           # Endpoint para buscar tickets
│   │   │   └── user.py              # Rotas de usuário (padrão)
│   │   └── main.py                  # Aplicação Flask principal
│   ├── freshdesk_export_tickets_clean.ps1  # Script PowerShell
│   ├── venv/                        # Ambiente virtual Python
│   └── requirements.txt             # Dependências Python
└── README.md                        # Este arquivo
```

## Pré-requisitos

- **PowerShell Core 7.x** (já instalado no sistema)
- **Python 3.11+** com pip
- **Acesso à internet** para conectar com a API do Freshdesk

## Como Executar

### 1. Navegue até o diretório do projeto
```bash
cd freshdesk-dashboard/freshdesk-api
```

### 2. Ative o ambiente virtual
```bash
source venv/bin/activate
```

### 3. Execute a aplicação
```bash
python src/main.py
```

### 4. Acesse o dashboard
Abra seu navegador e vá para: `http://localhost:5001`

## Como Usar

1. **Primeira execução**: Clique no botão "🔄 Atualizar Tickets" para carregar os dados
2. **Visualização**: Os gráficos e estatísticas serão exibidos automaticamente
3. **Atualização**: O sistema atualiza automaticamente a cada 5 minutos, ou você pode forçar a atualização clicando no botão
4. **Navegação**: Role a página para ver todos os gráficos e a lista detalhada de tickets

## Gráficos Disponíveis

- **Tickets por Status**: Gráfico de rosca mostrando distribuição por status (Aberto, Pendente, Resolvido, Fechado)
- **Tickets por Prioridade**: Gráfico de barras com distribuição por prioridade (Baixa, Média, Alta, Urgente)
- **Tickets por Empresa**: Gráfico de barras horizontais com as top 10 empresas
- **Tickets por Tipo**: Gráfico de pizza com distribuição por tipo de ticket

## Informações Técnicas

### Configuração da API Freshdesk
O script PowerShell está configurado para:
- **Domínio**: suportetryvia.freshdesk.com
- **API Key**: YbOYtaCLmhZuvC9hqWUo (configurada no script)

### Dados Exibidos
Para cada ticket, o dashboard mostra:
- ID do ticket
- Assunto
- Status (com cores diferenciadas)
- Prioridade (com cores diferenciadas)
- Data de criação
- Tipo do ticket
- Empresa associada

### Tecnologias Utilizadas
- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Gráficos**: Chart.js
- **Dados**: PowerShell + API REST do Freshdesk
- **Estilo**: CSS customizado com gradientes e animações

## Solução de Problemas

### Erro "PowerShell não encontrado"
- Verifique se o PowerShell Core está instalado: `pwsh --version`
- Se necessário, instale o PowerShell Core

### Erro de conexão com Freshdesk
- Verifique se a API Key está correta no script PowerShell
- Confirme se o domínio está correto (suportetryvia)
- Teste a conectividade com a internet

### Porta em uso
- Se a porta 5001 estiver em uso, altere no arquivo `src/main.py`
- Mude a linha: `app.run(host='0.0.0.0', port=5001, debug=True)`

## Personalização

### Alterar intervalo de atualização automática
No arquivo `src/static/index.html`, altere a linha:
```javascript
setInterval(fetchTickets, 5 * 60 * 1000); // 5 minutos
```

### Modificar cores dos gráficos
As cores estão definidas no JavaScript dentro do arquivo `index.html`, nas seções de cada gráfico.

### Adicionar novos campos
Para exibir campos adicionais dos tickets, modifique:
1. O script PowerShell para incluir os campos desejados
2. O JavaScript no `index.html` para processar e exibir os novos dados

## Suporte

Para dúvidas ou problemas, verifique:
1. Os logs do Flask no terminal
2. O console do navegador (F12) para erros JavaScript
3. Se o arquivo `tickets_exportados.json` está sendo gerado corretamente

