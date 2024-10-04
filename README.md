# Sistema de Gerenciamento de Filmes e Gêneros

Este projeto Django implementa um sistema para gerenciar filmes e gêneros, incluindo funcionalidade de soft delete, rastreamento de tempo (campos created_at, updated_at), e integração assíncrona com API para enriquecimento dos dados dos filmes.

## Funcionalidades

- **Soft Delete**: Em vez de excluir permanentemente os registros, eles são marcados como excluídos e podem ser restaurados.
- **Timestamps**: Rastreamento dos campos created_at e updated_at para todos os registros de filmes e gêneros.
- **Integração Assíncrona com API**: Enriquecimento dos dados de filmes com informações de uma API externa (The Movie Database - TMDb)..
- **Relacionamento Many-to-Many**: Filmes podem ter vários gêneros e gêneros podem ser compartilhados por vários filmes.

## Modelos

### 1. `Movie`

- `id_the_movie`: Inteiro (ID do filme da TMDb)
- `title`: String (Título do filme)
- `release_date`: Data (Data de lançamento)
- `overview`: Texto (Sinopse do filme)
- `popularity`: Float (Popularidade do filme)
- `vote_average`: Float (Média de votos)
- `vote_count`: Inteiro (Número de votos)
- `poster_path`: String (URL do pôster do filme)
- **Relações**: Many-to-Many com `Genre`
- **Soft delete**: Implementado através do campo booleano `is_deleted`

### 2. `Genre`

- `name`: String (Nome do gênero)
- **Soft delete**: Implementado através do campo booleano `is_deleted`

## Configuração

### Pré-requisitos

- Python 3.x
- Django 3.x
- PostgreSQL (ou SQLite para desenvolvimento)

### Instalação

1. Clone o repositório:
   // TODO: Adicionar o link do repositório

   ```bash
   git clone https://github.com/your-repo.git
   cd your-repo
   ```

2. Instale as dependências:
   ```bash
    pip install -r requirements.txt
   ```
3. Crie o banco de dados e execute as migrações:
   ```bash
    python manage.py makemigrations
    python manage.py migrate
   ```
4. Crie um superusuário:

   ```bash
    python manage.py createsuperuser
   ```

5. Execute o servidor de desenvolvimento:
   ```bash
    python manage.py runserver
   ```

### Executando os Testes

1. Para executar os testes, use o seguinte comando:
   ```bash
   python manage.py test
   ```

## Funcionalidade de Soft Delete

- Excluir: Quando você chama `delete()` em um `Movie` ou `Genre`, o objeto não será removido do banco de dados. Em vez disso, ele será marcado como `is_deleted=True`.

- Restaurar: Você pode restaurar um objeto excluído usando o método `restore()`.

## Integração com API

O sistema busca e enriquece dados de filmes de forma assíncrona a partir de uma API externa (The Movie Database - TMDb) usando `aiohttp`.

## Comando de Carregamento de Dados

Este projeto inclui um comando personalizado para carregar dados de filmes a partir de um arquivo CSV, realizar a limpeza e enriquecimento dos dados com uma API externa (TMDB), e salvar os dados no banco de dados do Django.

### Como executar o comando

1. **Certifique-se de ter o arquivo CSV `movie.csv`**: O arquivo `movie.csv` deve estar localizado no mesmo diretório do comando, ou você pode alterar o caminho do arquivo diretamente no código.

2. **Chave de API**: O comando faz chamadas à API do TMDB. Certifique-se de ter uma chave de API válida e configurada no seu arquivo `.env` (ou no `settings.py`).

3. **Executar o comando**:

   Para executar o comando e carregar os dados, use o seguinte comando:

   ```bash
   python manage.py load_data
   ```

## Estrutura do CSV

O arquivo movie.csv deve conter as seguintes colunas:

- `id`: ID do filme.
- `title`: Título do filme.
- `release_date`: Data de lançamento.
- `overview`: Descrição do filme.
- `popularity`: Popularidade.
- `vote_average`: Média de votos.
- `vote_count`: Contagem de votos.

## Estrutura e Personalização do Django Admin

O projeto inclui uma customização completa da interface do Django Admin para melhorar a experiência de gerenciamento de dados. Aqui estão as principais personalizações e como elas estão configuradas.

### Modelos Gerenciados

1. **Filmes (Movie)**
2. **Gêneros (Genre)**

### Filtros, Campos de Busca e Exibição de Colunas

#### 1. **Model: Filmes (Movie)**

A tabela de filmes exibe informações chave e facilita a busca e filtragem com as seguintes customizações:

- **Colunas Exibidas**:

  - `title`: O título do filme.
  - `get_year`: O ano de lançamento do filme (extraído do campo `release_date`).
  - `get_genres`: A lista de gêneros associados ao filme.
  - `show_poster`: Exibe uma miniatura do pôster do filme.
  - `created_at`: Data de criação do registro no sistema.
  - `updated_at`: Data da última atualização do registro.

- **Filtros Disponíveis**:

  - `release_date`: Permite filtrar filmes pela data de lançamento.
  - `genre__name`: Permite filtrar filmes pelos gêneros (associações do tipo Many-to-Many).

- **Campos de Busca**:
  - `title`: Permite buscar filmes pelo título.

#### 2. Model: Gêneros (Genre)

A tabela de gêneros exibe informações básicas sobre os gêneros cadastrados.

- **Colunas Exibidas**:

  - `name`: O nome do gênero.
  - `created_at`: Data de criação do registro.
  - `updated_at`: Data da última atualização do registro.

- **Campos de Busca**:
  - `name`: Permite buscar gêneros pelo nome.
