# Sistema de Gestão de Biblioteca Pessoal

Uma aplicação web completa para gerenciar sua coleção de livros pessoal, desenvolvida com API REST Django no backend e JavaScript vanilla no frontend.

## 📚 Visão Geral

Este sistema permite organizar e acompanhar sua biblioteca pessoal com recursos para gerenciamento de livros, informações de autores, categorização e controle de empréstimos. A aplicação oferece uma interface limpa e responsiva com estatísticas detalhadas e capacidades de relatórios.

## ✨ Funcionalidades

### Funcionalidades Principais

- **Operações CRUD Completas**: Criar, ler, atualizar e excluir livros, autores e categorias
- **Busca e Filtros Avançados**: Encontre livros por título, autor, categoria ou critérios personalizados
- **Gestão de Empréstimos**: Acompanhe livros emprestados com datas de vencimento e status de devolução
- **Dashboard com Análises**: Estatísticas visuais sobre sua coleção de biblioteca
- **Validação de Dados**: Validação abrangente de entrada tanto no frontend quanto no backend

### Interface do Usuário

- **Design Responsivo**: Funciona perfeitamente em desktop, tablet e dispositivos móveis
- **Dashboard Interativo**: Estatísticas em tempo real e relatórios visuais
- **Navegação Intuitiva**: Interface fácil de usar para todas as operações da biblioteca
- **Ações Rápidas**: Cadastro e busca rápida de livros

## 🛠️ Stack Tecnológico

### Backend

- **Django 4.x**: Framework web e ORM
- **Django REST Framework**: Desenvolvimento de API
- **Python 3.8+**: Linguagem de programação
- **MySQL**: Banco de dados (configurável)

### Frontend

- **HTML5**: Estrutura e semântica
- **CSS3**: Estilização e design responsivo
- **JavaScript Vanilla**: Funcionalidade interativa e comunicação com API
- **Chart.js** (opcional): Para visualizações do dashboard

## 📋 Pré-requisitos

Antes de executar este projeto, certifique-se de ter:

- Python 3.8 ou superior
- pip (instalador de pacotes Python)
- Git
- Um navegador web moderno

## 🚀 Instalação e Configuração

### 1. Clonar o Repositório

```bash
git clone https://github.com/seuusuario/sistema-biblioteca-pessoal.git
cd sistema-biblioteca-pessoal
```

### 2. Criar Ambiente Virtual

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configuração do Banco de Dados

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Criar Superusuário (Opcional)

```bash
python manage.py createsuperuser
```

### 6. Executar Servidor de Desenvolvimento

```bash
python manage.py runserver
```

A aplicação estará disponível em `http://localhost:8000`

## 📁 Estrutura do Projeto

```mdx
sistema-biblioteca-pessoal/
│
├── backend/
│ ├── biblioteca_project/
│ │ ├── settings.py
│ │ ├── urls.py
│ │ └── wsgi.py
│ │
│ ├── biblioteca_app/
│ │ ├── models.py
│ │ ├── serializers.py
│ │ ├── views.py
│ │ ├── urls.py
│ │ └── migrations/
│ │
│ └── manage.py
│
├── frontend/
│ ├── index.html
│ ├── css/
│ │ ├── styles.css
│ │ └── responsive.css
│ │
│ ├── js/
│ ├── main.js
│ ├── api.js
│ └── dashboard.js
│
│
│
│
├── requirements.txt
├── README.md
└── .gitignore
```

## 🔧 Endpoints da API

### Livros

- `GET /api/books/` - Listar todos os livros
- `POST /api/books/` - Criar novo livro
- `GET /api/books/{id}/` - Obter livro específico
- `DELETE /api/books/{id}/` - Excluir livro

### Autores

- `GET /api/authors/` - Listar todos os autores
- `POST /api/authors/` - Criar novo autor
- `GET /api/authors/{id}/` - Obter autor específico
- `DELETE /api/authors/{id}/` - Excluir autor

### Categorias

- `GET /api/categories/` - Listar todas as categorias
- `POST /api/categories/` - Criar nova categoria
- `GET /api/categories/{id}/` - Obter categoria específica
- `DELETE /api/categories/{id}/` - Excluir categoria

### Empréstimos

- `GET /api/loans/` - Listar todos os empréstimos
- `POST /api/loans/` - Criar novo empréstimo
- `PUT /api/loans/{id}/return_book/` - Devolver livro

## 💻 Como Usar

### Adicionando Livros

1. Navegue até a seção "Adicionar Livro"
2. Preencha os detalhes do livro (título, autor, categoria, ISBN, etc.)
3. Clique em "Adicionar Livro" para adicionar à sua biblioteca

### Buscando Livros

1. Use a barra de pesquisa na página de livros
2. Filtre por categoria, autor ou status de disponibilidade
3. Os resultados são atualizados em tempo real conforme você digita

### Gerenciando Empréstimos

1. Navegue para a tela de empréstimos
2. Preencha os dados do usuário que vai pegar o livro e selecione o livro para emprestar
3. Acompanhe as datas de vencimento e devoluções na seção Empréstimos

### Visualizando Estatísticas

1. Acesse o Dashboard para insights visuais
2. Veja total de livros, categorias, empréstimos ativos
3. Observe tendências de leitura e crescimento da coleção

### Variáveis de Ambiente

Crie um arquivo `.env` a partir do `.env.example` para dados sensíveis e preencha os campos que estão sem valor:

```env
SECRET_KEY=sua-chave-secreta
DEBUG=False
DATABASE_URL=url-do-seu-banco
ALLOWED_HOSTS=seu-dominio.com
```

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---
