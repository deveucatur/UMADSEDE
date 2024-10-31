import streamlit as st
from database import Evento, Presenca, Pessoa, Visitante, session
import pandas as pd
import datetime

st.header("Eventos e Presença")

def criar_evento():
    st.subheader("Criar Novo Evento")
    with st.form("Criar Evento"):
        nome_evento = st.text_input("Nome do Evento")
        data_evento = st.date_input("Data do Evento", value=datetime.date.today())
        tipo_evento = st.selectbox("Tipo do Evento", ["Jovens", "Adolescentes", "Ambos"])
        submit = st.form_submit_button("Criar Evento")

        if submit:
            novo_evento = Evento(
                nome=nome_evento,
                data=data_evento,
                tipo=tipo_evento,
                encerrado=False
            )
            session.add(novo_evento)
            session.commit()
            st.success(f"Evento '{nome_evento}' criado com sucesso!")

def registrar_presenca():
    st.subheader("Registrar Presença")

    # Selecionar eventos que ainda não tiveram presença registrada
    eventos_sem_presenca = session.query(Evento).filter(
        ~Evento.id.in_(session.query(Presenca.evento_id).distinct()),
        Evento.encerrado == False
    ).all()

    if not eventos_sem_presenca:
        st.info("Não há eventos sem presença registrada.")
        return

    evento_selecionado = st.selectbox(
        "Selecione o Evento",
        eventos_sem_presenca,
        format_func=lambda x: f"{x.nome} - {x.data.strftime('%d/%m/%Y')} ({x.tipo})"
    )

    # Mapear o tipo de evento para o tipo de pessoa
    if evento_selecionado.tipo == "Ambos":
        pessoas = session.query(Pessoa).filter(Pessoa.status == "Ativo").all()
    else:
        tipo_evento = evento_selecionado.tipo
        if tipo_evento == 'Jovens':
            tipo_pessoa = 'Jovem'
        elif tipo_evento == 'Adolescentes':
            tipo_pessoa = 'Adolescente'
        else:
            tipo_pessoa = None

        if tipo_pessoa:
            pessoas = session.query(Pessoa).filter(
                Pessoa.status == "Ativo",
                Pessoa.tipo == tipo_pessoa
            ).all()
        else:
            pessoas = []

    if not pessoas:
        st.warning("Não há pessoas disponíveis para este tipo de evento.")
        return

    presentes = st.multiselect(
        "Selecione os Presentes",
        pessoas,
        format_func=lambda x: x.nome
    )

    # Visitantes
    st.subheader("Adicionar Visitantes")
    num_visitantes = st.number_input("Número de Visitantes", min_value=0, step=1)
    visitantes = []
    for i in range(int(num_visitantes)):
        with st.expander(f"Visitante {i+1}"):
            nome_visitante = st.text_input(f"Nome do Visitante {i+1}", key=f"nome_visitante_{i}")
            telefone_visitante = st.text_input(f"Telefone do Visitante {i+1}", key=f"telefone_visitante_{i}")

            if pessoas:
                convidado_por = st.selectbox(
                    f"Convidado por",
                    pessoas,
                    format_func=lambda x: x.nome,
                    key=f"convidado_por_{i}"
                )
                convidado_por_id = convidado_por.id
            else:
                st.warning("Não há pessoas disponíveis para selecionar como 'Convidado por'.")
                convidado_por_id = None

            visitantes.append({
                'nome': nome_visitante,
                'telefone': telefone_visitante,
                'convidado_por_id': convidado_por_id
            })

    if st.button("Registrar Presenças"):
        # Criar um conjunto de IDs dos presentes
        presentes_ids = {pessoa.id for pessoa in presentes}

        # Registrar presença dos presentes e ausentes
        for pessoa in pessoas:
            presente = pessoa.id in presentes_ids
            nova_presenca = Presenca(
                pessoa_id=pessoa.id,
                evento_id=evento_selecionado.id,
                presente=presente
            )
            session.add(nova_presenca)

        # Registrar visitantes
        for visitante_data in visitantes:
            novo_visitante = Visitante(
                nome=visitante_data['nome'],
                telefone=visitante_data['telefone'],
                convidado_por=visitante_data['convidado_por_id'],
                evento_id=evento_selecionado.id
            )
            session.add(novo_visitante)

        # Encerrar o evento para novos registros
        evento_selecionado.encerrado = True
        session.commit()
        st.success("Presenças registradas e evento encerrado com sucesso!")
        st.rerun()

