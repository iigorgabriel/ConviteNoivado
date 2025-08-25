from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'sua_chave_secreta_aqui')

# Configuração do Supabase
supabase: Client = create_client(
    os.getenv('SUPABASE_URL'), 
    os.getenv('SUPABASE_KEY')
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/confirmar', methods=['POST'])
def confirmar():
    try:
        # Verificar se as variáveis de ambiente estão configuradas
        if not os.getenv('SUPABASE_URL') or not os.getenv('SUPABASE_KEY'):
            return redirect(url_for('sucesso') + '?error=config')
        
        # Coletar nomes do formulário
        nomes = []
        i = 1
        while f'nome{i}' in request.form:
            nome = request.form[f'nome{i}'].strip()
            if nome:
                nomes.append(nome)
            i += 1
        
        if not nomes:
            return redirect(url_for('sucesso') + '?error=nome')
        
        # Inserir no Supabase
        novo_convidado = {
            'nomes': nomes,
            'total_pessoas': len(nomes),
            'data_confirmacao': datetime.now().isoformat()
        }
        
        result = supabase.table('convidados').insert(novo_convidado).execute()
        
        return redirect(url_for('sucesso'))
        
    except Exception as e:
        error_msg = f'Erro ao confirmar presença: {str(e)}'
        print(f"DEBUG: {error_msg}")  # Log para debug
        return redirect(url_for('sucesso') + '?error=geral')

@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        senha = request.form.get('senha')
        if senha == os.getenv('ADMIN_PASSWORD', 'noivado2024'):
            session['admin_logado'] = True
            return redirect(url_for('admin'))
        else:
            flash('Senha incorreta!', 'error')
    
    if not session.get('admin_logado'):
        return render_template('admin_login.html')
    
    try:
        # Buscar dados do Supabase
        result = supabase.table('convidados').select('*').order('created_at', desc=True).execute()
        convidados = result.data
        
        total_convidados = len(convidados)
        total_pessoas = sum(convidado['total_pessoas'] for convidado in convidados)
        
        return render_template('admin.html', convidados=convidados, 
                             total_convidados=total_convidados, 
                             total_pessoas=total_pessoas)
    except Exception as e:
        flash(f'Erro ao carregar dados: {str(e)}', 'error')
        return render_template('admin.html', convidados=[], 
                             total_convidados=0, total_pessoas=0)

@app.route('/logout')
def logout():
    session.pop('admin_logado', None)
    return redirect(url_for('index'))

@app.route('/editar_convidado/<int:convidado_id>', methods=['GET', 'POST'])
def editar_convidado(convidado_id):
    if not session.get('admin_logado'):
        return redirect(url_for('admin'))
    
    try:
        if request.method == 'POST':
            # Coletar nomes do formulário
            nomes = []
            i = 1
            while f'nome{i}' in request.form:
                nome = request.form[f'nome{i}'].strip()
                if nome:
                    nomes.append(nome)
                i += 1
            
            if not nomes:
                flash('Por favor, insira pelo menos um nome.', 'error')
                return redirect(url_for('editar_convidado', convidado_id=convidado_id))
            
            # Atualizar no Supabase
            dados_atualizados = {
                'nomes': nomes,
                'total_pessoas': len(nomes),
                'data_confirmacao': datetime.now().isoformat()
            }
            
            supabase.table('convidados').update(dados_atualizados).eq('id', convidado_id).execute()
            
            flash('Convidado atualizado com sucesso!', 'success')
            return redirect(url_for('admin'))
        
        # Buscar dados do convidado
        result = supabase.table('convidados').select('*').eq('id', convidado_id).execute()
        
        if not result.data:
            flash('Convidado não encontrado!', 'error')
            return redirect(url_for('admin'))
        
        convidado = result.data[0]
        return render_template('editar_convidado.html', convidado=convidado)
        
    except Exception as e:
        flash(f'Erro ao editar convidado: {str(e)}', 'error')
        return redirect(url_for('admin'))

@app.route('/deletar_convidado/<int:convidado_id>')
def deletar_convidado(convidado_id):
    if not session.get('admin_logado'):
        return redirect(url_for('admin'))
    
    try:
        # Deletar do Supabase
        supabase.table('convidados').delete().eq('id', convidado_id).execute()
        
        flash('Convidado removido com sucesso!', 'success')
        return redirect(url_for('admin'))
        
    except Exception as e:
        flash(f'Erro ao deletar convidado: {str(e)}', 'error')
        return redirect(url_for('admin'))

@app.route('/api/convidados')
def api_convidados():
    try:
        result = supabase.table('convidados').select('*').order('created_at', desc=True).execute()
        return jsonify(result.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Não chame app.run() aqui. A Vercel importa 'app' automaticamente.

# Para desenvolvimento local
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
