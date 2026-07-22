import json
import os

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.host = None
        self.port = None
        self.scan_interval_ms = None
        self.alarms = []
        self._loaded = False

    def load(self):
        try:
            if not os.path.isfile(self.config_file):
                print(f"Arquivo {self.config_file} não encontrado.")
                return False
            with open(self.config_file, 'r', encoding='utf-8-sig') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Erro ao carregar configuração: {e}")
            return False

        # Extrai os dados
        server = data.get('modbus_server', {})
        self.host = server.get('host', '0.0.0.0')
        self.port = server.get('port', 502)
        self.scan_interval_ms = data.get('scan_interval_ms', 500)
        self.alarms = data.get('alarms', [])

        # Opcional: verifica arquivos de áudio (apenas aviso)
        for alarm in self.alarms:
            audio_path = alarm.get('audio_file', '')
            if audio_path and not os.path.isfile(audio_path):
                print(f"Aviso: arquivo de áudio não encontrado: {audio_path}")

        self._loaded = True
        print(f"Configuração carregada com sucesso. {len(self.alarms)} alarme(s) definido(s).")
        return True

    def get_server(self):
        return (self.host, self.port)

    def get_alarms(self):
        return self.alarms

    def get_scan_interval(self):
        return self.scan_interval_ms