import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Criar pasta para salvar os gráficos 
os.makedirs("resultados", exist_ok=True)

# Configuração de estilo visual dos gráficos
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

# Configurações Gerais de Amostragem
fs = 1000  # Frequência de amostragem (Hz)
t = np.arange(0, 1.0, 1/fs)

print("=== INICIANDO GERAÇÃO DOS GRÁFICOS ===")

# ==========================================
# Q1. Duas Senoides e Filtro Passa-Baixas
# ==========================================
f1, f2 = 10, 150  # 10 Hz (desejada) e 150 Hz (indesejada)
sinal_q1 = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)

# Projeto do filtro FIR Passa-Baixas via Janela
num_taps = 61
b_fir_q1 = signal.firwin(num_taps, cutoff=50, fs=fs)
sinal_filtrado_q1 = signal.lfilter(b_fir_q1, 1.0, sinal_q1)

plt.figure(figsize=(10, 3.5))
plt.plot(t, sinal_q1, label='Sinal Composto (10Hz + 150Hz)', alpha=0.6)
plt.plot(t, sinal_filtrado_q1, label='Sinal Filtrado (Passa-Baixas 50Hz)', linewidth=2)
plt.title('Q1 - Filtragem de Componentes Senoidais')
plt.xlabel('Tempo (s)')
plt.ylabel('Amplitude')
plt.legend()
plt.tight_layout()
plt.savefig('resultados/q1_filtragem_senoides.png')
plt.show()  # Exibir

# ==========================================
# Q2 e Q3. Ruído Branco + Comparação FIR vs IIR Butterworth
# ==========================================
np.random.seed(42)
sinal_puro = np.sin(2 * np.pi * 5 * t)
ruido = np.random.normal(0, 0.5, len(t))
sinal_ruidoso = sinal_puro + ruido

# FIR (Janela de Hamming)
b_fir = signal.firwin(81, cutoff=20, fs=fs)
filtrado_fir = signal.lfilter(b_fir, 1.0, sinal_ruidoso)

# IIR (Butterworth de 4ª ordem)
b_iir, a_iir = signal.butter(4, 20, btype='low', fs=fs)
filtrado_iir = signal.lfilter(b_iir, a_iir, sinal_ruidoso)

fig, axs = plt.subplots(3, 1, figsize=(10, 7), sharex=True)
axs[0].plot(t, sinal_ruidoso, color='gray', alpha=0.7, label='Ruidoso')
axs[0].plot(t, sinal_puro, 'r', label='Original (5 Hz)')
axs[0].set_title('Sinal Original e Contaminado')
axs[0].legend()

axs[1].plot(t, filtrado_fir, 'g', label='Filtrado FIR (Ordem 80)')
axs[1].set_title('Q2 - Redução de Ruído com Filtro FIR')
axs[1].legend()

axs[2].plot(t, filtrado_iir, 'b', label='Filtrado IIR Butterworth (Ordem 4)')
axs[2].set_title('Q3 - Redução de Ruído com Filtro IIR')
axs[2].legend()
plt.xlabel('Tempo (s)')
plt.tight_layout()
plt.savefig('resultados/q2_q3_comparacao_ruido.png')
plt.show()  # Exibir

# ==========================================
# Q4. Resposta em Frequência (Magnitude): FIR vs IIR
# ==========================================
w_fir, h_fir = signal.freqz(b_fir, 1.0, worN=2000, fs=fs)
w_iir, h_iir = signal.freqz(b_iir, a_iir, worN=2000, fs=fs)

plt.figure(figsize=(10, 3.5))
plt.plot(w_fir, 20 * np.log10(np.abs(h_fir)), 'g', label=f'FIR (Ordem {len(b_fir)-1})')
plt.plot(w_iir, 20 * np.log10(np.abs(h_iir)), 'b', label=f'IIR Butterworth (Ordem 4)')
plt.axvline(20, color='r', linestyle='--', label='Corte (20 Hz)')
plt.title('Q4 - Resposta em Frequência (Magnitude)')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Ganho (dB)')
plt.ylim([-80, 5])
plt.legend()
plt.tight_layout()
plt.savefig('resultados/q4_resposta_frequencia.png')
plt.show()  # Exibir gráfico

# ==========================================
# Q5. Polos e Zeros do Filtro IIR
# ==========================================
z, p, k = signal.tf2zpk(b_iir, a_iir)
fig, ax = plt.subplots(figsize=(4.5, 4.5))
circulo = plt.Circle((0, 0), 1, color='gray', fill=False, linestyle='--')
ax.add_artist(circulo)
ax.scatter(np.real(z), np.imag(z), s=80, marker='o', facecolors='none', edgecolors='b', label='Zeros')
ax.scatter(np.real(p), np.imag(p), s=80, marker='x', color='r', label='Polos')
ax.axhline(0, color='black', lw=0.5)
ax.axvline(0, color='black', lw=0.5)
ax.set_title('Q5 - Mapa de Polos e Zeros (IIR)')
ax.set_xlabel('Parte Real')
ax.set_ylabel('Parte Imaginária')
ax.set_xlim([-1.2, 1.2])
ax.set_ylim([-1.2, 1.2])
ax.grid(True)
ax.legend()
plt.tight_layout()
plt.savefig('resultados/q5_polos_zeros.png')
plt.show()  # Exibir o gráfico

# ==========================================
# Q6. Resposta ao Impulso: FIR vs IIR
# ==========================================
t_imp = np.arange(0, 150)
impulso = np.zeros(150)
impulso[0] = 1.0

h_fir_imp = signal.lfilter(b_fir, 1.0, impulso)
h_iir_imp = signal.lfilter(b_iir, a_iir, impulso)

