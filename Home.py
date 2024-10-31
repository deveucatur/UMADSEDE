import streamlit as st
from database import Pessoa, Presenca, Evento, Visitante, session
import pandas as pd
import datetime
from sqlalchemy import func
import plotly.express as px
from header import header_html, header_css

# Configurações iniciais
st.set_page_config(
    page_title="UMADSEDE - Home",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Defina o nome da página atual
page_name = "Home"

# Gere o HTML e o CSS do cabeçalho
header_html_content = header_html(page_name)
header_css_content = header_css()

# Insira o CSS na página (antes do HTML)
st.markdown(f"<style>{header_css_content}</style>", unsafe_allow_html=True)

# Insira o cabeçalho na página
st.markdown(header_html_content, unsafe_allow_html=True)




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
                color: #FF7F00;  /* Laranja */
                font-weight: bold;
                margin-bottom: 1rem;
            }
            .sub-header {
                font-size: 1.75rem;
                color: #FF7F00;  /* Laranja */
                font-weight: bold;
                margin-top: 2rem;
                margin-bottom: 1rem;
            }
            /* Métricas */
            .metric-container {
                background-color: #FFF9C4;  /* Amarelo Claro */
                padding: 1rem;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                text-align: center;
                margin-bottom: 1rem;
            }
            .metric-label {
                font-size: 1.1rem;
                color: #666666;
            }
            .metric-value {
                font-size: 2rem;
                font-weight: bold;
                color: #FF7F00;  /* Laranja */
            }
            /* Rodapé */
            .footer {
                text-align: center;
                color: #666666;
                margin-top: 2rem;
                font-size: 0.9rem;
            }
            /* Cartões */
            .card {
                background-color: #ffffff;
                padding: 1rem;
                border-radius: 8px;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
                margin-bottom: 1rem;
            }
            .card-title {
                font-size: 1.2rem;
                font-weight: bold;
                color: #333333;
            }
            .card-content {
                font-size: 1rem;
                color: #666666;
            }
            /* Remover o menu de hambúrguer e o rodapé do Streamlit */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

add_custom_css()

# Cabeçalho Principal
st.markdown('<h1 class="main-header">UMADSEDE - União da Mocidade e Adolescentes da Sede</h1>', unsafe_allow_html=True)

# Seção de Eventos
#st.markdown('<h2 class="sub-header">Eventos</h2>', unsafe_allow_html=True)
#events = [
#    {
#        "nome": "Culto de Sábado",
#        "descricao": "Um momento especial de adoração, louvor e comunhão entre os jovens e adolescentes."
#    },
#    {
#        "nome": "Confra UMADSEDE",
#        "descricao": "Uma conferência anual que reúne jovens e adolescentes para momentos de aprendizado e celebração."
#    },
#    {
#        "nome": "Festa da UMADSEDE",
#        "descricao": "Um evento festivo com atividades, música e integração para fortalecer os laços entre os participantes."
#    }
#]
#
#for event in events:
#    with st.expander(f"📅 {event['nome']}"):
 #       st.write(event["descricao"])

# Dados Globais
total_pessoas = session.query(Pessoa).count()
total_jovens = session.query(Pessoa).filter(Pessoa.tipo == "Jovem", Pessoa.status == "Ativo").count()
total_adolescentes = session.query(Pessoa).filter(Pessoa.tipo == "Adolescente", Pessoa.status == "Ativo").count()
total_batizados_aguas = session.query(Pessoa).filter(Pessoa.batizado_aguas == True, Pessoa.status == "Ativo").count()
total_nao_batizados_aguas = session.query(Pessoa).filter(Pessoa.batizado_aguas == False, Pessoa.status == "Ativo").count()
total_batizados_espirito = session.query(Pessoa).filter(Pessoa.batizado_espirito == True, Pessoa.status == "Ativo").count()
total_nao_batizados_espirito = session.query(Pessoa).filter(Pessoa.batizado_espirito == False, Pessoa.status == "Ativo").count()

# Exibir métricas globais
st.markdown('<h3>Métricas Globais</h3>', unsafe_allow_html=True)

# Organizar métricas em duas linhas para melhor responsividade
col1, col2, col3 = st.columns(3)
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

