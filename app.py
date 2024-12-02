import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

clubs_df = pd.read_csv('datasets/clubs.csv')
players_df = pd.read_csv('datasets/players.csv')
games_events_df = pd.read_csv('datasets/game_events.csv')
appearances_df = pd.read_csv('datasets/appearances.csv')
competitions_df = pd.read_csv('datasets/competitions.csv')

## Id do vinicius Junior
vinicius_linha = players_df.name.apply(lambda name: name == 'Vinicius Junior')
id_vinicius = players_df[vinicius_linha]['player_id'].values[0]
players_df_vini = players_df[players_df['player_id'] == id_vinicius]

## Id do Rodri
rodri_linha = (players_df['name'] == 'Rodri') & (players_df['last_season'] == 2024)
id_rodri = players_df[rodri_linha]['player_id'].values[0]
players_df_rodri = players_df[players_df['player_id'] == id_rodri]

#Temporada 23-24
start_date = '2023-08-01'
end_date = '2024-07-31'


# Filtrar os eventos de Vinícius Jr. dentro desse intervalo de tempo
events_vinijr = games_events_df[(games_events_df["player_id"] == id_vinicius) &
                                (games_events_df["date"] >= start_date) &
                                (games_events_df["date"] <= end_date)]

# Filtrar os eventos de Rodri dentro desse intervalo de tempo
events_rodri = games_events_df[(games_events_df["player_id"] == id_rodri) &
                                (games_events_df["date"] >= start_date) &
                                (games_events_df["date"] <= end_date)]


# Filtra as participações do Vinicius Junior no intervalo de datas definido
appearances_vini = appearances_df[(appearances_df["player_id"] == id_vinicius) &
                                  (appearances_df["date"] >= start_date) &
                                  (appearances_df["date"] <= end_date)]
# Filtra as participações do Rodri no mesmo intervalo de datas
appearances_rodri = appearances_df[(appearances_df["player_id"] == id_rodri) &
                                   (appearances_df["date"] >= start_date) &
                                   (appearances_df["date"] <= end_date)]

# Calcula o total de gols marcados pelo Vinicius Junior e Rodri no intervalo de datas
gols_vini = appearances_vini['goals'].sum()
gols_rodri = appearances_rodri['goals'].sum()

# Calcula as assistências de Vinicius Jr. e Rodri
assists_vini = appearances_vini['assists'].sum()
assists_rodri = appearances_rodri['assists'].sum()

# Calcula a soma de gols e assistências para determinar a participação em gols
participacao_gol_vini = gols_vini + assists_vini
participacao_gol_rodri = gols_rodri + assists_rodri

linha_assists = pd.DataFrame({
    'player_id': ['Rodri', 'Vinicius Junior'],  # Jogadores
    'type': ['Assists', 'Assists'],            # Tipo de evento
    'count': [assists_rodri, assists_vini]     # Contagem de assistências
})

# Concatena os DataFrames de eventos de Rodri e Vinicius Jr.
events_rodri_vinijr = pd.concat([events_rodri, events_vinijr])

# Agrupa os eventos por jogador e tipo, contando ocorrências
events_rodri_vinijr = events_rodri_vinijr.groupby(['player_id', 'type']).size().reset_index(name='count')

# Adiciona as assistências ao DataFrame consolidado
events_rodri_vinijr = pd.concat([events_rodri_vinijr, linha_assists], ignore_index=True)

# Substitui IDs numéricos pelos nomes dos jogadores
events_rodri_vinijr['player_id'] = events_rodri_vinijr['player_id'].replace({357565: 'Rodri', 371998: 'Vinicius Junior'})
events_rodri_vinijr['player_id'] = events_rodri_vinijr['player_id'].astype(str)

# Ordena o DataFrame por jogador para facilitar a visualização
events_rodri_vinijr = events_rodri_vinijr.sort_values(by='player_id').reset_index(drop=True)

# Exibe as primeiras 20 linhas do DataFrame
events_rodri_vinijr.head(20)

# Filtrar os dados de cada jogador
linhas_vini = events_rodri_vinijr[events_rodri_vinijr.player_id == 'Vinicius Junior']
linhas_rodri = events_rodri_vinijr[events_rodri_vinijr.player_id == 'Rodri']

# Excluir a métrica "Shootout" de Rodri
linhas_rodri = linhas_rodri[linhas_rodri["type"] != "Shootout"]

# Garantir que as métricas estão na mesma ordem para ambos os jogadores
linhas_vini = linhas_vini.set_index("type")
linhas_rodri = linhas_rodri.set_index("type")

# Listas de contagem para as barras
vini_counts = linhas_vini["count"]
rodri_counts = linhas_rodri["count"]

x = range(len(vini_counts))  # Base para o eixo x
width = 0.4

temp_23_24, ax = plt.subplots(figsize=(10, 6))
ax.bar([pos - width/2 for pos in x], vini_counts, width=width, label="Vinicius Junior", color="blue")
ax.bar([pos + width/2 for pos in x], rodri_counts, width=width, label="Rodri", color="green")

# Configurações do gráfico
ax.set_xlabel("Tipos de Métricas")
ax.set_ylabel("Quantidade")
ax.set_title("Comparação de Estatísticas: Vinicius Junior vs Rodri")
ax.set_xticks(ticks=x, labels=vini_counts.index, rotation=45)  # Rótulos no eixo X
ax.legend()
plt.tight_layout()

st.title("Bola de Ouro 23-24. Vinicius Júnior ou Rodri?")
st.write("Aqui iremos tentar mostrar, com as estatísticas, que o Vinicíus Júnior mereceu a bola de ouro, no lugar do Rodri.")

st.subheader("Gráfico de Comparação: Vinicius Junior vs Rodri, na temporada 23-24")
st.pyplot(temp_23_24)
st.write("Aqui vemos que o Vinícius foi superior em Gols e Rodri foi superior nas assistências.")
st.write("Vinícius Júnior foi mais substituido do que o Rodri, o que pode nos dizer que talvez o vinícius seja mais irregular durante as partidas, do que o Rodri. Porém, pode ter outros significados, o Real Madrid tem um plantel ofensivo muito forte, logo uma substituição pode não estar diretamente relacionada à má desempenho.")