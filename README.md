# PNBoia API

## Short English Description - PNBoia API

The PNBoia API serves as a platform for accessing buoy data collected by the National Buoy Program (PNBoia) of the Brazilian Navy Hydrographic Center. Currently for internal use only.

---

## Sobre a PNBoia API

A PNBoia API é uma plataforma desenvolvida para disponibilizar dados meteorológicos e oceanográficos coletados pelo Programa Nacional de Boias (PNBoia) do Centro de Hidrografia da Marinha do Brasil (CHM).

### Objetivo

Esta API tem como objetivo principal fornecer acesso padronizado e seguro aos dados coletados pelas boias meteoceanográficas, facilitando a integração com outros sistemas e aplicações.

### Funcionalidades Principais

- Acesso a dados em tempo real e históricos de boias fundeadas
- Dados meteorológicos (direção e velocidade do vento, temperatura do ar, pressão atmosférica, etc.)
- Dados oceanográficos (altura e direção de ondas, temperatura da superfície do mar, correntes marinhas, etc.)
- Suporte a diferentes formatos de resposta (JSON, CSV, etc.)
- Autenticação via token de acesso

### Estrutura do Projeto

- `pnboia_api/` - Código-fonte principal da aplicação
  - `app/` - Endpoints da API
  - `crud/` - Operações de banco de dados
  - `models/` - Modelos de dados
  - `schemas/` - Esquemas de validação
  - `db/` - Configurações do banco de dados

### Requisitos

- Python 3.8+
- PostgreSQL
- Bibliotecas listadas em `requirements.txt`

### Instalação

1. Clone o repositório
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente virtual:
   - Windows: `.\venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Instale as dependências: `pip install -r requirements.txt`
5. Configure as variáveis de ambiente no arquivo `.env`
6. Execute a aplicação: `uvicorn pnboia_api.app.main:app --reload`

---
