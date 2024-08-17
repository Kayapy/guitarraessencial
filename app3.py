import streamlit as st
import torchaudio
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
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        st.error(f"Arquivo {bin_file} não encontrado.")
        return ""

# Função para definir a imagem de fundo da página
def set_jpeg_as_page_bg(jpeg_file):
    jpeg_file = os.path.join(os.path.dirname(__file__), jpeg_file)
    bin_str = get_base64_of_bin_file(jpeg_file)
    if bin_str:
        page_bg_img = '''
        <style>
        .stApp {
            background-image: url("data:image/jpeg;base64,%s");
            background-size: cover;
        }
        </style>
        ''' % bin_str

        st.markdown(page_bg_img, unsafe_allow_html=True)

# Conteúdo do aplicativo Streamlit
st.title("")
st.title("")
st.title("")
st.title("")
st.title("")
st.title("")

# Definir a imagem de fundo
set_jpeg_as_page_bg('fretnutapp.png')

# Função para listar arquivos WAV no diretório
def listar_arquivos_wav(diretorio):
    arquivos = [f for f in os.listdir(diretorio) if f.endswith('.wav')]
    # Ordenar os arquivos numericamente assumindo que o nome do arquivo tem números
    arquivos.sort(key=lambda x: int(x.split()[0])) 
    return arquivos

# Diretório contendo arquivos WAV
diretorio_audio = 'bruno kayapy guitarra essencial'
arquivos_wav = listar_arquivos_wav(diretorio_audio)

# Manter estado atual da faixa
if 'faixa_selecionada' not in st.session_state:
    st.session_state.faixa_selecionada = arquivos_wav[0]  # Iniciar com a primeira faixa

# Exibir a faixa atual com texto branco
faixa_atual = st.session_state.faixa_selecionada
st.markdown(f"<p style='color: white;'>Reproduzindo: {faixa_atual}</p>", unsafe_allow_html=True)

# Carregar e reproduzir a faixa atual
file_path = os.path.join(diretorio_audio, faixa_atual)
if os.path.exists(file_path):
    waveform, sample_rate = carregar_audio(file_path)
    st.audio(file_path, format='audio/wav', start_time=0)
else:
    st.error(f"Arquivo de áudio {file_path} não encontrado.")

# Adicionar a lista de reprodução
st.markdown('<div class="playlist-container">', unsafe_allow_html=True)
faixa_selecionada = st.selectbox('Selecione uma faixa', arquivos_wav, index=arquivos_wav.index(st.session_state.faixa_selecionada))
st.session_state.faixa_selecionada = faixa_selecionada
st.markdown('</div>', unsafe_allow_html=True)
