import streamlit as st
from database import Pessoa, session
import pandas as pd
from sqlalchemy import func

st.header("Cadastro de Pessoas")

def adicionar_pessoa():
    with st.form("Adicionar Novo"):
        nome = st.text_input("Nome")
        data_nascimento = st.date_input("Data de Nascimento")
        telefone = st.text_input("Telefone")
        batizado_aguas = st.selectbox("Batizado nas Águas", ["Sim", "Não"]) == "Sim"
        batizado_espirito = st.selectbox("Batizado no Espírito Santo", ["Sim", "Não"]) == "Sim"
        status = st.selectbox("Status", ["Ativo", "Inativo"])
        tipo = st.selectbox("Tipo", ["Jovem", "Adolescente"])
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
                st.rerun()

def exibir_pessoas():
    st.subheader("Lista de Pessoas")

    # Filtros
    filtro_nome = st.text_input("Filtrar por nome")
    filtro_status = st.selectbox("Filtrar por status", ["Todos", "Ativo", "Inativo"])
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
        st.info("Nenhum encontrado com os filtros aplicados.")
        return

    # Exibir tabela interativa
    st.table(data[['id', 'nome', 'tipo', 'data_nascimento', 'telefone', 'batizado_aguas', 'batizado_espirito', 'status']])

    # Selecionar pessoa para editar
    pessoa_id = st.number_input("Digite o ID da Pessoa para Editar", min_value=0, step=1)
    if pessoa_id > 0:
        editar_pessoa(pessoa_id)

def editar_pessoa(pessoa_id):
    pessoa = session.query(Pessoa).filter_by(id=pessoa_id).first()
    if pessoa:
        with st.form(f"Editar {pessoa.nome}"):
            nome = st.text_input("Nome", value=pessoa.nome)
            data_nascimento = st.date_input("Data de Nascimento", value=pessoa.data_nascimento)
            telefone = st.text_input("Telefone", value=pessoa.telefone)
            batizado_aguas = st.selectbox(
                "Batizado nas Águas", ["Sim", "Não"], index=0 if pessoa.batizado_aguas else 1
            ) == "Sim"
            batizado_espirito = st.selectbox(
                "Batizado no Espírito Santo", ["Sim", "Não"], index=0 if pessoa.batizado_espirito else 1
            ) == "Sim"
            status = st.selectbox("Status", ["Ativo", "Inativo"], index=0 if pessoa.status == "Ativo" else 1)
            tipo = st.selectbox("Tipo", ["Jovem", "Adolescente"], index=0 if pessoa.tipo == "Jovem" else 1)
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
                    st.rerun()
    else:
        st.error("Não encontrado.")

adicionar_pessoa()
exibir_pessoas()
