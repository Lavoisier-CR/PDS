# =============================================================
# SIMULAÇÃO DE SINAIS DIGITAIS ADQUIRIDOS POR SISTEMAS EMBARCADOS
# Fundamentação: Oppenheim, Proakis, Lathi
# =============================================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import AutoMinorLocator

# =============================================================
# CONFIGURAÇÕES GLOBAIS DE VISUALIZAÇÃO
# =============================================================

plt.rcParams.update({
    'figure.facecolor': '#0f0f1a',
    'axes.facecolor':   '#1a1a2e',
    'axes.edgecolor':   '#4a4a7a',
    'axes.labelcolor':  '#e0e0ff',
    'xtick.color':      '#e0e0ff',
    'ytick.color':      '#e0e0ff',
    'text.color':       '#e0e0ff',
    'grid.color':       '#2a2a4a',
    'grid.linestyle':   '--',
    'grid.alpha':       0.6,
    'legend.facecolor': '#1a1a2e',
    'legend.edgecolor': '#4a4a7a',
    'font.family':      'monospace',
})

CORES = {
    'ciano':    '#00f5ff',
    'magenta':  '#ff00ff',
    'verde':    '#00ff88',
    'amarelo':  '#ffee00',
    'laranja':  '#ff6600',
    'roxo':     '#aa00ff',
    'branco':   '#ffffff',
    'vermelho': '#ff4444',
}

# =============================================================
# MÓDULO 1: PARÂMETROS DO SISTEMA EMBARCADO (ADC)
# =============================================================

# --- Parâmetros do ADC (ex: STM32, ESP32, Arduino) ----------
Fs        = 1000          # Frequência de amostragem [Hz]
Ts        = 1 / Fs        # Período de amostragem [s]
bits_adc  = 12            # Resolução do ADC em bits
niveis    = 2 ** bits_adc # Número de níveis de quantização (4096)
Vref      = 3.3           # Tensão de referência do ADC [V]
lsb       = Vref / niveis # Valor do LSB (menor variação detectável)
duracao   = 1.0           # Duração do sinal [s]

# --- Vetor de tempo contínuo (simulando o sinal real) --------
t_cont = np.linspace(0, duracao, 100_000)  # Alta resolução

# --- Vetor de tempo discreto (amostras do ADC) ---------------
t_disc = np.arange(0, duracao, Ts)         # Instantes de amostragem
N      = len(t_disc)                       # Número total de amostras

print("=" * 55)
print("     PARÂMETROS DO SISTEMA EMBARCADO (ADC)")
print("=" * 55)
print(f"  Frequência de amostragem : {Fs} Hz")
print(f"  Período de amostragem    : {Ts*1000:.2f} ms")
print(f"  Resolução do ADC         : {bits_adc} bits")
print(f"  Níveis de quantização    : {niveis}")
print(f"  Tensão de referência     : {Vref} V")
print(f"  Valor do LSB             : {lsb*1000:.4f} mV")
print(f"  Número de amostras       : {N}")
print("=" * 55)

# =============================================================
# MÓDULO 2: GERAÇÃO DO SINAL ANALÓGICO (ANTES DO ADC)
# =============================================================

# --- Sinal composto: soma de senoides (sensor analógico) -----
f1, A1 = 50,  1.0   # Componente fundamental   [Hz, V]
f2, A2 = 120, 0.5   # Segunda harmônica        [Hz, V]
f3, A3 = 200, 0.3   # Interferência de rede    [Hz, V]

# Sinal contínuo (referência)
x_cont = (A1 * np.sin(2 * np.pi * f1 * t_cont) +
          A2 * np.sin(2 * np.pi * f2 * t_cont) +
          A3 * np.sin(2 * np.pi * f3 * t_cont))

# Sinal amostrado pelo ADC (antes da quantização)
x_amostrado = (A1 * np.sin(2 * np.pi * f1 * t_disc) +
               A2 * np.sin(2 * np.pi * f2 * t_disc) +
               A3 * np.sin(2 * np.pi * f3 * t_disc))

