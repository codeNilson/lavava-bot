# Valorant Amateur League Bot - Bot do Discord para o Campeonato

Este repositório contém o código-fonte do bot do Discord integrado ao site do campeonato **[Valorant Amateur League](https://github.com/AroMight/valorant-amateur-league)**. O bot foi desenvolvido para automatizar e facilitar a administração do torneio de Valorant, oferecendo funcionalidades interativas para os jogadores e organizadores diretamente no Discord.

## Funcionalidades Principais

- **Sorteio e Gerenciamento de Times**  
  - Sorteia dois líderes antes de cada partida.  
  - Permite que os líderes escolham os jogadores em tempo real no Discord.  

- **Sincronização com o Site do Campeonato**  
  - Utiliza a API do site para criar times e partidas a partir das escolhas de jogadores feitas pelos líderes.  

- **Comandos Personalizados**  
  - Criação de times e associação com partidas.  
  - Exibição classificações diretamente no Discord.  
  - Integração com a API para realizar validações.

- **Moderação e Administração**  
  - Facilita a gestão dos jogadores e equipes. 


## Tecnologias Utilizadas

- **Linguagem:** Python com a biblioteca `discord.py`.  
- **API:** Integração com a API RESTful do site principal.  
- **Gerenciamento de Configurações:** Arquivo `.env` para variáveis de ambiente.  

## Requisitos

- Python 3.9 ou superior.  
- Token de bot do Discord configurado no arquivo `.env`.  
- API do site configurada e acessível.  

## Rodando Localmente

1. Clone o projeto

```bash
git clone https://github.com/AroMight/valorant-bot.git
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # No Windows, use venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:

```bash
- Crie um arquivo `.env` e preencha com as informações do .env-example
```

5. Inicie o bot:

```bash
python main.py
```

## Integração com o Site Principal

Este bot está integrado ao site do campeonato **[Valorant Amateur League](https://github.com/AroMight/valorant-amateur-league)** para sincronizar informações em tempo real. Confira o repositório principal para mais detalhes sobre o funcionamento completo da plataforma.

---
