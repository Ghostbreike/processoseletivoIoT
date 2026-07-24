import machine
import dht
import time

# Configuração dos pinos com base no diagrama
sensor_temp = dht.DHT22(machine.Pin(15))
led_alerta = machine.Pin(2, machine.Pin.OUT)

print("Iniciando Sistema de Monitoramento de Temperatura...")

# Limitando a 4 iterações para o simulador não dar timeout
for i in range(4):
    try:
        # Realiza a leitura do sensor
        sensor_temp.measure()
        temperatura = sensor_temp.temperature()
        umidade = sensor_temp.humidity()
        
        print(f"Temperatura: {temperatura}°C | Umidade: {umidade}%")
        
        # Lógica de controle: Alerta se passar de 30 graus
        if temperatura > 30.0:
            led_alerta.value(1) # Acende o LED
            print("ALERTA: Temperatura muito alta!")
        else:
            led_alerta.value(0) # Apaga o LED
            
    except OSError as e:
        print("Falha ao ler o sensor.")
        
    # Temporização do loop (leitura a cada 2 segundos)
    time.sleep(2)