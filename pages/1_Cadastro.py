import streamlit as st
from database import Pessoa, session
import pandas as pd
from sqlalchemy import func

st.set_page_config(page_title="Cadastro de Pessoas", page_icon="📝", layout="wide")
st.header("Cadastro de Pessoas")

def adicionar_pessoa():
    with st.form("Adicionar Novo", clear_on_submit=True):
        st.subheader("Adicionar Nova Pessoa")
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome")
            data_nascimento = st.date_input("Data de Nascimento")
            telefone = st.text_input("Telefone")
            tipo = st.selectbox("Tipo", ["Jovem", "Adolescente"])
        with col2:
            batizado_aguas = st.selectbox("Batizado nas Águas", ["Sim", "Não"]) == "Sim"
            batizado_espirito = st.selectbox("Batizado no Espírito Santo", ["Sim", "Não"]) == "Sim"
            status = st.selectbox("Status", ["Ativo", "Inativo"])
            observacao = st.text_area("Observação")
        submit = st.form_submit_button("Adicionar")

        if submit:
            # Verificar se já existe alguém com o mesmo nome
            existe = session.query(Pessoa).filter(func.lower(Pessoa.nome) == nome.lower()).first()
            if existe:
                st.error("Já existe alguém cadastrado com este nome.")
            else:
                nova_pessoa = Pessoa(
                    nome=nome,
                    data_nascimento=data_nascimento,
                    telefone=telefone,
                    batizado_aguas=batizado_aguas,
                    batizado_espirito=batizado_espirito,
                    status=status,
                    tipo=tipo,
                    observacao=observacao
                )
                session.add(nova_pessoa)
                session.commit()
                st.success("Adicionado com sucesso!")
                st.experimental_rerun()

def exibir_pessoas():
    st.subheader("Lista de Pessoas")

    # Filtros organizados em colunas
    with st.expander("Filtros"):
        col1, col2, col3 = st.columns(3)
        with col1:
            filtro_nome = st.text_input("Filtrar por nome")
        with col2:
            filtro_status = st.selectbox("Filtrar por status", ["Todos", "Ativo", "Inativo"])
        with col3:
            filtro_tipo = st.selectbox("Filtrar por tipo", ["Todos", "Jovem", "Adolescente"])

    query = session.query(Pessoa)
    if filtro_nome:
        query = query.filter(Pessoa.nome.ilike(f"%{filtro_nome}%"))
    if filtro_status != "Todos":
        query = query.filter_by(status=filtro_status)
    if filtro_tipo != "Todos":
        query = query.filter_by(tipo=filtro_tipo)

    data = pd.read_sql(query.statement, session.bind)
    if data.empty:
        st.info("Nenhum registro encontrado com os filtros aplicados.")
        return

    # Melhorar a tabela de dados
    data['Data de Nascimento'] = pd.to_datetime(data['data_nascimento']).dt.strftime('%d/%m/%Y')
    data['Batizado nas Águas'] = data['batizado_aguas'].apply(lambda x: 'Sim' if x else 'Não')
    data['Batizado no Espírito Santo'] = data['batizado_espirito'].apply(lambda x: 'Sim' if x else 'Não')
    data = data.rename(columns={
        'nome': 'Nome',
        'tipo': 'Tipo',
        'telefone': 'Telefone',
        'status': 'Status',
        'observacao': 'Observação'
    })
    data = data[['id', 'Nome', 'Tipo', 'Data de Nascimento', 'Telefone', 'Batizado nas Águas', 'Batizado no Espírito Santo', 'Status', 'Observação']]

    # Exibir tabela interativa
    st.dataframe(data.style.format({
        'Data de Nascimento': '{}',
        'Batizado nas Águas': '{}',
        'Batizado no Espírito Santo': '{}'
    }), use_container_width=True)

    # Selecionar pessoa para editar
    st.subheader("Editar Pessoa")
    with st.expander("Selecione a Pessoa para Editar"):
        pessoas_opcoes = data[['id', 'Nome']].apply(lambda row: f"{row['id']} - {row['Nome']}", axis=1)
        pessoa_selecionada = st.selectbox("Selecione pelo ID e Nome", pessoas_opcoes)
        if pessoa_selecionada:
            pessoa_id = int(pessoa_selecionada.split(' - ')[0])
            editar_pessoa(pessoa_id)

def editar_pessoa(pessoa_id):
    pessoa = session.query(Pessoa).filter_by(id=pessoa_id).first()
    if pessoa:
        with st.form(f"Editar Pessoa ID {pessoa.id}", clear_on_submit=True):
            st.subheader(f"Editando: {pessoa.nome}")
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome", value=pessoa.nome)
                data_nascimento = st.date_input("Data de Nascimento", value=pessoa.data_nascimento)
                telefone = st.text_input("Telefone", value=pessoa.telefone)
                tipo = st.selectbox("Tipo", ["Jovem", "Adolescente"], index=0 if pessoa.tipo == "Jovem" else 1)
            with col2:
                batizado_aguas = st.selectbox(
                    "Batizado nas Águas", ["Sim", "Não"], index=0 if pessoa.batizado_aguas else 1
                ) == "Sim"
                batizado_espirito = st.selectbox(
                    "Batizado no Espírito Santo", ["Sim", "Não"], index=0 if pessoa.batizado_espirito else 1
                ) == "Sim"
                status = st.selectbox("Status", ["Ativo", "Inativo"], index=0 if pessoa.status == "Ativo" else 1)
                observacao = st.text_area("Observação", value=pessoa.observacao)
            submit = st.form_submit_button("Salvar")

            if submit:
                # Verificar se o novo nome já existe em outro registro
                existe = session.query(Pessoa).filter(
                    func.lower(Pessoa.nome) == nome.lower(), Pessoa.id != pessoa_id
                ).first()
                if existe:
                    st.error("Já existe alguém cadastrado com este nome.")
                else:
                    pessoa.nome = nome
                    pessoa.data_nascimento = data_nascimento
                    pessoa.telefone = telefone
                    pessoa.batizado_aguas = batizado_aguas
                    pessoa.batizado_espirito = batizado_espirito
                    pessoa.status = status
                    pessoa.tipo = tipo
                    pessoa.observacao = observacao
                    session.commit()
                    st.success("Atualizado com sucesso.")
                    st.experimental_rerun()
    else:
        st.error("Pessoa não encontrada.")

# Organização em abas
tab1, tab2 = st.tabs(["Adicionar Pessoa", "Gerenciar Pessoas"])

with tab1:
    adicionar_pessoa()

with tab2:
    exibir_pessoas()
