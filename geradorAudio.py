import os
from gtts import gTTS

def gerar_audio(texto, nome_arquivo, lang="pt", slow=False):
    """
    Gera um arquivo de áudio MP3 a partir de um texto usando Google TTS.
    
    :param texto: Texto a ser convertido em fala.
    :param nome_arquivo: Caminho completo do arquivo de saída (ex: "audios/alarme.mp3").
    :param lang: Idioma (padrão 'pt' - português).
    :param slow: Fala mais lenta (True/False).
    """
    try:
        # Cria o diretório se não existir
        diretorio = os.path.dirname(nome_arquivo)
        if diretorio and not os.path.exists(diretorio):
            os.makedirs(diretorio)
        
        # Gera o áudio com gTTS
        tts = gTTS(text=texto, lang=lang, slow=slow)
        tts.save(nome_arquivo)
        print(f"✅ Áudio MP3 gerado: {nome_arquivo}")
            
    except Exception as e:
        print(f"❌ Erro ao gerar áudio: {e}")

# Exemplo de uso (se executar diretamente)
if __name__ == "__main__":
    # Gera áudios de exemplo para os alarmes
    gerar_audio("Erro no Robô", "audios/robotError.mp3")
    #gerar_audio("Falha na Retirada do JIG um", "audios/falhaRJig01.mp3")
    #gerar_audio("Falha na Retirada do JIG dois", "audios/falhaRJig02.mp3")
    