# Adiciona ruído térmico do sensor (AWGN) - SNR ~40 dB
snr_db    = 40
snr_lin   = 10 ** (snr_db / 10)
potencia  = np.mean(x_amostrado ** 2)
sigma     = np.sqrt(potencia / snr_lin)
ruido     = np.random.normal(0, sigma, N)
x_ruidoso = x_amostrado + ruido

# =============================================================
# MÓDULO 3: QUANTIZAÇÃO DO ADC
# =============================================================

def quantizar_adc(sinal, bits, v_min=-Vref/2, v_max=Vref/2):
    """
    Simula a quantização de um ADC de N bits.
    Converte o sinal contínuo em valores inteiros (códigos ADC)
    e depois reconverte para tensão (saída do ADC).

    Parâmetros:
        sinal  : array do sinal de entrada
        bits   : resolução em bits
        v_min  : tensão mínima do ADC
        v_max  : tensão máxima do ADC

    Retorna:
        sinal_q   : sinal quantizado em tensão
        codigos   : códigos inteiros do ADC
        erro_q    : erro de quantização (ruído de quantização)
    """
    niveis_q = 2 ** bits
    lsb_q    = (v_max - v_min) / niveis_q

    # Limita o sinal ao range do ADC (clipping)
    sinal_clip = np.clip(sinal, v_min, v_max)

    # Converte para código inteiro (0 a 2^bits - 1)
    codigos = np.floor((sinal_clip - v_min) / lsb_q).astype(int)
    codigos = np.clip(codigos, 0, niveis_q - 1)

    # Reconverte para tensão (saída do DAC/ADC)
    sinal_q = codigos * lsb_q + v_min + lsb_q / 2

    # Erro de quantização
    erro_q = sinal_q - sinal_clip

    return sinal_q, codigos, erro_q


x_quantizado, codigos_adc, erro_quant = quantizar_adc(
    x_ruidoso, bits_adc
)

# =============================================================
# MÓDULO 4: SEQUÊNCIAS ELEMENTARES DISCRETAS
# =============================================================

n = np.arange(-50, 150)  # Eixo de amostras discretas

# --- Impulso unitário (delta de Kronecker) -------------------
impulso = (n == 0).astype(float)

# --- Degrau unitário -----------------------------------------
degrau  = (n >= 0).astype(float)

# --- Rampa unitária ------------------------------------------
rampa   = np.where(n >= 0, n, 0).astype(float)

# --- Exponencial real decrescente: a^n * u[n] ----------------
a_real    = 0.95
exp_real  = (a_real ** n) * degrau

# --- Exponencial complexa: e^(j*omega*n) ---------------------
omega_0   = 0.1 * np.pi
exp_comp  = np.exp(1j * omega_0 * n)

# =============================================================
# MÓDULO 5: OPERAÇÕES COM SINAIS
# =============================================================

# --- Sinal base para operações (janela de 100 amostras) ------
n_op = np.arange(0, 100)
x_op = np.sin(2 * np.pi * 0.05 * n_op) * np.exp(-0.03 * n_op)

# --- Deslocamento temporal: y[n] = x[n - n0] -----------------
n0           = 20
x_atrasado   = np.zeros(len(n_op))
x_atrasado[n0:] = x_op[:len(n_op) - n0]

# --- Inversão: y[n] = x[-n] ----------------------------------
x_invertido = x_op[::-1]

# --- Escalonamento de amplitude: y[n] = 2 * x[n] -------------
x_escalonado = 2.0 * x_op

# --- Soma de sinais ------------------------------------------
x_soma = x_op + x_atrasado

# =============================================================
# MÓDULO 6: ENERGIA E POTÊNCIA DOS SINAIS
# =============================================================

