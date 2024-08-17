import streamlit as st
import torchaudio
import io
import os
import base64

# Função para carregar o arquivo de áudio
def carregar_audio(file_path):
    waveform, sample_rate = torchaudio.load(file_path)
    return waveform, sample_rate

# Função para aplicar time stretch
def aplicar_time_stretch(waveform, sample_rate, rate):
    transform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=int(sample_rate * rate))
    return transform(waveform)

# Função para obter a codificação base64 de um arquivo binário
@st.cache_data(show_spinner=False)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data=f.read()
    return base64.b64encode(data).decode()

# Função para definir a imagem de fundo da página
def set_jpeg_as_page_bg(jpeg_file):
    bin_str=get_base64_of_bin_file(jpeg_file)
    page_bg_img='''
    <style>
    .stApp {
    background-image: url("data:image/jpeg;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

# Conteúdo do aplicativo Streamlit
st.title("")
st.title("")
st.title("")
st.title("")
st.title("")
st.title("")

# Definir a imagem de fundo (substitua 'background.jpg' pelo caminho do seu arquivo JPEG)
set_jpeg_as_page_bg('C:/Users/kayap/PycharmProjects/Fretnut App/Fretnut.venv/fretnutapp.png')

# Função para listar arquivos WAV no diretório
def listar_arquivos_wav(diretorio):
    return [f for f in os.listdir(diretorio) if f.endswith('.wav')]

# Diretório contendo arquivos WAV
diretorio_audio = 'C:/Users/kayap/OneDrive/Documentos/FretNut App/bruno kayapy guitarra essencial'
arquivos_wav = listar_arquivos_wav(diretorio_audio)

# Manter estado atual da faixa
if 'indice_faixa' not in st.session_state:
    st.session_state.indice_faixa = 0

# Função para atualizar a faixa atual
def atualizar_faixa(indice):
    if 0 <= indice < len(arquivos_wav):
        st.session_state.indice_faixa = indice

# Conteúdo do aplicativo
st.markdown('<div class="player-container">', unsafe_allow_html=True)

# Exibir a faixa atual com texto branco
faixa_atual = arquivos_wav[st.session_state.indice_faixa]
st.markdown(f"<p style='color: white;'>Reproduzindo: {faixa_atual}</p>", unsafe_allow_html=True)

# Carregar e reproduzir a faixa atual
file_path = os.path.join(diretorio_audio, faixa_atual)
waveform, sample_rate = carregar_audio(file_path)
st.audio(file_path, format='audio/wav', start_time=0)

st.markdown('</div>', unsafe_allow_html=True)

# Navegação entre faixas (posicionar os botões no centro horizontalmente)
st.markdown('<div class="button-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("Faixa Anterior"):
        atualizar_faixa(st.session_state.indice_faixa - 1)
with col3:
    if st.button("Próxima Faixa"):
        atualizar_faixa(st.session_state.indice_faixa + 1)
st.markdown('</div>', unsafe_allow_html=True)
