# Configurar Senha Administrativa

## 🔐 Como Alterar a Senha

### 1. **Localizar o Arquivo**
Abra o arquivo `app.py` e procure pela linha:

```python
senha_correta = 'noivado2024'
```

### 2. **Alterar a Senha**
Substitua `'noivado2024'` pela senha que você deseja usar:

```python
senha_correta = 'SUA_SENHA_AQUI'
```

### 3. **Exemplo**
Se você quiser usar a senha `minha_senha_123`:

```python
senha_correta = 'minha_senha_123'
```
    
## 🔒 Segurança

- **Use uma senha forte**: Combine letras, números e símbolos
- **Não compartilhe**: Mantenha a senha em segurança
- **Altere regularmente**: Troque a senha periodicamente

## 📱 Como Acessar

1. Acesse o site: `http://localhost:5000`
2. Clique em **"Área Administrativa"**
3. Digite sua senha
4. Clique em **"Entrar"**

## ✅ Funcionalidades da Área Administrativa

- **Visualizar Confirmações**: Veja todos os convidados que confirmaram presença
- **Estatísticas**: Total de convidados e pessoas confirmadas
- **Exportar Dados**: Baixe a lista em formato CSV
- **Configurar Evento**: Defina informações do noivado
- **Logout**: Sair da área administrativa

## 🚨 Importante

- A senha atual é: `noivado2024`
- Altere esta senha antes de usar em produção
- A sessão expira quando você fecha o navegador
