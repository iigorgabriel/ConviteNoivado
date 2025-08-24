#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from supabase import create_client

# Carregar variáveis de ambiente
load_dotenv()

def test_supabase():
    try:
        print("🔍 Testando conexão com Supabase...")
        
        # Verificar variáveis
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        
        print(f"URL: {url}")
        print(f"Key: {key[:20]}..." if key else "Key: None")
        
        if not url or not key:
            print("❌ Variáveis de ambiente não encontradas!")
            return False
        
        # Criar cliente
        supabase = create_client(url, key)
        print("✅ Cliente Supabase criado")
        
        # Testar inserção
        print("🔍 Testando inserção...")
        result = supabase.table('convidados').insert({
            'nomes': ['Teste Python'],
            'total_pessoas': 1
        }).execute()
        
        print("✅ Inserção bem-sucedida!")
        print(f"Dados inseridos: {result.data}")
        
        # Testar leitura
        print("🔍 Testando leitura...")
        result = supabase.table('convidados').select('*').execute()
        
        print("✅ Leitura bem-sucedida!")
        print(f"Total de registros: {len(result.data)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
        print(f"Tipo do erro: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = test_supabase()
    if success:
        print("\n🎉 Todos os testes passaram!")
    else:
        print("\n💥 Alguns testes falharam!")
