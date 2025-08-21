# Sistema de Convite de Noivado

Um sistema completo para gerenciar confirmações de presença em um noivado, desenvolvido com Python Flask e SQLite3.

## 🚀 Funcionalidades

- **Página Principal**: Exibe informações do evento e formulário de confirmação
- **Confirmação Simplificada**: Formulário com até 3 nomes por confirmação
- **Área Administrativa Protegida**: Acesso com senha para gerenciamento
- **Armazenamento JSON**: Dados salvos em arquivo JSON para facilidade
- **Configuração do Evento**: Definição de data, local e informações dos noivos
- **Exportação de Dados**: Exportação da lista de convidados em CSV
- **Design Responsivo**: Interface moderna com cor personalizada (#7d8766)
- **Sistema de Login**: Proteção por senha na área administrativa
- **Visualização de Confirmações**: Lista completa de convidados confirmados
- **Edição de Convidados**: Modificar nomes e informações dos convidados
- **Exclusão de Convidados**: Remover convidados da lista

## 📋 Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

## 🛠️ Instalação

1. **Clone ou baixe o projeto**
   ```bash
   # Se estiver usando git
   git clone [url-do-repositorio]
   cd "Convite de noivado"
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute o sistema**
   ```bash
   python app.py
   ```

4. **Acesse no navegador**
   ```
   http://localhost:5000
   ```

## 📱 Como Usar

### 1. Configuração Inicial
- Acesse a **Área Administrativa** (`/admin`)
- Use a senha: `noivado2024` (você pode alterar no arquivo `app.py`)
- Clique em **"Configurar Evento"**
- Preencha as informações dos noivos, data, local e descrição
- Salve a configuração

### 2. Compartilhamento
- Compartilhe o link `http://localhost:5000` com seus convidados
- Os convidados podem acessar e preencher o formulário com até 3 nomes
- Confirmação automática após envio

### 3. Gerenciamento
- Na área administrativa, visualize todas as confirmações
- Edite ou remova convidados conforme necessário
- Exporte a lista de convidados em CSV
- Acompanhe estatísticas em tempo real
- Dados salvos em `convidados.json`
- Sistema protegido por senha personalizada

## 🗄️ Estrutura do Banco de Dados

### Tabela: `convidados`
- `id`: Identificador único
- `nome`: Nome do convidado
- `email`: E-mail (opcional)
- `telefone`: Telefone (opcional)
- `confirmado`: Status de confirmação
- `data_confirmacao`: Data/hora da confirmação
- `numero_acompanhantes`: Quantidade de acompanhantes
- `observacoes`: Observações adicionais
- `data_criacao`: Data de criação do registro

### Tabela: `config_evento`
- `id`: Identificador único
- `nome_noivos`: Nomes dos noivos
- `data_evento`: Data do evento
- `hora_evento`: Horário do evento
- `local_evento`: Local do evento
- `descricao_evento`: Descrição adicional
- `data_criacao`: Data de criação da configuração

## 🌐 Rotas da Aplicação

- `/`: Página principal com informações do evento
- `/confirmar`: Formulário de confirmação de presença
- `/admin`: Área administrativa
- `/configurar`: Configuração do evento
- `/editar_convidado/<id>`: Editar convidado específico
- `/deletar_convidado/<id>`: Remover convidado específico
- `/api/convidados`: API para listar convidados (JSON)
- `/api/estatisticas`: API para estatísticas (JSON)

## 🎨 Personalização

O sistema usa CSS customizado com:
- Gradientes modernos
- Animações suaves
- Design responsivo
- Ícones Font Awesome
- Paleta de cores roxa/azul

## 📊 Funcionalidades Avançadas

- **Exportação CSV**: Baixe a lista completa de convidados
- **Estatísticas em Tempo Real**: Acompanhe confirmações vs pendentes
- **Validação de Formulários**: Campos obrigatórios e validações
- **Mensagens Flash**: Feedback visual para o usuário
- **API REST**: Endpoints para integração externa

## 🔧 Configuração de Produção

Para usar em produção:

1. **Altere a chave secreta** em `app.py`:
   ```python
   app.secret_key = 'sua_chave_secreta_muito_segura_aqui'
   ```

2. **Configure um servidor WSGI** como Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

3. **Use um proxy reverso** como Nginx para melhor performance

## 📝 Licença

Este projeto é de código aberto e pode ser usado livremente.

## 🤝 Contribuição

Sinta-se à vontade para contribuir com melhorias, correções ou novas funcionalidades!

---

**Desenvolvido com ❤️ para celebrar momentos especiais** 