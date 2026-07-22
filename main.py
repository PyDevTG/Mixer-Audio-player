from config_manager import ConfigManager
from ModbusServer import ModbusTCPServer
from audio_player import AudioPlayer
from alarmMonitor import AlarmMonitor
import time
from gui import AlarmGUI   # <-- nova importação
import threading

def main():
    print("=== Iniciando Mixer Sonoro de Alarmes ===")

    # 1. Carrega a configuração
    cfg = ConfigManager("config.json")
    if not cfg.load():
        print("Erro fatal: configuração inválida.")
        return

    # 2. Inicia o servidor Modbus
    modbus = ModbusTCPServer(host=cfg.host, port=cfg.port)
    modbus.start_server()
    print(f"✅ Servidor Modbus rodando em {cfg.host}:{cfg.port}")

    # 3. Inicia o player de áudio
    audio = AudioPlayer()
    print("✅ Player de áudio inicializado")

    # 4. Cria o monitor de alarmes (sem callback inicial)
    monitor = AlarmMonitor(
        alarms=cfg.alarms,
        scan_interval_ms=cfg.scan_interval_ms,
        modbus_server=modbus,
        audio_player=audio,
        gui_callback=None
    )
    print(f"✅ Monitoramento configurado (intervalo: {cfg.scan_interval_ms} ms)")

    # 5. Inicia a GUI
    gui = AlarmGUI(monitor)
    # Conecta o callback da GUI ao monitor
    monitor.gui_callback = gui.update_alarm_status

    # 6. Inicia o monitor em uma thread separada (para não bloquear a GUI)
    monitor_thread = threading.Thread(target=monitor.run, daemon=True)
    monitor_thread.start()
    print("✅ Monitoramento iniciado em thread separada")

    # 7. A GUI bloqueia a thread principal (mainloop)
    gui.run()

    # 8. Ao fechar a GUI, finaliza
    monitor.stop()
    modbus.stop_server()
    print("Sistema finalizado.")

if __name__ == "__main__":
    main()
