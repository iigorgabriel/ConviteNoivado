#!/usr/bin/env python3
"""
Script de teste para verificar se o sistema de noivado está funcionando
"""

import sqlite3
import os
from datetime import datetime

def testar_banco_dados():
    """Testa a criação e conexão com o banco de dados"""
    print("🔍 Testando banco de dados...")
    
    # Verifica se o arquivo do banco existe
    if os.path.exists('noivado.db'):
        print("✅ Banco de dados encontrado")
    else:
        print("❌ Banco de dados não encontrado")
        return False
    
    try:
        # Testa conexão
        conn = sqlite3.connect('noivado.db')
        cursor = conn.cursor()
        
        # Verifica se as tabelas existem
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelas = [row[0] for row in cursor.fetchall()]
        
        if 'convidados' in tabelas and 'config_evento' in tabelas:
            print("✅ Tabelas criadas corretamente")
        else:
            print("❌ Tabelas não encontradas")
            return False
        
        # Testa inserção de dados
        cursor.execute('''
            INSERT INTO config_evento (nome_noivos, data_evento, hora_evento, local_evento, descricao_evento)
            VALUES (?, ?, ?, ?, ?)
        ''', ('Teste João e Maria', '2024-12-25', '19:00', 'Local de Teste', 'Evento de teste'))
        
        cursor.execute('''
            INSERT INTO convidados (nome, email, telefone, confirmado, numero_acompanhantes, observacoes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('Convidado Teste', 'teste@email.com', '(11) 99999-9999', True, 2, 'Teste do sistema'))
        
        conn.commit()
        print("✅ Inserção de dados funcionando")
        
        # Testa consulta
        cursor.execute('SELECT COUNT(*) FROM convidados')
        total = cursor.fetchone()[0]
        print(f"✅ Consulta funcionando - Total de convidados: {total}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro no banco de dados: {e}")
        return False

def testar_arquivos():
    """Testa se todos os arquivos necessários existem"""
    print("\n📁 Testando arquivos...")
    
    arquivos_necessarios = [
        'app.py',
        'requirements.txt',
        'README.md',
        'templates/base.html',
        'templates/index.html',
        'templates/confirmar.html',
        'templates/admin.html',
        'templates/configurar.html'
    ]
    
    todos_existem = True
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo}")
        else:
            print(f"❌ {arquivo}")
            todos_existem = False
    
    return todos_existem

def testar_dependencias():
    """Testa se as dependências podem ser importadas"""
    print("\n📦 Testando dependências...")
    
    try:
        import flask
        print("✅ Flask importado com sucesso")
    except ImportError:
        print("❌ Flask não encontrado")
        return False
    
    try:
        import sqlite3
        print("✅ SQLite3 importado com sucesso")
    except ImportError:
        print("❌ SQLite3 não encontrado")
        return False
    
    return True

def main():
    """Função principal de teste"""
    print("🎉 TESTE DO SISTEMA DE CONVITE DE NOIVADO")
    print("=" * 50)
    
    # Testa arquivos
    arquivos_ok = testar_arquivos()
    
    # Testa dependências
    deps_ok = testar_dependencias()
    
    # Testa banco de dados
    db_ok = testar_banco_dados()
    
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES:")
    print(f"Arquivos: {'✅ OK' if arquivos_ok else '❌ FALHOU'}")
    print(f"Dependências: {'✅ OK' if deps_ok else '❌ FALHOU'}")
    print(f"Banco de dados: {'✅ OK' if db_ok else '❌ FALHOU'}")
    
    if arquivos_ok and deps_ok and db_ok:
        print("\n🎉 SISTEMA PRONTO PARA USO!")
        print("Para iniciar o servidor, execute: python app.py")
        print("Acesse: http://localhost:5000")
    else:
        print("\n⚠️  Alguns testes falharam. Verifique os erros acima.")

if __name__ == "__main__":
    main() 