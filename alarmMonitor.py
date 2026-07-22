import time

class AlarmMonitor:
    def __init__(self, alarms, scan_interval_ms, modbus_server, audio_player, gui_callback=None, status_callback=None):
        self.alarms = alarms
        self.scan_interval = scan_interval_ms / 1000.0
        self.modbus = modbus_server
        self.audio = audio_player
        self.gui_callback = gui_callback
        self.status_callback = status_callback  # novo callback para status do servidor
        self.running = True
        self.server_ok = True  # estado atual do servidor

    def run(self):
        print("Monitoramento iniciado (sequencial). Pressione Ctrl+C para parar.")
        try:
            while self.running:
                for alarm in self.alarms:
                    if not self.running:
                        break
                    
                    reg = alarm['register']
                    trigger = alarm['trigger_value']
                    bell=alarm['bell']
                    
                    
                    # Lê o registrador
                    try:
                        values = self.modbus.read_holding(reg, 1)
                        current_value = values[0] if values else 0
                        # Se chegou aqui, servidor está respondendo
                        if not self.server_ok:
                            self.server_ok = True
                            if self.status_callback:
                                self.status_callback(True)
                    except Exception as e:
                        print(f"Erro ao ler registrador {reg}: {e}")
                        current_value = 0
                        # Se houve erro, servidor pode estar inativo
                        if self.server_ok:
                            self.server_ok = False
                            if self.status_callback:
                                self.status_callback(False)

                    # Se o valor for igual ao trigger, toca o áudio e espera
                    if current_value == trigger:
                        print(f"🔔 Alarme ATIVO: {alarm['name']} (valor={current_value})")
                        try:
                            if(bell==True):
                                self.audio.play('audios/bell.mp3')
                                time.sleep(3)
                        except:
                            pass
                        self.audio.play(alarm['audio_file'])
                        
                        
                        wait_time = alarm.get('repeat_interval_sec', self.scan_interval)
                        if wait_time < 0.1:
                            wait_time = self.scan_interval
                        print(f"⏳ Aguardando {wait_time:.1f}s antes do próximo alarme...")
                        time.sleep(wait_time)
                        
                        if self.gui_callback:
                            self.gui_callback(alarm['name'], True)
                    else:
                        # Atualiza GUI como inativo (se mudou)
                        if self.gui_callback:
                            #pass
                            # Idealmente, só atualizar se mudou, mas por simplicidade chamamos sempre
                            self.gui_callback(alarm['name'], False)

                # Aguarda o próximo ciclo completo
                #print(f"🔄 Varredura concluída. Aguardando {self.scan_interval}s antes de recomeçar.")
                time.sleep(self.scan_interval)

        except KeyboardInterrupt:
            print("\nMonitoramento interrompido pelo usuário.")
        finally:
            self.running = False
            print("Monitoramento finalizado.")

    def stop(self):
        self.running = False