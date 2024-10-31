import streamlit as st
from database import Pessoa, Presenca, Evento, Visitante, session
import pandas as pd
import datetime
from sqlalchemy import func
import plotly.express as px

# Configurações iniciais
st.set_page_config(
    page_title="UMADSEDE - Home",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Aplicando um tema personalizado com CSS
def add_custom_css():
    st.markdown("""
        <style>
            /* Estilos gerais */
            body {
                background-color: #f0f2f6;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            /* Cabeçalhos */
            .main-header {
                font-size: 2.5rem;
                color: #1f4e79;
                font-weight: bold;
                margin-bottom: 1rem;
            }
            .sub-header {
                font-size: 1.75rem;
                color: #1f4e79;
                font-weight: bold;
                margin-top: 2rem;
                margin-bottom: 1rem;
            }
            /* Métricas */
            .metric-container {
                background-color: #ffffff;
                padding: 1rem;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            .metric-label {
                font-size: 1.1rem;
                color: #666666;
            }
            .metric-value {
                font-size: 2rem;
                font-weight: bold;
                color: #1f4e79;
            }
            /* Rodapé */
            .footer {
                text-align: center;
                color: #666666;
                margin-top: 2rem;
                font-size: 0.9rem;
            }
            /* Remover o menu de hambúrguer e o rodapé do Streamlit */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

add_custom_css()

# Cabeçalho Principal
st.markdown('<h1 class="main-header">UMADSEDE - União da Mocidade e Adolescentes da Sede</h1>', unsafe_allow_html=True)

# Seções de Propósito e Visão
st.markdown('<h2 class="sub-header">Propósito e Visão</h2>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <p style="font-size: 1.1rem; color: #333333;">
            <strong>Propósito:</strong><br>
            Unir e fortalecer os jovens e adolescentes na fé, promovendo crescimento espiritual, comunhão e serviço à comunidade.
        </p>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
        <p style="font-size: 1.1rem; color: #333333;">
            <strong>Visão a Longo Prazo:</strong><br>
            Ser uma geração comprometida com os princípios cristãos, impactando positivamente a sociedade através do amor, respeito e dedicação ao próximo.
        </p>
    """, unsafe_allow_html=True)

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

# Dados Globais
st.markdown('<h2 class="sub-header">Dados Globais</h2>', unsafe_allow_html=True)
total_pessoas = session.query(Pessoa).count()
total_jovens = session.query(Pessoa).filter(Pessoa.tipo == "Jovem", Pessoa.status == "Ativo").count()
total_adolescentes = session.query(Pessoa).filter(Pessoa.tipo == "Adolescente", Pessoa.status == "Ativo").count()
total_batizados_aguas = session.query(Pessoa).filter(Pessoa.batizado_aguas == True, Pessoa.status == "Ativo").count()
total_batizados_espirito = session.query(Pessoa).filter(Pessoa.batizado_espirito == True, Pessoa.status == "Ativo").count()

# Exibir métricas globais
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown("""
        <div class="metric-container">
            <div class="metric-label">Total de Pessoas</div>
            <div class="metric-value">{}</div>
        </div>
    """.format(total_pessoas), unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class="metric-container">
            <div class="metric-label">Total de Jovens</div>
            <div class="metric-value">{}</div>
        </div>
    """.format(total_jovens), unsafe_allow_html=True)
with col3:
    st.markdown("""
        <div class="metric-container">
            <div class="metric-label">Total de Adolescentes</div>
            <div class="metric-value">{}</div>
        </div>
    """.format(total_adolescentes), unsafe_allow_html=True)
with col4:
    st.markdown("""
        <div class="metric-container">
            <div class="metric-label">Batizados nas Águas</div>
            <div class="metric-value">{}</div>
        </div>
    """.format(total_batizados_aguas), unsafe_allow_html=True)
with col5:
    st.markdown("""
        <div class="metric-container">
            <div class="metric-label">Batizados no Espírito Santo</div>
            <div class="metric-value">{}</div>
        </div>
    """.format(total_batizados_espirito), unsafe_allow_html=True)

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

# Seção de Resumo Semanal
st.markdown('<h2 class="sub-header">Resumo Semanal</h2>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown('<h3>Aniversariantes da Semana</h3>', unsafe_allow_html=True)
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

with col2:
    st.markdown('<h3>Eventos desta Semana</h3>', unsafe_allow_html=True)
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

# Filtros do Dashboard
st.markdown('<h3>Filtros</h3>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    mes_atual = datetime.datetime.now().month
    mes = st.selectbox(
        "Mês",
        list(range(1, 13)),
        format_func=lambda x: datetime.date(1900, x, 1).strftime('%B'),
        index=mes_atual - 1
    )
with col2:
    ano_atual = datetime.datetime.now().year
    anos_disponiveis = [ano_atual, ano_atual - 1]
    ano = st.selectbox("Ano", anos_disponiveis, index=0)
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

# Percentual Médio de Presença
total_pessoas_ativas = session.query(Pessoa).filter(Pessoa.status == "Ativo").count()
percentual_presenca = (media_presencas / total_pessoas_ativas) * 100 if total_pessoas_ativas > 0 else 0

# Exibir Métricas do Mês
st.markdown('<h3>Métricas do Mês</h3>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("""
        <div class="metric-container">
            <div class="metric-label">Eventos no Mês</div>
            <div class="metric-value">{}</div>
        </div>
    """.format(total_eventos), unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class="metric-container">
            <div class="metric-label">Presença Média</div>
            <div class="metric-value">{:.1f}</div>
        </div>
    """.format(media_presencas), unsafe_allow_html=True)
with col3:
    st.markdown("""
        <div class="metric-container">
            <div class="metric-label">Visitantes no Mês</div>
            <div class="metric-value">{}</div>
        </div>
    """.format(visitantes_mes), unsafe_allow_html=True)
with col4:
    st.markdown("""
        <div class="metric-container">
            <div class="metric-label">Percentual Médio de Presença</div>
            <div class="metric-value">{:.2f}%</div>
        </div>
    """.format(percentual_presenca), unsafe_allow_html=True)

# Gráficos
st.markdown('<h3>Gráficos</h3>', unsafe_allow_html=True)

# Gráfico de Batizados nas Águas e no Espírito Santo
st.markdown('<h4>Distribuição de Batizados</h4>', unsafe_allow_html=True)
batizados_data = {
    'Categoria': ['Batizados nas Águas', 'Batizados no Espírito Santo', 'Não Batizados'],
    'Quantidade': [
        total_batizados_aguas,
        total_batizados_espirito,
        total_pessoas - (total_batizados_aguas + total_batizados_espirito)
    ]
}
df_batizados = pd.DataFrame(batizados_data)
fig_batizados = px.pie(
    df_batizados,
    names='Categoria',
    values='Quantidade',
    color='Categoria',
    color_discrete_map={
        'Batizados nas Águas': '#1f77b4',
        'Batizados no Espírito Santo': '#2ca02c',
        'Não Batizados': '#d62728'
    },
    title='Distribuição de Batizados entre os Participantes'
)
st.plotly_chart(fig_batizados, use_container_width=True)

# Gráfico de Presenças por Evento
st.markdown('<h4>Presenças por Evento</h4>', unsafe_allow_html=True)
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
    df_presencas_melted = df_presencas.melt(id_vars='Evento', value_vars=['Presentes', 'Ausentes'], var_name='Status', value_name='Quantidade')
    fig_presencas = px.bar(
        df_presencas_melted,
        x='Evento',
        y='Quantidade',
        color='Status',
        barmode='stack',
        title='Presenças e Ausências por Evento',
        color_discrete_map={'Presentes': '#2ca02c', 'Ausentes': '#d62728'}
    )
    fig_presencas.update_xaxes(tickangle=-45)
    st.plotly_chart(fig_presencas, use_container_width=True)
else:
    st.info("Não há dados de presenças para o período selecionado.")

# Gráfico de Distribuição por Tipo
st.markdown('<h4>Distribuição por Tipo</h4>', unsafe_allow_html=True)
tipo_data = {
    'Tipo': ['Jovens', 'Adolescentes'],
    'Quantidade': [total_jovens, total_adolescentes]
}
df_tipo = pd.DataFrame(tipo_data)
fig_tipo = px.pie(
    df_tipo,
    names='Tipo',
    values='Quantidade',
    title='Distribuição de Jovens e Adolescentes'
)
st.plotly_chart(fig_tipo, use_container_width=True)

# Gráfico de Status (Ativo/Inativo)
st.markdown('<h4>Status dos Participantes</h4>', unsafe_allow_html=True)
status_counts = session.query(Pessoa.status, func.count(Pessoa.id)).group_by(Pessoa.status).all()
status_data = {
    'Status': [status for status, count in status_counts],
    'Quantidade': [count for status, count in status_counts]
}
df_status = pd.DataFrame(status_data)
fig_status = px.pie(
    df_status,
    names='Status',
    values='Quantidade',
    title='Status dos Participantes'
)
st.plotly_chart(fig_status, use_container_width=True)

# Rodapé
st.markdown('<div class="footer">💒 Igreja Assembleia de Deus - Ministério de Jovens e Adolescentes UMADSEDE</div>', unsafe_allow_html=True)
