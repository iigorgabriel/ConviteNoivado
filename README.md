# Convite de Noivado - Igor & Júlia

Sistema de confirmação de presença para noivado desenvolvido com Flask e Supabase.

## 🚀 Funcionalidades

- **Página Principal**: Formulário para confirmar presença com até 3 nomes
- **Área Administrativa**: Protegida por senha para gerenciar convidados
- **Banco de Dados**: Supabase (PostgreSQL) para armazenamento robusto
- **Deploy**: Otimizado para Vercel
- **Design Responsivo**: Interface moderna e adaptável

## 🛠️ Tecnologias

- **Backend**: Flask (Python)
- **Banco de Dados**: Supabase (PostgreSQL)
- **Frontend**: HTML, CSS, JavaScript
- **Deploy**: Vercel
- **Ícones**: Font Awesome

## 📋 Pré-requisitos

- Python 3.8+
- Conta no Supabase
- Conta no Vercel (para deploy)

## ⚙️ Configuração

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd convite-noivado
```

### 2. Configure o Supabase

1. Crie uma conta em [supabase.com](https://supabase.com)
2. Crie um novo projeto
3. Vá em Settings > API e copie:
   - Project URL
   - anon/public key

### 3. Configure as variáveis de ambiente

Copie o arquivo `env.example` para `.env`:
```bash
cp env.example .env
```

Edite o `.env` com suas credenciais:
```env
SUPABASE_URL=sua_url_do_supabase_aqui
SUPABASE_KEY=sua_chave_anon_do_supabase_aqui
SECRET_KEY=sua_chave_secreta_aqui
ADMIN_PASSWORD=noivado2024
```

### 4. Instale as dependências
```bash
pip install -r requirements.txt
```

### 5. Configure o banco de dados

Execute o SQL no Supabase SQL Editor:

```sql
-- Tabela de convidados
CREATE TABLE convidados (
    id SERIAL PRIMARY KEY,
    nomes TEXT[] NOT NULL,
    total_pessoas INTEGER NOT NULL,
    data_confirmacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Políticas de segurança (RLS)
ALTER TABLE convidados ENABLE ROW LEVEL SECURITY;

-- Permitir inserção para todos (confirmação de presença)
CREATE POLICY "Permitir inserção de convidados" ON convidados
    FOR INSERT WITH CHECK (true);

-- Permitir leitura para todos (API pública)
CREATE POLICY "Permitir leitura de convidados" ON convidados
    FOR SELECT USING (true);

-- Permitir atualização e deleção apenas para admins (será configurado depois)
CREATE POLICY "Permitir admin" ON convidados
    FOR ALL USING (auth.role() = 'authenticated');
```

## 🚀 Como Usar

### Desenvolvimento Local
```bash
python api/index.py
```

### Deploy na Vercel

1. Conecte seu repositório ao Vercel
2. Configure as variáveis de ambiente no Vercel:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `SECRET_KEY`
   - `ADMIN_PASSWORD`
3. Deploy automático!

## 📁 Estrutura do Projeto

```
├── api/
│   ├── index.py          # Aplicação Flask principal
│   ├── templates/        # Templates HTML
│   └── static/           # Arquivos estáticos (CSS, imagens)
├── requirements.txt      # Dependências Python
├── vercel.json          # Configuração Vercel
├── env.example          # Exemplo de variáveis de ambiente
└── README.md            # Este arquivo
```

## 🔐 Segurança

- Senha administrativa configurável
- Row Level Security (RLS) no Supabase
- Variáveis de ambiente para credenciais
- Validação de entrada nos formulários

## 📊 Dados

Os dados dos convidados são armazenados no Supabase com:
- Nomes (array de strings)
- Total de pessoas
- Data de confirmação
- Timestamp de criação

## 🔄 Rotas

- `/` - Página principal com formulário de confirmação
- `/admin` - Área administrativa (protegida por senha)
- `/confirmar` - Endpoint para confirmar presença
- `/editar_convidado/<id>` - Editar convidado
- `/deletar_convidado/<id>` - Deletar convidado
- `/api/convidados` - API para listar convidados

## 🎨 Personalização

- Cores principais: `#7d8766` (verde)
- Logo: Adicione sua logo em `api/static/images/logo-noivado.png`
- Endereço: Configure no template `index.html`

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório. 