import streamlit as st
from database import Evento, Presenca, Pessoa, Visitante, session
import pandas as pd
import datetime
from header import header_html, header_css

st.set_page_config(page_title="Eventos e Presença", page_icon="🔥", layout="wide")


# Gere o HTML e o CSS do cabeçalho
header_html_content = header_html()
header_css_content = header_css()

# Insira o CSS na página (antes do HTML)
st.markdown(f"<style>{header_css_content}</style>", unsafe_allow_html=True)

# Insira o cabeçalho na página
st.markdown(header_html_content, unsafe_allow_html=True)


st.header("📅 Eventos e Presença")


# Organização em abas
tab1, tab2, tab3 = st.tabs(["Criar Evento", "Registrar Presença", "Histórico de Eventos"])

def criar_evento():
    with tab1:
        st.subheader("Criar Novo Evento")
        with st.form("Criar Evento", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                nome_evento = st.text_input("Nome do Evento")
                tipo_evento = st.selectbox("Tipo do Evento", ["Jovens", "Adolescentes", "Ambos"])
            with col2:
                data_evento = st.date_input("Data do Evento", value=datetime.date.today())
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
                st.rerun()

def registrar_presenca():
    with tab2:
        st.subheader("Registrar Presença")

        # Selecionar eventos que ainda não tiveram presença registrada
        eventos_sem_presenca = session.query(Evento).filter(
            ~Evento.id.in_(session.query(Presenca.evento_id).distinct()),
            Evento.encerrado == False
        ).all()

        if not eventos_sem_presenca:
            st.info("Não há eventos disponíveis para registrar presenças.")
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

        st.subheader("Selecionar Presentes")
        presentes = st.multiselect(
            "Selecione os Presentes",
            pessoas,
            format_func=lambda x: x.nome
        )

        # Visitantes
        st.subheader("Adicionar Visitantes")
        num_visitantes = st.number_input("Número de Visitantes", min_value=0, step=1, key='num_visitantes')

        if num_visitantes > 0:
            visitantes = []
            for i in range(int(num_visitantes)):
                st.markdown(f"**Visitante {i+1}**")
                col1, col2, col3 = st.columns([3, 3, 4])
                with col1:
                    nome_visitante = st.text_input(f"Nome", key=f"nome_visitante_{i}")
                with col2:
                    telefone_visitante = st.text_input(f"Telefone", key=f"telefone_visitante_{i}")
                with col3:
                    convidado_por = st.selectbox(
                        f"Convidado por",
                        [None] + pessoas,
                        format_func=lambda x: x.nome if x else "Selecione",
                        key=f"convidado_por_{i}"
                    )
                    convidado_por_id = convidado_por.id if convidado_por else None

                visitantes.append({
                    'nome': nome_visitante,
                    'telefone': telefone_visitante,
                    'convidado_por_id': convidado_por_id
                })
        else:
            visitantes = []

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
    with tab3:
        st.subheader("Histórico de Eventos")

        with st.expander("Filtros"):
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
        ).order_by(Evento.data.desc()).all()

        if not eventos_filtrados:
            st.info("Nenhum evento encontrado para o período selecionado.")
            return

        # Apresentar os eventos filtrados em uma tabela
        df_eventos = pd.DataFrame([{
            'ID': evento.id,
            'Nome': evento.nome,
            'Data': evento.data.strftime('%d/%m/%Y'),
            'Tipo': evento.tipo
        } for evento in eventos_filtrados])

        # Exibir a tabela de eventos
        st.dataframe(df_eventos, use_container_width=True)

        # Criar opções de seleção com ID, Nome e Tipo
        eventos_opcoes = df_eventos.apply(lambda row: f"{row['ID']} - {row['Nome']} ({row['Tipo']})", axis=1)
        evento_selecionado_str = st.selectbox("Selecione um Evento para ver detalhes", eventos_opcoes)

        # Extrair o ID do evento selecionado
        evento_selecionado_id = int(evento_selecionado_str.split(' - ')[0])
        evento_selecionado = session.query(Evento).filter_by(id=evento_selecionado_id).first()

        if evento_selecionado:
            st.markdown(f"### {evento_selecionado.nome} - {evento_selecionado.data.strftime('%d/%m/%Y')} ({evento_selecionado.tipo})")
            # Calcular Resumo de Frequência para o Evento
            presencas = session.query(Presenca).filter_by(evento_id=evento_selecionado.id).all()
            presentes = sum(1 for p in presencas if p.presente)
            ausentes = sum(1 for p in presencas if not p.presente)
            visitantes_count = session.query(Visitante).filter_by(evento_id=evento_selecionado.id).count()
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
            data_presencas = []
            for presenca in presencas:
                pessoa = session.query(Pessoa).filter_by(id=presenca.pessoa_id).first()
                data_presencas.append({
                    'Nome': pessoa.nome,
                    'Tipo': pessoa.tipo,
                    'Presente': 'Sim' if presenca.presente else 'Não'
                })
            df_presencas = pd.DataFrame(data_presencas)
            st.dataframe(df_presencas, use_container_width=True)

            # Mostrar Visitantes do Evento
            visitantes_list = session.query(Visitante).filter_by(evento_id=evento_selecionado.id).all()
            if visitantes_list:
                st.markdown("#### Visitantes")
                data_visitantes = []
                for visitante in visitantes_list:
                    convidado_por = session.query(Pessoa).filter_by(id=visitante.convidado_por).first()
                    data_visitantes.append({
                        'Nome': visitante.nome,
                        'Telefone': visitante.telefone,
                        'Convidado por': convidado_por.nome if convidado_por else 'N/A'
                    })
                df_visitantes = pd.DataFrame(data_visitantes)
                st.dataframe(df_visitantes, use_container_width=True)

# Chamada das funções
criar_evento()
registrar_presenca()
historico_eventos()