col4, col5 = st.columns(2)
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
        for pessoa in aniversariantes_semana:
            st.markdown(f"""
                <div class="card">
                    <div class="card-title">{pessoa.nome}</div>
                    <div class="card-content">
                        <strong>Tipo:</strong> {pessoa.tipo}<br>
                        <strong>Data de Nascimento:</strong> {pessoa.data_nascimento.strftime('%d/%m')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.write("Nenhum aniversariante nesta semana.")

with col2:
    st.markdown('<h3>Eventos desta Semana</h3>', unsafe_allow_html=True)
    if eventos_semana:
        for evento in eventos_semana:
            st.markdown(f"""
                <div class="card">
                    <div class="card-title">{evento.nome}</div>
                    <div class="card-content">
                        <strong>Data:</strong> {evento.data.strftime('%d/%m/%Y')}<br>
                        <strong>Tipo:</strong> {evento.tipo}
                    </div>
                </div>
            """, unsafe_allow_html=True)
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
col1, col2 = st.columns(2)
with col1:
    st.markdown("""
        <div class="metric-container">
            <div class="metric-label">Eventos no Mês</div>
            <div class="metric-value">{}</div>
        </div>
    """.format(total_eventos), unsafe_allow_html=True)
    st.markdown("""
        <div class="metric-container">
            <div class="metric-label">Visitantes no Mês</div>
            <div class="metric-value">{}</div>
        </div>
    """.format(visitantes_mes), unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div class="metric-container">
            <div class="metric-label">Presença Média</div>
            <div class="metric-value">{:.1f}</div>
        </div>
    """.format(media_presencas), unsafe_allow_html=True)
    st.markdown("""
        <div class="metric-container">
            <div class="metric-label">Percentual Médio de Presença</div>
            <div class="metric-value">{:.2f}%</div>
        </div>
    """.format(percentual_presenca), unsafe_allow_html=True)

# Gráficos
st.markdown('<h3>Gráficos</h3>', unsafe_allow_html=True)

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
	
# Gráfico de Frequência por Pessoa
st.markdown('<h4>Frequência por Pessoa</h4>', unsafe_allow_html=True)
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
    fig_frequencia = px.bar(
        df_frequencia,
        x='Nome',
        y='Presenças',
        color='Tipo',
        title='Frequência de Presença por Pessoa',
        labels={'Presenças': 'Quantidade de Presenças'},
        hover_data=['Ausências']
    )
    fig_frequencia.update_xaxes(tickangle=-45)
    st.plotly_chart(fig_frequencia, use_container_width=True)
else:
    st.info("Não há dados de frequência para o período selecionado.")

# Gráfico de Visitantes por Semana
st.markdown('<h4>Visitantes por Semana</h4>', unsafe_allow_html=True)
visitantes_por_semana = session.query(
    func.strftime("%W", Evento.data).label("semana"),
    func.count(Visitante.id)
).join(Evento, Visitante.evento_id == Evento.id).filter(
    Evento.data >= data_inicio,
    Evento.data < data_fim,
    Evento.tipo.in_(tipo_evento_filter)
).group_by("semana").all()

if visitantes_por_semana:
    df_visitantes_semana = pd.DataFrame(visitantes_por_semana, columns=['Semana', 'Visitantes'])
    df_visitantes_semana['Semana'] = df_visitantes_semana['Semana'].astype(int)
    df_visitantes_semana = df_visitantes_semana.sort_values('Semana')
    fig_visitantes_semana = px.line(
        df_visitantes_semana,
        x='Semana',
        y='Visitantes',
        markers=True,
        title='Visitantes por Semana'
    )
    st.plotly_chart(fig_visitantes_semana, use_container_width=True)
else:
    st.info("Não há dados de visitantes para o período selecionado.")
    

# Gráficos de Pizza Lado a Lado
st.markdown('<h4>Distribuições de Batismos</h4>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    # Gráfico de Batizados nas Águas
    batizados_aguas_data = {
        'Batizado nas Águas': ['Sim', 'Não'],
        'Quantidade': [total_batizados_aguas, total_nao_batizados_aguas]
    }
    df_batizados_aguas = pd.DataFrame(batizados_aguas_data)
    fig_batizados_aguas = px.pie(
        df_batizados_aguas,
        names='Batizado nas Águas',
        values='Quantidade',
        title='Batizados nas Águas'
    )
    st.plotly_chart(fig_batizados_aguas, use_container_width=True)

with col2:
    # Gráfico de Batizados no Espírito Santo
    batizados_espirito_data = {
        'Batizado no Espírito Santo': ['Sim', 'Não'],
        'Quantidade': [total_batizados_espirito, total_nao_batizados_espirito]
    }
    df_batizados_espirito = pd.DataFrame(batizados_espirito_data)
    fig_batizados_espirito = px.pie(
        df_batizados_espirito,
        names='Batizado no Espírito Santo',
        values='Quantidade',
        title='Batizados no Espírito Santo'
    )
    st.plotly_chart(fig_batizados_espirito, use_container_width=True)

# Outra linha de gráficos de pizza
col3, col4 = st.columns(2)

with col3:
	# Gráfico de Distribuição por Tipo
    tipo_data = {
        'Tipo': ['Jovens', 'Adolescentes'],
        'Quantidade': [total_jovens, total_adolescentes]
    }
    df_tipo = pd.DataFrame(tipo_data)
    fig_tipo = px.pie(
        df_tipo,
        names='Tipo',
        values='Quantidade',
        title='Distribuição por Tipo'
    )
    st.plotly_chart(fig_tipo, use_container_width=True)


with col4:
    # Gráfico de Status (Ativo/Inativo)
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