fig, axs = plt.subplots(2, 1, figsize=(10, 5))
axs[0].stem(t_imp[:100], h_fir_imp[:100], linefmt='g-', markerfmt='go', basefmt='k-')
axs[0].set_title('Q6 - Resposta ao Impulso - FIR (Finitude Estrita)')
axs[0].set_ylabel('Amplitude')

axs[1].stem(t_imp[:100], h_iir_imp[:100], linefmt='b-', markerfmt='bo', basefmt='k-')
axs[1].set_title('Resposta ao Impulso - IIR (Decaimento Assintótico)')
axs[1].set_xlabel('Amostras (n)')
axs[1].set_ylabel('Amplitude')
plt.tight_layout()
plt.savefig('resultados/q6_resposta_impulso.png')
plt.show()  # Exibir

# ==========================================
# Q7. Filtro Passa-Faixa
# ==========================================
f_pf1, f_pf2, f_pf3 = 15, 60, 200
sinal_pf = np.sin(2*np.pi*f_pf1*t) + np.sin(2*np.pi*f_pf2*t) + np.sin(2*np.pi*f_pf3*t)

# Projeta passa-faixa para isolar os 60 Hz
b_pf = signal.firwin(121, [45, 75], pass_zero='bandpass', fs=fs)
sinal_filtrado_pf = signal.lfilter(b_pf, 1.0, sinal_pf)

freqs_fft = np.fft.rfftfreq(len(t), 1/fs)
fft_original = np.abs(np.fft.rfft(sinal_pf))
fft_filtrado = np.abs(np.fft.rfft(sinal_filtrado_pf))

fig, axs = plt.subplots(2, 1, figsize=(10, 5))
axs[0].plot(freqs_fft, fft_original, color='orange')
axs[0].set_title('Q7 - Espectro do Sinal Original (Três Senoides)')
axs[0].set_xlim([0, 250])
axs[0].set_ylabel('Magnitude')

axs[1].plot(freqs_fft, fft_filtrado, color='teal')
axs[1].set_title('Espectro do Sinal Filtrado (Passa-Faixa centrado em 60 Hz)')
axs[1].set_xlim([0, 250])
axs[1].set_xlabel('Frequência (Hz)')
axs[1].set_ylabel('Magnitude')
plt.tight_layout()
plt.savefig('resultados/q7_filtro_passa_faixa.png')
plt.show()  # Exibir

# ==========================================
# Q8. Resposta de Fase: FIR (Linear) vs IIR (Não Linear)
# ==========================================
plt.figure(figsize=(10, 3.5))
plt.plot(w_fir, np.unwrap(np.angle(h_fir)), 'g', label='FIR (Fase Perfeitamente Linear)')
plt.plot(w_iir, np.unwrap(np.angle(h_iir)), 'b', label='IIR (Fase Não Linear)')
plt.title('Q8 - Comparação da Resposta de Fase Unwrapped')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Fase (radianos)')
plt.xlim([0, 100])
plt.legend()
plt.tight_layout()
plt.savefig('resultados/q8_resposta_fase.png')
plt.show()  # Exibir

# ==========================================
# Q9. Atraso de Grupo (Group Delay)
# ==========================================
w_gd_fir, gd_fir = signal.group_delay((b_fir, 1.0), w=2000, fs=fs)
w_gd_iir, gd_iir = signal.group_delay((b_iir, a_iir), w=2000, fs=fs)

plt.figure(figsize=(10, 3.5))
plt.plot(w_gd_fir, gd_fir, 'g', label='FIR (Atraso Constante)')
plt.plot(w_gd_iir, gd_iir, 'b', label='IIR (Atraso Variável com a Frequência)')
plt.axvline(20, color='r', linestyle='--', label='Corte do Filtro (20 Hz)')
plt.title('Q9 - Comparação do Atraso de Grupo (Group Delay)')
plt.xlabel('Frequência (Hz)')
plt.ylabel('Atraso (Amostras)')
plt.xlim([0, 100])
plt.ylim([0, max(np.max(gd_fir), np.max(gd_iir[:200])) * 1.2])
plt.legend()
plt.tight_layout()
plt.savefig('resultados/q9_atraso_grupo.png')
plt.show()  # Exibir

# ==========================================
# Q10. Aplicação Prática: Suavização de Sensor (Problema Agrícola)
# ==========================================
sinal_sensor_puro = np.ones(len(t)) * 5.0
ruido_sensor = 0.4 * np.sin(2 * np.pi * 120 * t) + np.random.normal(0, 0.15, len(t))
sinal_sensor_ruidoso = sinal_sensor_puro + ruido_sensor

b_sensor, a_sensor = signal.butter(2, 5, btype='low', fs=fs)
sinal_sensor_suavizado = signal.lfilter(b_sensor, a_sensor, sinal_sensor_ruidoso)

plt.figure(figsize=(10, 3.5))
plt.plot(t, sinal_sensor_ruidoso, color='salmon', alpha=0.6, label='Leitura Bruta do Sensor (Com interferência AC)')
plt.plot(t, sinal_sensor_suavizado, color='darkred', linewidth=2, label='Dado Condicionado/Suavizado (Pronto para TinyML)')
plt.axhline(5.0, color='black', linestyle=':', label='Valor Real Estável')
plt.title('Q10 - Aplicação Prática: Condicionamento de Sinais em Monitoramento Agrícola')
plt.xlabel('Tempo (s)')
plt.ylabel('Grandeza do Sensor (V)')
plt.legend()
plt.tight_layout()
plt.savefig('resultados/q10_aplicacao_pratica.png')
plt.show()  # Exibir