def historico_eventos():
    st.subheader("Filtros de Histórico")

    # Filtro de Mês, Ano e Tipo de Evento
    mes_atual = datetime.datetime.now().month
    ano_atual = datetime.datetime.now().year

    col1, col2, col3 = st.columns(3)
    with col1:
        mes = st.selectbox(
            "Selecione o Mês",
            list(range(1, 13)),
            format_func=lambda x: datetime.date(1900, x, 1).strftime('%B'),
            index=mes_atual - 1
        )
    with col2:
        anos_disponiveis = [ano_atual, ano_atual - 1]
        ano = st.selectbox("Selecione o Ano", anos_disponiveis, index=0)
    with col3:
        tipo_filter = st.multiselect(
            "Tipo de Evento",
            ["Jovens", "Adolescentes", "Ambos"],
            default=["Jovens", "Adolescentes", "Ambos"]
        )

    # Filtrar eventos pelo mês, ano e tipo
    data_inicio = datetime.date(ano, mes, 1)
    if mes == 12:
        data_fim = datetime.date(ano + 1, 1, 1)
    else:
        data_fim = datetime.date(ano, mes + 1, 1)

    eventos_filtrados = session.query(Evento).filter(
        Evento.data >= data_inicio,
        Evento.data < data_fim,
        Evento.tipo.in_(tipo_filter)
    ).all()

    if not eventos_filtrados:
        st.info("Nenhum evento encontrado para o período selecionado.")
        return

    # Listar Eventos Filtrados
    for evento in eventos_filtrados:
        with st.expander(f"{evento.nome} - {evento.data.strftime('%d/%m/%Y')} ({evento.tipo})"):
            # Calcular Resumo de Frequência para o Evento
            presencas = session.query(Presenca).filter_by(evento_id=evento.id).all()
            presentes = sum(1 for p in presencas if p.presente)
            ausentes = sum(1 for p in presencas if not p.presente)
            visitantes_count = session.query(Visitante).filter_by(evento_id=evento.id).count()
            total_pessoas = presentes + ausentes

            # Calcular Percentual de Frequência
            if total_pessoas > 0:
                percentual_frequencia = (presentes / total_pessoas) * 100
            else:
                percentual_frequencia = 0

            # Exibir Resumo de Frequência
            st.markdown("#### Resumo de Frequência")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Presentes", presentes)
            col2.metric("Total Visitantes", visitantes_count)
            col3.metric("Total Ausentes", ausentes)
            col4.metric("Percentual de Frequência", f"{percentual_frequencia:.2f}%")

            # Listar Presenças para o Evento
            data = []
            for presenca in presencas:
                pessoa = session.query(Pessoa).filter_by(id=presenca.pessoa_id).first()
                data.append({
                    'Nome': pessoa.nome,
                    'Tipo': pessoa.tipo,
                    'Presente': 'Sim' if presenca.presente else 'Não'
                })
            df = pd.DataFrame(data)
            st.table(df)

            # Mostrar Visitantes do Evento
            visitantes_list = session.query(Visitante).filter_by(evento_id=evento.id).all()
            if visitantes_list:
                st.write("**Visitantes:**")
                data_visitantes = []
                for visitante in visitantes_list:
                    convidado_por = session.query(Pessoa).filter_by(id=visitante.convidado_por).first()
                    data_visitantes.append({
                        'Nome': visitante.nome,
                        'Telefone': visitante.telefone,
                        'Convidado por': convidado_por.nome if convidado_por else 'N/A'
                    })
                df_visitantes = pd.DataFrame(data_visitantes)
                st.table(df_visitantes)

# Chamada das funções
criar_evento()
registrar_presenca()
historico_eventos()
