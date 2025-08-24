# 🚀 Configuração do Supabase

Este guia te ajudará a configurar o Supabase para o projeto de convite de noivado.

## 📋 Passo a Passo

### 1. Criar conta no Supabase

1. Acesse [supabase.com](https://supabase.com)
2. Clique em "Start your project"
3. Faça login com GitHub ou crie uma conta
4. Clique em "New Project"

### 2. Criar novo projeto

1. **Nome do projeto**: `convite-noivado` (ou qualquer nome)
2. **Database Password**: Crie uma senha forte (guarde ela!)
3. **Region**: Escolha a região mais próxima (ex: São Paulo)
4. Clique em "Create new project"

### 3. Aguardar configuração

O Supabase vai configurar seu projeto (pode demorar 1-2 minutos).

### 4. Obter credenciais

1. No dashboard, vá em **Settings** (ícone de engrenagem)
2. Clique em **API**
3. Copie:
   - **Project URL** (ex: `https://abcdefghijklmnop.supabase.co`)
   - **anon public** key (começa com `eyJ...`)

### 5. Configurar banco de dados

1. No dashboard, vá em **SQL Editor**
2. Clique em **New query**
3. Cole e execute este SQL:

```sql
-- Tabela de convidados
CREATE TABLE convidados (
    id SERIAL PRIMARY KEY,
    nomes TEXT[] NOT NULL,
    total_pessoas INTEGER NOT NULL,
    data_confirmacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Habilitar Row Level Security
ALTER TABLE convidados ENABLE ROW LEVEL SECURITY;

-- Política para permitir inserção (confirmação de presença)
CREATE POLICY "Permitir inserção de convidados" ON convidados
    FOR INSERT WITH CHECK (true);

-- Política para permitir leitura (listar convidados)
CREATE POLICY "Permitir leitura de convidados" ON convidados
    FOR SELECT USING (true);

-- Política para permitir atualização e deleção (apenas para admins)
CREATE POLICY "Permitir admin" ON convidados
    FOR ALL USING (auth.role() = 'authenticated');
```

### 6. Configurar variáveis de ambiente

1. Copie o arquivo `env.example` para `.env`:
   ```bash
   cp env.example .env
   ```

2. Edite o `.env` com suas credenciais:
   ```env
   SUPABASE_URL=https://seu-projeto.supabase.co
   SUPABASE_KEY=sua_chave_anon_aqui
   SECRET_KEY=uma_chave_secreta_aleatoria_aqui
   ADMIN_PASSWORD=noivado2024
   ```

### 7. Testar conexão

Execute o projeto localmente:
```bash
pip install -r requirements.txt
python api/index.py
```

## 🔧 Configurações Adicionais (Opcional)

### Autenticação mais segura

Se quiser usar autenticação do Supabase em vez de senha simples:

1. No Supabase, vá em **Authentication** > **Settings**
2. Configure **Site URL** com seu domínio
3. Em **Auth Providers**, configure email/password se necessário

### Backup automático

O Supabase faz backup automático, mas você pode configurar:

1. Vá em **Settings** > **Database**
2. Configure **Backup Schedule** se necessário

### Monitoramento

1. Vá em **Logs** para ver requisições
2. Use **Analytics** para métricas

## 🚨 Troubleshooting

### Erro de conexão
- Verifique se as credenciais estão corretas
- Confirme se o projeto está ativo
- Teste a conexão no SQL Editor

### Erro de permissão
- Verifique se as políticas RLS estão corretas
- Confirme se a tabela foi criada

### Erro de CORS (em produção)
- Configure **Site URL** nas configurações de autenticação
- Adicione seu domínio em **Additional Redirect URLs**

## 📞 Suporte

- [Documentação Supabase](https://supabase.com/docs)
- [Discord Supabase](https://discord.supabase.com)
- [GitHub Issues](https://github.com/supabase/supabase/issues)
