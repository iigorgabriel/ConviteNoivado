from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = '1234'  # Importante para sessões

# Configuração do banco de dados
DATABASE = 'noivado.db'

def init_db():
    """Inicializa o banco de dados"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Tabela de convidados
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS convidados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT,
            telefone TEXT,
            confirmado BOOLEAN DEFAULT FALSE,
            data_confirmacao DATETIME,
            numero_acompanhantes INTEGER DEFAULT 0,
            observacoes TEXT,
            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabela de configurações do evento
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS config_evento (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_noivos TEXT NOT NULL,
            data_evento DATE NOT NULL,
            hora_evento TIME NOT NULL,
            local_evento TEXT NOT NULL,
            descricao_evento TEXT,
            data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Retorna uma conexão com o banco de dados"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Página principal"""
    conn = get_db_connection()
    config = conn.execute('SELECT * FROM config_evento ORDER BY id DESC LIMIT 1').fetchone()
    conn.close()
    
    # Carregar estatísticas do JSON
    import json
    import os
    
    total_convidados = 0
    total_pessoas = 0
    convidados_file = 'convidados.json'
    
    if os.path.exists(convidados_file):
        with open(convidados_file, 'r', encoding='utf-8') as f:
            convidados = json.load(f)
            total_convidados = len(convidados)
            total_pessoas = sum(convidado['total_pessoas'] for convidado in convidados)
    
    return render_template('index.html', config=config, total_convidados=total_convidados, total_pessoas=total_pessoas)

@app.route('/confirmar', methods=['GET', 'POST'])
def confirmar():
    """Página de confirmação de presença"""
    if request.method == 'POST':
        # Coletar todos os nomes do formulário
        nomes = []
        i = 1
        while f'nome{i}' in request.form:
            nome = request.form.get(f'nome{i}', '').strip()
            if nome:  # Só adiciona se não estiver vazio
                nomes.append(nome)
            i += 1
        
        if not nomes:
            flash('Pelo menos um nome é obrigatório!', 'danger')
            return redirect(url_for('index'))
        
        # Salvar no JSON para facilitar o gerenciamento
        import json
        import os
        
        convidados_file = 'convidados.json'
        convidados = []
        
        if os.path.exists(convidados_file):
            with open(convidados_file, 'r', encoding='utf-8') as f:
                convidados = json.load(f)
        
        novo_convidado = {
            'id': len(convidados) + 1,
            'nomes': nomes,
            'data_confirmacao': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_pessoas': len(nomes)
        }
        
        convidados.append(novo_convidado)
        
        with open(convidados_file, 'w', encoding='utf-8') as f:
            json.dump(convidados, f, ensure_ascii=False, indent=2)
        
        flash(f'Confirmação registrada com sucesso! {len(nomes)} pessoa(s) confirmada(s).', 'success')
        return redirect(url_for('index'))
    
    return render_template('confirmar.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """Página administrativa"""
    if request.method == 'POST':
        senha = request.form.get('senha', '')
        # Senha definida pelo usuário - você pode alterar aqui
        senha_correta = 'noivado2024'
        
        if senha == senha_correta:
            session['admin_logado'] = True
            return redirect(url_for('admin'))
        else:
            flash('Senha incorreta!', 'danger')
    
    # Verificar se está logado
    if not session.get('admin_logado'):
        return render_template('admin_login.html')
    
    # Carregar dados do JSON
    import json
    import os
    
    convidados = []
    convidados_file = 'convidados.json'
    
    if os.path.exists(convidados_file):
        with open(convidados_file, 'r', encoding='utf-8') as f:
            convidados = json.load(f)
    
    # Calcular estatísticas
    total_pessoas = sum(convidado['total_pessoas'] for convidado in convidados)
    total_convidados = len(convidados)
    
    conn = get_db_connection()
    config = conn.execute('SELECT * FROM config_evento ORDER BY id DESC LIMIT 1').fetchone()
    conn.close()
    
    return render_template('admin.html', convidados=convidados, config=config, 
                         total_pessoas=total_pessoas, total_convidados=total_convidados)

@app.route('/configurar', methods=['GET', 'POST'])
def configurar():
    """Configuração do evento"""
    if request.method == 'POST':
        nome_noivos = request.form['nome_noivos']
        data_evento = request.form['data_evento']
        hora_evento = request.form['hora_evento']
        local_evento = request.form['local_evento']
        descricao_evento = request.form.get('descricao_evento', '')
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO config_evento (nome_noivos, data_evento, hora_evento, local_evento, descricao_evento)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome_noivos, data_evento, hora_evento, local_evento, descricao_evento))
        conn.commit()
        conn.close()
        
        flash('Configuração salva com sucesso!', 'success')
        return redirect(url_for('admin'))
    
    conn = get_db_connection()
    config = conn.execute('SELECT * FROM config_evento ORDER BY id DESC LIMIT 1').fetchone()
    conn.close()
    
    return render_template('configurar.html', config=config)

