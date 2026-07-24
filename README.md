# Relatório do Desafio Técnico: Monitoramento de Temperatura e Porta

## Identificação do Candidato
* **Nome completo:** Rian Lucas da Silva
* **GitHub:** Ghostbreike

## Visão Geral da Solução
* **Objetivo:** O projeto estabelece uma solução embarcada para auditar e controlar a qualidade em ambientes que exigem isolamento térmico, prevenindo a degradação de insumos.
* **O que o sistema faz:** Monitora continuamente o tempo em que a porta permanece aberta e as variações térmicas bruscas no ambiente (Delta T). Caso qualquer um dos limites seja ultrapassado, o sistema dispara alertas independentes via comunicação Serial.
* **Como o usuário interage:** O usuário interage fisicamente com a porta do ambiente (representada pelo botão). O sistema atua de forma autônoma, lendo essa interação e o clima, e reportando o status de alarme ou normalização de volta para o usuário através do terminal de logs.

## Arquitetura do Sistema Embarcado
* **Fluxo principal (`main.py`):** O sistema inicializa a comunicação I2C e configura o pino do botão. Em seguida, entra em um loop infinito (`while True`) onde avalia as condições de risco a cada 100ms de forma não-bloqueante (sem uso de delays longos que travem a checagem paralela).
* **Estrutura de estados:** 
  * *Estado Normal:* Monitora ativamente.
  * *Alarme de Porta:* Disparado se o botão registrar a porta aberta (lógica 0) por mais de 5000ms.
  * *Alarme Térmico:* Disparado se a variação da temperatura (T_atual - T_ref) for maior ou igual a 3.0°C.
  * *Normalização:* Apenas ocorre quando a porta é fechada (lógica 1) simultaneamente à estabilização térmica, emitindo o log de restauração com um atraso estratégico de 1 segundo para sincronização com serviços de CI.
* **Como os componentes interagem:** O ESP32 atua como processador central. Ele lê os pulsos lógicos do Botão via GPIO e capta os bytes brutos de temperatura do MPU6050 via protocolo I2C. Após processar a lógica matemática e os blocos condicionais, o ESP32 emite logs de texto através da saída TX para o monitor Serial.

## Componentes Utilizados na Simulação
* **Microcontrolador:** ESP32 DevKit C v4 (`esp`) - Responsável pelo processamento lógico geral, execução do firmware em MicroPython e comunicação Serial.
* **Sensor de Temperatura:** MPU6050 (`imu1`) - Módulo inercial utilizado especificamente para extrair a temperatura ambiente do local. Comunicação via pinos I2C (SDA 21, SCL 22).
* **Sensor de Porta:** Pushbutton (`btn1`) - Simula um sensor fim de curso da porta. O estado pressionado (1) representa a porta fechada, enquanto o solto (0) representa a porta aberta. Conectado ao pino 14 com Pull-Down interno.