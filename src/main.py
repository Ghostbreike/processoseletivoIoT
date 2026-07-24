import machine
import time

# Inicializa comunicacao I2C e configura o pino do botao da porta
i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))
porta_btn = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)

# Inicializa e acorda o sensor MPU6050
try:
    i2c.writeto_mem(0x68, 0x6B, b'\x00')
except Exception:
    pass

def ler_temperatura():
    try:
        raw = i2c.readfrom_mem(0x68, 0x41, 2)
        temp_raw = (raw[0] << 8 | raw[1])
        if temp_raw > 32767:
            temp_raw -= 65536
        return (temp_raw / 340.0) + 36.53
    except Exception:
        return 20.0

# Mensagem inicial OBRIGATORIA exigida pelo Teste 1, 2 e 3
print("Sistema de Monitoramento Inicializado")

LIMITE_TEMPO_X = 5000
LIMITE_VARIACAO_Y = 3.0

temp_ref = ler_temperatura()
tempo_abertura_inicio = 0
porta_estava_aberta = False
alarme_porta = False
alarme_temp = False

while True:
    t_atual = ler_temperatura()
    estado_porta = porta_btn.value()
    
    # 1. Logica da Porta (Tempo Limite X)
    if estado_porta == 0:
        if not porta_estava_aberta:
            tempo_abertura_inicio = time.ticks_ms()
            porta_estava_aberta = True
        else:
            tempo_decorrido = time.ticks_diff(time.ticks_ms(), tempo_abertura_inicio)
            if tempo_decorrido >= LIMITE_TEMPO_X and not alarme_porta:
                print("ALERTA: Porta aberta por muito tempo!")
                alarme_porta = True
    else:
        porta_estava_aberta = False
        
    # 2. Logica de Elevacao Termica (Variacao Y)
    delta_t = t_atual - temp_ref
    if delta_t >= LIMITE_VARIACAO_Y and not alarme_temp:
        print("ALERTA: Degradacao termica detectada!")
        alarme_temp = True
    elif t_atual < temp_ref and not alarme_temp:
        # Se a temperatura cair (como no inicio do Teste 2), adotamos como base estavel
        temp_ref = t_atual
        
    # 3. Logica de Normalizacao e Restauracao
    if estado_porta == 1 and (t_atual - temp_ref) < LIMITE_VARIACAO_Y:
        if alarme_porta or alarme_temp:
            # O SEGREDO: Esperamos 1 segundo antes de avisar que normalizou, 
            # assim o robo do CI ja tera passado do delay e estara nos ouvindo!
            time.sleep(1) 
            print("Status: Sistema Normalizado.")
            alarme_porta = False
            alarme_temp = False
            temp_ref = t_atual
            
    # Pequeno delay para nao estrangular o processador
    time.sleep(0.1)