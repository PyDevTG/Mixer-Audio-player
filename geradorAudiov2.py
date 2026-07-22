import os
import asyncio

# Tenta importar edge-tts
try:
    import edge_tts
    EDGE_AVAILABLE = True
except ImportError:
    EDGE_AVAILABLE = False
    print("⚠️ edge-tts não instalado. Instale com: pip install edge-tts")

# Tenta importar gTTS
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False
    print("⚠️ gTTS não instalado. Instale com: pip install gTTS")

# Dicionário de vozes (códigos para edge-tts)
VOZES_EDGE = {
    "antonio": "pt-BR-AntonioNeural",
    "francisca": "pt-BR-FranciscaNeural",
    "duarte": "pt-PT-DuarteNeural",
    "raquel": "pt-PT-RaquelNeural",
    "joana": "pt-PT-JoanaNeural",
    "en_female": "en-US-JennyNeural",
    "en_male": "en-US-GuyNeural",
}

# Dicionário de TLDs para gTTS (diferentes sotaques)
TLDS = ["com.br", "pt", "com", "co.uk"]

async def gerar_edge(texto, nome_arquivo, voz_codigo, timeout=30):
    try:
        comunicador = edge_tts.Communicate(texto, voz_codigo)
        await asyncio.wait_for(comunicador.save(nome_arquivo), timeout=timeout)
        print(f"✅ Áudio gerado (edge-tts): {nome_arquivo} (voz: {voz_codigo})")
        return True
    except Exception as e:
        print(f"⚠️ edge-tts falhou: {e}")
        return False

def gerar_gtts(texto, nome_arquivo, lang="pt", tld="com.br", slow=False):
    try:
        tts = gTTS(text=texto, lang=lang, slow=slow, tld=tld)
        tts.save(nome_arquivo)
        print(f"✅ Áudio gerado (gTTS): {nome_arquivo} (tld={tld})")
        return True
    except Exception as e:
        print(f"❌ gTTS falhou: {e}")
        return False

def gerar_audio(texto, nome_arquivo, voz="antonio", timeout=30, fallback_gtts=True):
    """
    Gera áudio usando edge-tts (melhor qualidade, várias vozes).
    Se falhar, usa gTTS como fallback.
    
    :param texto: Texto a ser falado.
    :param nome_arquivo: Caminho do arquivo de saída (ex: "audios/alarme.mp3").
    :param voz: Chave do dicionário VOZES_EDGE (antonio, francisca, duarte, etc.)
    :param timeout: Tempo máximo de espera para edge-tts (segundos).
    :param fallback_gtts: Se True, usa gTTS se edge-tts falhar.
    """
    # Cria diretório
    os.makedirs(os.path.dirname(nome_arquivo) or '.', exist_ok=True)
    
    # Tenta edge-tts primeiro
    if EDGE_AVAILABLE:
        voz_codigo = VOZES_EDGE.get(voz, voz)  # permite código direto
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            sucesso = loop.run_until_complete(gerar_edge(texto, nome_arquivo, voz_codigo, timeout))
            if sucesso:
                return
        finally:
            loop.close()
        print("⚠️ edge-tts não funcionou, tentando fallback...")
    
    # Fallback: gTTS
    if fallback_gtts and GTTS_AVAILABLE:
        # Tenta diferentes TLDs para variar sotaque
        for tld in TLDS:
            if gerar_gtts(texto, nome_arquivo, lang="pt", tld=tld):
                return
        # Último recurso: gTTS sem TLD especificado
        gerar_gtts(texto, nome_arquivo, lang="pt")
    else:
        print("❌ Nenhum método disponível para gerar áudio.")

# ---------- Exemplo de uso ----------
if __name__ == "__main__":
    # Gera áudio com voz masculina brasileira (antonio)
    gerar_audio("Erro no Robô", "audios/robotError.mp3", voz="antonio")
    
    # Gera com voz feminina brasileira (francisca)
    gerar_audio("Falha na Retirada do JIG um", "audios/falhaRJig01.mp3", voz="francisca")
    gerar_audio("Falha na Retirada do JIG dois", "audios/falhaRJig02.mp3", voz="francisca")
    
    # Pode usar também código direto (se quiser outra voz não listada):
    # gerar_audio("Texto", "audio.mp3", voz="pt-PT-DuarteNeural")