def calcular_energia_potencia(sinal, nome="Sinal"):
    """
    Calcula a energia total e a potência média de uma sequência.

    E = sum(|x[n]|^2)
    P = (1/N) * sum(|x[n]|^2)

    Parâmetros:
        sinal : array da sequência discreta
        nome  : nome do sinal para exibição

    Retorna:
        energia  : energia total do sinal
        potencia : potência média do sinal
    """
    energia  = np.sum(np.abs(sinal) ** 2)
    potencia = np.mean(np.abs(sinal) ** 2)

    print(f"\n  [{nome}]")
    print(f"    Energia total  E  = {energia:.4f} J")
    print(f"    Potência média P  = {potencia:.6f} W")
    print(f"    Tipo de sinal     : "
          f"{'Energia Finita' if energia < np.inf else 'Potência'}")
    return energia, potencia

print("\n" + "=" * 55)
print("       ENERGIA E POTÊNCIA DOS SINAIS")
print("=" * 55)

E_orig,    P_orig    = calcular_energia_potencia(x_amostrado,  "Original Amostrado")
E_ruid,    P_ruid    = calcular_energia_potencia(x_ruidoso,    "Com Ruído Térmico ")
E_quant,   P_quant   = calcular_energia_potencia(x_quantizado, "Quantizado (ADC)  ")
E_eq,      P_eq      = calcular_energia_potencia(erro_quant,   "Erro de Quantiz.  ")
E_exp,     P_exp     = calcular_energia_potencia(exp_real,     "Exp. Real (a^n)   ")

# --- SQNR (Signal-to-Quantization-Noise Ratio) ---------------
sqnr_linear = P_orig / P_eq  if P_eq > 0 else np.inf
sqnr_db     = 10 * np.log10(sqnr_linear)
sqnr_teorico = 6.02 * bits_adc + 1.76  # Fórmula teórica SQNR

print(f"\n  [SQNR - Relação Sinal/Ruído de Quantização]")
print(f"    SQNR medido   = {sqnr_db:.2f} dB")
print(f"    SQNR teórico  = {sqnr_teorico:.2f} dB  (6.02*{bits_adc} + 1.76)")
print("=" * 55)

# =============================================================
# MÓDULO 7: ANÁLISE ESPECTRAL (FFT)
# =============================================================