@app.route('/logout')
def logout():
    """Logout da área administrativa"""
    session.pop('admin_logado', None)
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/api/convidados')
def api_convidados():
    """API para listar convidados"""
    import json
    import os
    
    convidados = []
    convidados_file = 'convidados.json'
    
    if os.path.exists(convidados_file):
        with open(convidados_file, 'r', encoding='utf-8') as f:
            convidados = json.load(f)
    
    return jsonify(convidados)

@app.route('/api/estatisticas')
def api_estatisticas():
    """API para estatísticas"""
    import json
    import os
    
    convidados = []
    convidados_file = 'convidados.json'
    
    if os.path.exists(convidados_file):
        with open(convidados_file, 'r', encoding='utf-8') as f:
            convidados = json.load(f)
    
    total_convidados = len(convidados)
    total_pessoas = sum(convidado['total_pessoas'] for convidado in convidados)
    
    return jsonify({
        'total_convidados': total_convidados,
        'total_pessoas': total_pessoas
    })

@app.route('/editar_convidado/<int:convidado_id>', methods=['GET', 'POST'])
def editar_convidado(convidado_id):
    """Editar convidado"""
    # Verificar se está logado
    if not session.get('admin_logado'):
        flash('Acesso negado!', 'danger')
        return redirect(url_for('admin'))
    
    import json
    import os
    
    convidados_file = 'convidados.json'
    convidados = []
    
    if os.path.exists(convidados_file):
        with open(convidados_file, 'r', encoding='utf-8') as f:
            convidados = json.load(f)
    
    # Encontrar o convidado
    convidado = None
    for c in convidados:
        if c['id'] == convidado_id:
            convidado = c
            break
    
    if not convidado:
        flash('Convidado não encontrado!', 'danger')
        return redirect(url_for('admin'))
    
    if request.method == 'POST':
        # Coletar todos os nomes do formulário
        nomes = []
        i = 1
        while f'nome{i}' in request.form:
            nome = request.form.get(f'nome{i}', '').strip()
            if nome:  # Só adiciona se não estiver vazio
                nomes.append(nome)
            i += 1
        
        if not nomes:
            flash('Pelo menos um nome é obrigatório!', 'danger')
            return render_template('editar_convidado.html', convidado=convidado)
        
        # Atualizar o convidado
        convidado['nomes'] = nomes
        convidado['total_pessoas'] = len(nomes)
        convidado['data_confirmacao'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Salvar no arquivo
        with open(convidados_file, 'w', encoding='utf-8') as f:
            json.dump(convidados, f, ensure_ascii=False, indent=2)
        
        flash('Convidado atualizado com sucesso!', 'success')
        return redirect(url_for('admin'))
    
    return render_template('editar_convidado.html', convidado=convidado)

@app.route('/deletar_convidado/<int:convidado_id>')
def deletar_convidado(convidado_id):
    """Deletar convidado"""
    # Verificar se está logado
    if not session.get('admin_logado'):
        flash('Acesso negado!', 'danger')
        return redirect(url_for('admin'))
    
    import json
    import os
    
    convidados_file = 'convidados.json'
    convidados = []
    
    if os.path.exists(convidados_file):
        with open(convidados_file, 'r', encoding='utf-8') as f:
            convidados = json.load(f)
    
    # Encontrar e remover o convidado
    convidado_encontrado = False
    for i, convidado in enumerate(convidados):
        if convidado['id'] == convidado_id:
            del convidados[i]
            convidado_encontrado = True
            break
    
    if not convidado_encontrado:
        flash('Convidado não encontrado!', 'danger')
        return redirect(url_for('admin'))
    
    # Reorganizar IDs
    for i, convidado in enumerate(convidados):
        convidado['id'] = i + 1
    
    # Salvar no arquivo
    with open(convidados_file, 'w', encoding='utf-8') as f:
        json.dump(convidados, f, ensure_ascii=False, indent=2)
    
    flash('Convidado removido com sucesso!', 'success')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000) 