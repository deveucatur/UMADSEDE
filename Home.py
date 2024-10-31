import streamlit as st
from database import Pessoa, Presenca, Evento, Visitante, session
import pandas as pd
import datetime
from sqlalchemy import func
import plotly.express as px
import plotly.graph_objects as go

# Configurações iniciais
st.set_page_config(
    page_title="UMADSEDE - Home",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Aplicando um tema personalizado
st.markdown("""
    <style>
        /* Estilos gerais */
        body {
            background-color: #f5f5f5;
        }
        .main-header {
            font-size: 2.5rem;
            color: #003366;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #003366;
            font-weight: bold;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
        /* Estilos para os cartões de métricas */
        .metric-card {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        }
        /* Estilos para os gráficos */
        .chart-container {
            background-color: #ffffff;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        /* Estilos para o rodapé */
        .footer {
            text-align: center;
            color: #666666;
            margin-top: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho Principal
st.markdown('<h1 class="main-header">UMADSEDE - União da Mocidade e Adolescentes da Sede</h1>', unsafe_allow_html=True)

# Seções de Propósito e Visão
st.markdown('<h2 class="sub-header">Propósito e Visão</h2>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        ### Propósito
        Nosso propósito é unir e fortalecer os jovens e adolescentes na fé, promovendo crescimento espiritual, comunhão e serviço à comunidade.
    """)
with col2:
    st.markdown("""
        ### Visão a Longo Prazo
        Ser uma geração comprometida com os princípios cristãos, impactando positivamente a sociedade através do amor, respeito e dedicação ao próximo.
    """)

# Seção de Eventos
st.markdown('<h2 class="sub-header">Eventos</h2>', unsafe_allow_html=True)
events = [
    {
        "nome": "Culto de Sábado",
        "descricao": "Um momento especial de adoração, louvor e comunhão entre os jovens e adolescentes."
    },
    {
        "nome": "Confra UMADSEDE",
        "descricao": "Uma conferência anual que reúne jovens e adolescentes para momentos de aprendizado e celebração."
    },
    {
        "nome": "Festa da UMADSEDE",
        "descricao": "Um evento festivo com atividades, música e integração para fortalecer os laços entre os participantes."
    }
]

for event in events:
    with st.expander(f"📅 {event['nome']}"):
        st.write(event["descricao"])

# Dados do Sistema
st.markdown('<h2 class="sub-header">Detalhamento</h2>', unsafe_allow_html=True)

# Número total de pessoas
total_pessoas = session.query(Pessoa).count()

# Número de Jovens e Adolescentes
total_jovens = session.query(Pessoa).filter(Pessoa.tipo == "Jovem", Pessoa.status == "Ativo").count()
total_adolescentes = session.query(Pessoa).filter(Pessoa.tipo == "Adolescente", Pessoa.status == "Ativo").count()

# Aniversariantes da semana
hoje = datetime.date.today()
dia_semana = hoje.weekday()  # 0 é segunda-feira
inicio_semana = hoje - datetime.timedelta(days=dia_semana)
fim_semana = inicio_semana + datetime.timedelta(days=6)

aniversariantes_semana = session.query(Pessoa).filter(
    func.strftime("%m-%d", Pessoa.data_nascimento) >= inicio_semana.strftime("%m-%d"),
    func.strftime("%m-%d", Pessoa.data_nascimento) <= fim_semana.strftime("%m-%d"),
    Pessoa.status == "Ativo"
).all()

# Eventos da semana
eventos_semana = session.query(Evento).filter(
    Evento.data >= inicio_semana,
    Evento.data <= fim_semana
).all()

# Exibir métricas
st.markdown('<h2 class="sub-header">Resumo Semanal</h2>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Total de Pessoas", total_pessoas)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Total de Jovens", total_jovens)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Total de Adolescentes", total_adolescentes)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Eventos nesta Semana", len(eventos_semana))
    st.markdown('</div>', unsafe_allow_html=True)

# Listar aniversariantes
st.markdown('<h2 class="sub-header">🎂 Aniversariantes da Semana</h2>', unsafe_allow_html=True)
if aniversariantes_semana:
    aniversariantes_data = [{
        'Nome': pessoa.nome,
        'Tipo': pessoa.tipo,
        'Data de Nascimento': pessoa.data_nascimento.strftime('%d/%m')
    } for pessoa in aniversariantes_semana]
    df_aniversariantes = pd.DataFrame(aniversariantes_data)
    st.table(df_aniversariantes)
else:
    st.write("Nenhum aniversariante nesta semana.")

# Listar eventos da semana
st.markdown('<h2 class="sub-header">📆 Eventos desta Semana</h2>', unsafe_allow_html=True)
if eventos_semana:
    eventos_data = [{
        'Nome': evento.nome,
        'Data': evento.data.strftime('%d/%m/%Y'),
        'Tipo': evento.tipo
    } for evento in eventos_semana]
    df_eventos_semana = pd.DataFrame(eventos_data)
    st.table(df_eventos_semana)
else:
    st.write("Nenhum evento nesta semana.")

st.write("---")

## DASHBOARD ##
st.markdown('<h2 class="sub-header">📊 Dashboard</h2>', unsafe_allow_html=True)

# Obter o mês e ano atuais
mes_atual = datetime.datetime.now().month
ano_atual = datetime.datetime.now().year

st.subheader("Filtros")
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
    ano = st.selectbox(
        "Selecione o Ano",
        anos_disponiveis,
        index=0
    )
with col3:
    tipo_evento_filter = st.multiselect(
        "Tipo de Evento",
        ["Jovens", "Adolescentes", "Ambos"],
        default=["Jovens", "Adolescentes", "Ambos"]
    )

# Data inicial e final do filtro
data_inicio = datetime.date(ano, mes, 1)
if mes == 12:
    data_fim = datetime.date(ano + 1, 1, 1)
else:
    data_fim = datetime.date(ano, mes + 1, 1)

# Dados Filtrados
eventos_filtrados = session.query(Evento).filter(
    Evento.data >= data_inicio,
    Evento.data < data_fim,
    Evento.tipo.in_(tipo_evento_filter)
).all()
eventos_ids = [evento.id for evento in eventos_filtrados]

presencas_filtradas = session.query(Presenca).filter(Presenca.evento_id.in_(eventos_ids)).all()

# Total de Eventos no Mês
total_eventos = len(eventos_filtrados)

# Presença Média no Mês
if total_eventos > 0:
    presencas_totais = sum(1 for p in presencas_filtradas if p.presente)
    media_presencas = presencas_totais / total_eventos
else:
    media_presencas = 0

# Visitantes no Mês
visitantes_mes = session.query(Visitante).filter(Visitante.evento_id.in_(eventos_ids)).count()

# Métricas do Dashboard
st.markdown('<h2 class="sub-header">Métricas do Mês</h2>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Eventos no Mês", total_eventos)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Presença Média por Evento", f"{media_presencas:.1f}")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Visitantes no Mês", visitantes_mes)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    percentual_presenca = (media_presencas / (total_jovens + total_adolescentes)) * 100 if (total_jovens + total_adolescentes) > 0 else 0
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Percentual Médio de Presença", f"{percentual_presenca:.2f}%")
    st.markdown('</div>', unsafe_allow_html=True)

# Gráfico de Presenças por Evento
st.markdown('<h2 class="sub-header">Presenças por Evento</h2>', unsafe_allow_html=True)
dados_presencas = []
for evento in eventos_filtrados:
    presencas_evento = session.query(Presenca).filter_by(evento_id=evento.id).all()
    total_presentes = sum(1 for p in presencas_evento if p.presente)
    total_ausentes = sum(1 for p in presencas_evento if not p.presente)
    dados_presencas.append({
        'Evento': f"{evento.nome} ({evento.data.strftime('%d/%m')}) - {evento.tipo}",
        'Presentes': total_presentes,
        'Ausentes': total_ausentes
    })

df_presencas = pd.DataFrame(dados_presencas)

if not df_presencas.empty:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_presencas['Evento'],
        y=df_presencas['Presentes'],
        name='Presentes',
        marker_color='green'
    ))
    fig.add_trace(go.Bar(
        x=df_presencas['Evento'],
        y=df_presencas['Ausentes'],
        name='Ausentes',
        marker_color='red'
    ))
    fig.update_layout(
        barmode='stack',
        xaxis_tickangle=-45,
        title='Presenças e Ausências por Evento',
        xaxis_title='Evento',
        yaxis_title='Quantidade',
        legend_title='Status'
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Não há dados de presenças para o período selecionado.")

# Gráfico de Frequência por Pessoa
st.markdown('<h2 class="sub-header">Frequência no Mês por Pessoa</h2>', unsafe_allow_html=True)
frequencia = {}
for presenca in presencas_filtradas:
    if presenca.pessoa_id not in frequencia:
        frequencia[presenca.pessoa_id] = {'Nome': '', 'Tipo': '', 'Presenças': 0, 'Ausências': 0}
    pessoa = session.query(Pessoa).filter_by(id=presenca.pessoa_id).first()
    frequencia[presenca.pessoa_id]['Nome'] = pessoa.nome
    frequencia[presenca.pessoa_id]['Tipo'] = pessoa.tipo
    if presenca.presente:
        frequencia[presenca.pessoa_id]['Presenças'] += 1
    else:
        frequencia[presenca.pessoa_id]['Ausências'] += 1

dados_frequencia = list(frequencia.values())
df_frequencia = pd.DataFrame(dados_frequencia)

if not df_frequencia.empty:
    df_frequencia = df_frequencia.sort_values('Presenças', ascending=False)
    fig = px.bar(
        df_frequencia,
        x='Nome',
        y='Presenças',
        color='Tipo',
        title='Frequência de Presença por Pessoa',
        labels={'Presenças': 'Quantidade de Presenças'},
        hover_data=['Ausências']
    )
    fig.update_xaxes(tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Não há dados de frequência para o período selecionado.")

# Gráfico de Visitantes por Evento
st.markdown('<h2 class="sub-header">Visitantes por Evento</h2>', unsafe_allow_html=True)
dados_visitantes = []
for evento in eventos_filtrados:
    visitantes_evento = session.query(Visitante).filter_by(evento_id=evento.id).count()
    dados_visitantes.append({
        'Evento': f"{evento.nome} ({evento.data.strftime('%d/%m')}) - {evento.tipo}",
        'Visitantes': visitantes_evento
    })

df_visitantes = pd.DataFrame(dados_visitantes)

if not df_visitantes.empty:
    fig = px.bar(
        df_visitantes,
        x='Evento',
        y='Visitantes',
        title='Número de Visitantes por Evento',
        labels={'Visitantes': 'Quantidade'}
    )
    fig.update_xaxes(tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Não há dados de visitantes para o período selecionado.")

# Rodapé
st.markdown('<div class="footer">💒 Igreja Assembleia de Deus - Ministério de Jovens e Adolescentes UMADSEDE</div>', unsafe_allow_html=True)