# --- FFT do sinal amostrado ----------------------------------
X_fft   = np.fft.fft(x_amostrado, N)
X_mag   = (2 / N) * np.abs(X_fft[:N // 2])  # Magnitude normalizada
freqs   = np.fft.fftfreq(N, Ts)[:N // 2]    # Eixo de frequências

# --- FFT do sinal quantizado ---------------------------------
Xq_fft  = np.fft.fft(x_quantizado, N)
Xq_mag  = (2 / N) * np.abs(Xq_fft[:N // 2])

# --- Espectro do erro de quantização -------------------------
Eq_fft  = np.fft.fft(erro_quant, N)
Eq_mag  = (2 / N) * np.abs(Eq_fft[:N // 2])

# =============================================================
# MÓDULO 8: CLASSIFICAÇÃO DE SISTEMAS (DEMONSTRAÇÃO)
# =============================================================

def sistema_media_movel(x, M=5):
    """
    Sistema LTI: Média Móvel de ordem M.
    y[n] = (1/M) * sum_{k=0}^{M-1} x[n-k]

    Propriedades:
      - Linear         : Sim (satisfaz superposição)
      - Invariante      : Sim (coeficientes constantes)
      - Causal          : Sim (usa apenas x[n-k], k >= 0)
      - Com memória     : Sim (usa M-1 amostras passadas)
      - BIBO estável    : Sim (sum|h[n]| = M * (1/M) = 1)
    """
    y = np.convolve(x, np.ones(M) / M, mode='same')
    return y

def sistema_nao_linear(x):
    """
    Sistema Não-Linear: Retificador de meia onda.
    y[n] = max(x[n], 0)

    Propriedades:
      - Linear    : Não (viola superposição)
      - Causal    : Sim
      - Invariante: Sim
    """
    return np.maximum(x, 0)

def sistema_nao_causal(x, M=5):
    """
    Sistema Não-Causal: Média centrada.
    y[n] = (1/(2M+1)) * sum_{k=-M}^{M} x[n-k]

    Propriedades:
      - Causal : Não (usa amostras futuras)
      - Linear : Sim
    """
    kernel = np.ones(2 * M + 1) / (2 * M + 1)
    return np.convolve(x, kernel, mode='same')

# Aplica os sistemas ao sinal quantizado
y_media_movel   = sistema_media_movel(x_quantizado, M=10)
y_nao_linear    = sistema_nao_linear(x_quantizado)
y_nao_causal    = sistema_nao_causal(x_quantizado, M=10)

print("\n" + "=" * 55)
print("       SISTEMAS DISCRETOS - CLASSIFICAÇÃO")
print("=" * 55)
print("  Média Móvel    : Linear | Invariante | Causal | BIBO")
print("  Retificador    : Não-Linear | Causal | BIBO")
print("  Média Centrada : Linear | Invariante | Não-Causal | BIBO")
print("=" * 55)

# =============================================================
# MÓDULO 9: VISUALIZAÇÕES
# =============================================================

# -------------------------------------------------------
# FIGURA 1: Processo de Aquisição ADC
# -------------------------------------------------------
fig1, axes = plt.subplots(4, 1, figsize=(14, 12))
fig1.suptitle("FIGURA 1 — Processo de Aquisição ADC em Sistema Embarcado",
              fontsize=13, fontweight='bold', color=CORES['ciano'], y=0.98)

# Sinal contínuo
ax = axes[0]
ax.plot(t_cont[:3000], x_cont[:3000],
        color=CORES['ciano'], lw=1.2, label='Sinal Analógico (contínuo)')
ax.set_ylabel("Amplitude [V]")
ax.set_title("Sinal Analógico — Sensor de Entrada", color=CORES['amarelo'])
ax.legend(loc='upper right')
ax.grid(True)

# Sinal amostrado (com ruído)
ax = axes[1]
ax.plot(t_disc[:150], x_ruidoso[:150],
        color=CORES['verde'], lw=1, label='Sinal + Ruído Térmico')
ax.stem(t_disc[:150], x_ruidoso[:150],
        linefmt='#00ff8833', markerfmt='o', basefmt=' ')
ax.set_ylabel("Amplitude [V]")
ax.set_title(f"Sinal Amostrado — Fs = {Fs} Hz  |  SNR = {snr_db} dB",
             color=CORES['amarelo'])
ax.legend(loc='upper right')
ax.grid(True)

# Sinal quantizado
ax = axes[2]
ax.step(t_disc[:150], x_quantizado[:150],
        color=CORES['magenta'], lw=1.5, label=f'Saída ADC {bits_adc}-bit')
ax.plot(t_disc[:150], x_ruidoso[:150],
        color=CORES['verde'], lw=0.8, alpha=0.4, label='Antes da Quantização')
ax.set_ylabel("Amplitude [V]")
ax.set_title(f"Sinal Quantizado — ADC {bits_adc} bits  |  {niveis} níveis  |  LSB = {lsb*1e3:.3f} mV",
             color=CORES['amarelo'])
ax.legend(loc='upper right')
ax.grid(True)

# Erro de quantização
ax = axes[3]
ax.plot(t_disc[:150], erro_quant[:150],
        color=CORES['laranja'], lw=1, label='Erro de Quantização e[n]')
ax.axhline(y= lsb/2, color=CORES['vermelho'], ls='--', lw=0.8, label=f'+LSB/2 = {lsb/2*1e3:.3f} mV')
ax.axhline(y=-lsb/2, color=CORES['vermelho'], ls='--', lw=0.8, label=f'-LSB/2')
ax.set_ylabel("Amplitude [V]")
ax.set_xlabel("Tempo [s]")
ax.set_title(f"Erro de Quantização  |  SQNR = {sqnr_db:.1f} dB  (teórico: {sqnr_teorico:.1f} dB)",
             color=CORES['amarelo'])
ax.legend(loc='upper right')
ax.grid(True)

plt.tight_layout()
plt.savefig("fig1_aquisicao_adc.png", dpi=150, bbox_inches='tight')
plt.show()

# -------------------------------------------------------
# FIGURA 2: Sequências Elementares
# -------------------------------------------------------
fig2, axes = plt.subplots(3, 2, figsize=(14, 12))
fig2.suptitle("FIGURA 2 — Sequências Elementares Discretas",
              fontsize=13, fontweight='bold', color=CORES['ciano'])

n_plot = np.arange(-20, 60)

# Impulso
ax = axes[0, 0]
imp_plot = (n_plot == 0).astype(float)
ax.stem(n_plot, imp_plot, linefmt=CORES['ciano'],
        markerfmt='o', basefmt=CORES['roxo'])
ax.set_title(r"Impulso Unitário  $\delta[n]$", color=CORES['amarelo'])
ax.set_xlabel("n"); ax.set_ylabel("Amplitude"); ax.grid(True)

# Degrau
ax = axes[0, 1]
deg_plot = (n_plot >= 0).astype(float)
ax.stem(n_plot, deg_plot, linefmt=CORES['verde'],
        markerfmt='o', basefmt=CORES['roxo'])
ax.set_title(r"Degrau Unitário  $u[n]$", color=CORES['amarelo'])
ax.set_xlabel("n"); ax.set_ylabel("Amplitude"); ax.grid(True)

# Rampa
ax = axes[1, 0]
rmp_plot = np.where(n_plot >= 0, n_plot, 0).astype(float)
ax.stem(n_plot, rmp_plot, linefmt=CORES['magenta'],
        markerfmt='o', basefmt=CORES['roxo'])
ax.set_title(r"Rampa Unitária  $r[n] = n \cdot u[n]$", color=CORES['amarelo'])
ax.set_xlabel("n"); ax.set_ylabel("Amplitude"); ax.grid(True)

# Exponencial real
ax = axes[1, 1]
exp_plot = (0.92 ** n_plot) * (n_plot >= 0).astype(float)
ax.stem(n_plot, exp_plot, linefmt=CORES['amarelo'],
        markerfmt='o', basefmt=CORES['roxo'])
ax.set_title(r"Exponencial Real  $a^n u[n],\; a=0.92$", color=CORES['amarelo'])
ax.set_xlabel("n"); ax.set_ylabel("Amplitude"); ax.grid(True)

# Exponencial complexa - Parte Real
ax = axes[2, 0]
ec_plot = np.exp(1j * 0.15 * np.pi * n_plot) * (n_plot >= 0).astype(float)
ax.stem(n_plot, ec_plot.real, linefmt=CORES['laranja'],
        markerfmt='o', basefmt=CORES['roxo'])
ax.set_title(r"Exp. Complexa — Real:  $\cos(\omega_0 n)\,u[n]$",
             color=CORES['amarelo'])
ax.set_xlabel("n"); ax.set_ylabel("Re{x[n]}"); ax.grid(True)

# Exponencial complexa - Parte Imaginária
ax = axes[2, 1]
ax.stem(n_plot, ec_plot.imag, linefmt=CORES['roxo'],
        markerfmt='o', basefmt=CORES['roxo'])
ax.set_title(r"Exp. Complexa — Imag:  $\sin(\omega_0 n)\,u[n]$",
             color=CORES['amarelo'])
ax.set_xlabel("n"); ax.set_ylabel("Im{x[n]}"); ax.grid(True)

plt.tight_layout()
plt.savefig("fig2_sequencias_elementares.png", dpi=150, bbox_inches='tight')
plt.show()

# -------------------------------------------------------
# FIGURA 3: Operações com Sinais
# -------------------------------------------------------
fig3, axes = plt.subplots(3, 2, figsize=(14, 12))
fig3.suptitle("FIGURA 3 — Operações com Sinais Discretos",
              fontsize=13, fontweight='bold', color=CORES['ciano'])

# Sinal original
ax = axes[0, 0]
ax.stem(n_op, x_op, linefmt=CORES['ciano'],
        markerfmt='o', basefmt=CORES['roxo'])
ax.set_title(r"Sinal Original  $x[n]$", color=CORES['amarelo'])
ax.set_xlabel("n"); ax.set_ylabel("Amplitude"); ax.grid(True)

# Deslocamento
ax = axes[0, 1]
ax.stem(n_op, x_atrasado, linefmt=CORES['verde'],
        markerfmt='o', basefmt=CORES['roxo'])
ax.set_title(rf"Deslocamento  $x[n - {n0}]$  (atraso)", color=CORES['amarelo'])
ax.set_xlabel("n"); ax.set_ylabel("Amplitude"); ax.grid(True)

# Inversão
ax = axes[1, 0]
ax.stem(n_op, x_invertido, linefmt=CORES['magenta'],
        markerfmt='o', basefmt=CORES['roxo'])
ax.set_title(r"Inversão  $x[-n]$  (reflexão)", color=CORES['amarelo'])
ax.set_xlabel("n"); ax.set_ylabel("Amplitude"); ax.grid(True)

# Escalonamento
ax = axes[1, 1]
ax.stem(n_op, x_escalonado, linefmt=CORES['amarelo'],
        markerfmt='o', basefmt=CORES['roxo'])
ax.plot(n_op, x_op, color=CORES['ciano'], lw=0.8,
        alpha=0.4, label='x[n] original')
ax.set_title(r"Escalonamento  $y[n] = 2 \cdot x[n]$", color=CORES['amarelo'])
ax.set_xlabel("n"); ax.set_ylabel("Amplitude")
ax.legend(); ax.grid(True)

# Soma
ax = axes[2, 0]
ax.stem(n_op, x_soma, linefmt=CORES['laranja'],
        markerfmt='o', basefmt=CORES['roxo'])
ax.set_title(r"Soma  $y[n] = x[n] + x[n-20]$", color=CORES['amarelo'])
ax.set_xlabel("n"); ax.set_ylabel("Amplitude"); ax.grid(True)

# Comparativo: todas as operações
ax = axes[2, 1]
ax.plot(n_op, x_op,        color=CORES['ciano'],    lw=1.5, label='Original')
ax.plot(n_op, x_atrasado,  color=CORES['verde'],    lw=1.5, label='Atrasado')
ax.plot(n_op, x_invertido, color=CORES['magenta'],  lw=1.5, label='Invertido')
ax.plot(n_op, x_escalonado,color=CORES['amarelo'],  lw=1.0, label='Escalonado')
ax.set_title("Comparativo — Todas as Operações", color=CORES['amarelo'])
ax.set_xlabel("n"); ax.set_ylabel("Amplitude")
ax.legend(fontsize=8); ax.grid(True)

plt.tight_layout()
plt.savefig("fig3_operacoes_sinais.png", dpi=150, bbox_inches='tight')
plt.show()

# -------------------------------------------------------
# FIGURA 4: Análise Espectral (FFT)
# -------------------------------------------------------
fig4, axes = plt.subplots(3, 1, figsize=(14, 10))
fig4.suptitle("FIGURA 4 — Análise Espectral via FFT (Transformada de Fourier Discreta)",
              fontsize=13, fontweight='bold', color=CORES['ciano'])

# Espectro do sinal original
ax = axes[0]
ax.plot(freqs, X_mag, color=CORES['ciano'], lw=1.5)
ax.axvline(f1,  color=CORES['vermelho'],  ls='--', lw=1.2, label=f'f₁ = {f1} Hz')
ax.axvline(f2,  color=CORES['verde'],     ls='--', lw=1.2, label=f'f₂ = {f2} Hz')
ax.axvline(f3,  color=CORES['amarelo'],   ls='--', lw=1.2, label=f'f₃ = {f3} Hz')
ax.set_title("Espectro de Magnitude — Sinal Amostrado", color=CORES['amarelo'])
ax.set_ylabel("|X(f)| [V]")
ax.set_xlim([0, Fs / 2])
ax.legend(); ax.grid(True)

# Espectro do sinal quantizado
ax = axes[1]
ax.plot(freqs, Xq_mag, color=CORES['magenta'], lw=1.5)
ax.axvline(f1, color=CORES['vermelho'],  ls='--', lw=1.0, label=f'f₁ = {f1} Hz')
ax.axvline(f2, color=CORES['verde'],     ls='--', lw=1.0, label=f'f₂ = {f2} Hz')
ax.axvline(f3, color=CORES['amarelo'],   ls='--', lw=1.0, label=f'f₃ = {f3} Hz')
ax.set_title(f"Espectro de Magnitude — Sinal Quantizado ({bits_adc} bits)",
             color=CORES['amarelo'])
ax.set_ylabel("|Xq(f)| [V]")
ax.set_xlim([0, Fs / 2])
ax.legend(); ax.grid(True)

# Espectro do erro de quantização
ax = axes[2]
ax.plot(freqs, Eq_mag, color=CORES['laranja'], lw=1)
ax.axhline(y=np.mean(Eq_mag), color=CORES['vermelho'],
           ls='--', lw=1.2, label=f'Nível médio: {np.mean(Eq_mag)*1e3:.3f} mV')
ax.set_title("Espectro do Erro de Quantização — Ruído de Quantização",
             color=CORES['amarelo'])
ax.set_ylabel("|E(f)| [V]")
ax.set_xlabel("Frequência [Hz]")
ax.set_xlim([0, Fs / 2])
ax.legend(); ax.grid(True)

plt.tight_layout()
plt.savefig("fig4_analise_espectral.png", dpi=150, bbox_inches='tight')
plt.show()

# -------------------------------------------------------
# FIGURA 5: Classificação de Sistemas
# -------------------------------------------------------
fig5, axes = plt.subplots(2, 2, figsize=(14, 10))
fig5.suptitle("FIGURA 5 — Classificação de Sistemas Discretos",
              fontsize=13, fontweight='bold', color=CORES['ciano'])

t_sys = t_disc[:300]

# Entrada
ax = axes[0, 0]
ax.plot(t_sys, x_quantizado[:300],
        color=CORES['ciano'], lw=1.2, label='Entrada x[n]')
ax.set_title("Entrada — Sinal Adquirido pelo ADC", color=CORES['amarelo'])
ax.set_ylabel("Amplitude [V]"); ax.legend(); ax.grid(True)

# Sistema LTI — Média Móvel
ax = axes[0, 1]
ax.plot(t_sys, x_quantizado[:300],
        color=CORES['ciano'], lw=0.8, alpha=0.4, label='Entrada x[n]')
ax.plot(t_sys, y_media_movel[:300],
        color=CORES['verde'], lw=1.5,
        label='Saída — Média Móvel (M=10)')
ax.set_title("Sistema LTI: Linear | Invariante | Causal | BIBO",
             color=CORES['amarelo'])
ax.set_ylabel("Amplitude [V]"); ax.legend(fontsize=9); ax.grid(True)

# Sistema Não-Linear — Retificador
ax = axes[1, 0]
ax.plot(t_sys, x_quantizado[:300],
        color=CORES['ciano'], lw=0.8, alpha=0.4, label='Entrada x[n]')
ax.plot(t_sys, y_nao_linear[:300],
        color=CORES['laranja'], lw=1.5,
        label='Saída — Retificador')
ax.fill_between(t_sys, 0, y_nao_linear[:300],
                alpha=0.2, color=CORES['laranja'])
ax.set_title("Sistema Não-Linear: Retificador de Meia Onda",
             color=CORES['amarelo'])
ax.set_xlabel("Tempo [s]")
ax.set_ylabel("Amplitude [V]"); ax.legend(fontsize=9); ax.grid(True)

# Sistema Não-Causal — Média Centrada
ax = axes[1, 1]
ax.plot(t_sys, x_quantizado[:300],
        color=CORES['ciano'], lw=0.8, alpha=0.4, label='Entrada x[n]')
ax.plot(t_sys, y_nao_causal[:300],
        color=CORES['roxo'], lw=1.5,
        label='Saída — Média Centrada (não-causal)')
ax.plot(t_sys, y_media_movel[:300],
        color=CORES['verde'], lw=1.0, ls='--',
        alpha=0.6, label='Média Móvel (causal)')
ax.set_title("Sistema Não-Causal vs Causal — Comparativo",
             color=CORES['amarelo'])
ax.set_xlabel("Tempo [s]")
ax.set_ylabel("Amplitude [V]"); ax.legend(fontsize=9); ax.grid(True)

plt.tight_layout()
plt.savefig("fig5_classificacao_sistemas.png", dpi=150, bbox_inches='tight')
plt.show()

# -------------------------------------------------------
# FIGURA 6: Energia e Potência
# -------------------------------------------------------
fig6, axes = plt.subplots(1, 2, figsize=(14, 6))
fig6.suptitle("FIGURA 6 — Energia e Potência dos Sinais Analisados",
              fontsize=13, fontweight='bold', color=CORES['ciano'])

sinais_nomes   = ['Original', 'Com Ruído', 'Quantizado', 'Erro Quant.', 'Exp. Real']
energias       = [E_orig, E_ruid, E_quant, E_eq, E_exp]
potencias      = [P_orig, P_ruid, P_quant, P_eq, P_exp]
cores_barras   = [CORES['ciano'], CORES['verde'], CORES['magenta'],
                  CORES['laranja'], CORES['amarelo']]

# Gráfico de Energia
ax = axes[0]
bars = ax.bar(sinais_nomes, energias, color=cores_barras,
              edgecolor='#ffffff33', linewidth=0.8)
ax.set_title("Energia Total  $E = \sum |x[n]|^2$", color=CORES['amarelo'])
ax.set_ylabel("Energia [J]")
ax.set_xticklabels(sinais_nomes, rotation=15, fontsize=9)
ax.grid(True, axis='y')
for bar, val in zip(bars, energias):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.01,
            f'{val:.1f}', ha='center', va='bottom', fontsize=8,
            color=CORES['branco'])

# Gráfico de Potência
ax = axes[1]
bars = ax.bar(sinais_nomes, potencias, color=cores_barras,
              edgecolor='#ffffff33', linewidth=0.8)
ax.set_title("Potência Média  $P = \\frac{1}{N}\sum |x[n]|^2$",
             color=CORES['amarelo'])
ax.set_ylabel("Potência [W]")
ax.set_xticklabels(sinais_nomes, rotation=15, fontsize=9)
ax.grid(True, axis='y')
for bar, val in zip(bars, potencias):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() * 1.01,
            f'{val:.4f}', ha='center', va='bottom', fontsize=8,
            color=CORES['branco'])

plt.tight_layout()
plt.savefig("fig6_energia_potencia.png", dpi=150, bbox_inches='tight')
plt.show()

# =============================================================
# RELATÓRIO FINAL NO CONSOLE
# =============================================================
print("\n" + "=" * 55)
print("              RELATÓRIO FINAL DA SIMULAÇÃO")
print("=" * 55)
print(f"  Figuras geradas:")
print(f"    fig1_aquisicao_adc.png")
print(f"    fig2_sequencias_elementares.png")
print(f"    fig3_operacoes_sinais.png")
print(f"    fig4_analise_espectral.png")
print(f"    fig5_classificacao_sistemas.png")
print(f"    fig6_energia_potencia.png")
print(f"\n  Componentes espectrais detectadas:")
print(f"    f1 = {f1} Hz  |  A1 = {A1} V")
print(f"    f2 = {f2} Hz  |  A2 = {A2} V")
print(f"    f3 = {f3} Hz  |  A3 = {A3} V")
print(f"\n  Qualidade do ADC:")
print(f"    Bits        : {bits_adc}")
print(f"    Níveis      : {niveis}")
print(f"    LSB         : {lsb*1e3:.4f} mV")
print(f"    SQNR medido : {sqnr_db:.2f} dB")
print(f"    SQNR teórico: {sqnr_teorico:.2f} dB")
print("=" * 55)
print("  Simulação concluída com sucesso.")
print("=" * 55)
