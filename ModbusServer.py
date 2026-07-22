from pyModbusTCP.server import ModbusServer, DataBank

import threading
import time

class ModbusTCPServer:
    def __init__(self, host="0.0.0.0", port=502):
        self.databank = DataBank()
        self.server = ModbusServer(host=host, port=port, no_block=True,data_bank=self.databank)
        self.running = False

    def start_server(self):
        try:
            self.server.start()
            self.running = True
            #print(f"Servidor Modbus TCP iniciado em {self.server.host}:{self.server.port}")
        except Exception as e:
            
            print(f"Erro ao iniciar o servidor: {e}")

    def stop_server(self):
        try:
            self.server.stop()
            self.running = False
            #print("Servidor Modbus TCP parado.")
        except Exception as e:
            print(f"Erro ao parar o servidor: {e}")

    def read_holding(self, address, count=1):
        try:
            
            values = self.server.data_bank.get_holding_registers(address,count)
            #print(f"Lido Holding Register [{address}]: {values}")
            return values
        except Exception as e:
            print(f"Erro ao ler registrador: {e}")
            return None

    def write_holding(self, address, values):
        try:
            if isinstance(values, int):
                values = [values]
            values = self.server.data_bank.set_holding_registers(address,values)
            #print(f"Escrito Holding Register [{address}]: {values}")
        except Exception as e:
            print(f"Erro ao escrever registrador: {e}")
