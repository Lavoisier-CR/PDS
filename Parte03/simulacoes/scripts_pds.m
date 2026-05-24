%% PROCESSAMENTO DIGITAL DE SINAIS - ESTUDO DIRIGIDO PARTE 3
% Códigos desenvolvidos para rodar no MATLAB ou Octave.
clear; clc; close all;

%% Questão 1: Senoide Discreta e FFT
fprintf('Executando Questão 1...\n');
N = 128;
n = 0:N-1;
f0 = 0.1; % Frequência normalizada
x1 = sin(2*pi*f0*n);

X1 = fft(x1);
f_eixo = (0:N-1)/N;

figure;
subplot(2,1,1);
stem(n, x1, 'filled');
title('Q1 - Sinal no Domínio do Tempo');
xlabel('Amostras (n)'); ylabel('Amplitude'); grid on;

subplot(2,1,2);
plot(f_eixo, abs(X1)/N, 'LineWidth', 1.5);
title('Q1 - Espectro de Magnitude via FFT');
xlabel('Frequência Normalizada (f)'); ylabel('Magnitude'); grid on;

%% Questão 2: Soma de duas Senoides
fprintf('Executando Questão 2...\n');
f1 = 0.1;
f2 = 0.25;
x2 = sin(2*pi*f1*n) + sin(2*pi*f2*n);
X2 = fft(x2);

figure;
plot(f_eixo, abs(X2)/N, 'LineWidth', 1.5);
title('Q2 - Espectro da Soma de duas Senoides');
xlabel('Frequência Normalizada'); ylabel('Magnitude'); grid on;

%% Questão 3: Fenômeno de Aliasing
fprintf('Executando Questão 3...\n');
% Sinal original de alta frequência simulado sob uma taxa original implícita
n_alta = 0:127;
f_alta = 0.85; % Acima de Nyquist se considerarmos os limites padrão
x3_original = sin(2*pi*f_alta*n_alta);

% Subamostragem (redução da taxa por fator de 2)
x3_sub = x3_original(1:2:end);
N_sub = length(x3_sub);
f_eixo_sub = (0:N_sub-1)/N_sub;

figure;
subplot(2,1,1);
plot((0:127)/128, abs(fft(x3_original))/128);
title('Q3 - Espectro Original (Frequência Alta)'); grid on;
subplot(2,1,2);
plot(f_eixo_sub, abs(fft(x3_sub))/N_sub);
title('Q3 - Espectro com Aliasing (Taxa Reduzida)'); grid on;

%% Questão 4: Janelamento e Vazamento Espectral
fprintf('Executando Questão 4...\n');
f_vazamento = 0.115; % Frequência não múltipla inteira de 1/N para forçar vazamento
x4 = sin(2*pi*f_vazamento*n);

X4_retangular = fft(x4);
X4_hamming = fft(x4 .* hamming(N)');

figure;
plot(f_eixo, 20*log10(abs(X4_retangular)/N), 'b', 'LineWidth', 1.2); hold on;
plot(f_eixo, 20*log10(abs(X4_hamming)/N), 'r', 'LineWidth', 1.5);
title('Q4 - Comparação de Janelamento (Escala em dB)');
legend('Sem Janela (Retangular)', 'Janela de Hamming');
xlabel('Frequência Normalizada'); ylabel('Magnitude (dB)'); grid on;

%% Questão 5: Sinal Senoidal com Ruído Aditivo
fprintf('Executando Questão 5...\n');
ruido = 1.8 * randn(1, N); % Ruído Gaussiano de alta variância
x5 = sin(2*pi*0.15*n) + ruido;
X5 = fft(x5);

figure;
subplot(2,1,1);
plot(n, x5); title('Q5 - Sinal + Ruído no Tempo'); grid on;
subplot(2,1,2);
plot(f_eixo, abs(X5)/N); title('Q5 - Análise Espectral na Presença de Ruído'); grid on;

%% Questão 6: DFT Direta vs FFT
fprintf('Executando Questão 6...\n');
x6 = [1, 2, 3, 4, 5, 6, 7, 8]; % Sinal curto
N6 = length(x6);

% DFT Direta via laço aninhado
X6_direta = zeros(1, N6);
tic;
for k = 0:N6-1
    for m = 0:N6-1
        X6_direta(k+1) = X6_direta(k+1) + x6(m+1) * exp(-1i*2*pi*k*m/N6);
    end
end
tempo_direta = toc;

% FFT Otimizada
tic;
X6_fft = fft(x6);
tempo_fft = toc;

fprintf('Diferença máxima entre DFT e FFT: %e\n', max(abs(X6_direta - X6_fft)));
fprintf('Tempo DFT Direta: %.6f s | Tempo FFT: %.6f s\n', tempo_direta, tempo_fft);

%% Questão 7: Resposta ao Impulso de H(z) = 1 / (1 - 0.8z^-1)
fprintf('Executando Questão 7...\n');
b = 1;
a = [1, -0.8];
impulso = [1, zeros(1, 49)]; % Impulso unitário delta[n] com 50 amostras
h = filter(b, a, impulso);

figure;
stem(0:49, h, 'filled', 'm');
title('Q7 - Resposta ao Impulso de H(z)');
xlabel('Amostras (n)'); ylabel('h[n]'); grid on;

%% Questão 8: Resolução Espectral vs Número de Amostras
fprintf('Executando Questão 8...\n');
f_res = 0.1;
N_curto = 32;
N_longo = 256;

x_curto = sin(2*pi*f_res*(0:N_curto-1));
x_longo = sin(2*pi*f_res*(0:N_longo-1));

figure;
subplot(2,1,1);
plot((0:N_curto-1)/N_curto, abs(fft(x_curto))/N_curto, 'o-');
title('Q8 - Resolução com Poucas Amostras (N=32)'); grid on;
subplot(2,1,2);
plot((0:N_longo-1)/N_longo, abs(fft(x_longo))/N_longo);
title('Q8 - Resolução com Muitas Amostras (N=256)'); grid on;

%% Questão 9: Componentes Harmônicas e Vibrações
fprintf('Executando Questão 9...\n');
f_fundamental = 0.05;
x9 = sin(2*pi*f_fundamental*n) + 0.5*sin(2*pi*(3*f_fundamental)*n); % Fundamental + 3º Harmônico
X9 = fft(x9);

figure;
plot(f_eixo, abs(X9)/N);
title('Q9 - Análise de Harmônicos para Diagnóstico Mecânico');
xlabel('Frequência Normalizada'); grid on;

%% Questão 10: Análise de Sinal Real/Sintético Prático (Sinal DTMF)
fprintf('Executando Questão 10...\n');
fs_audio = 8000;
t_audio = 0:1/fs_audio:0.1; % 100 ms de sinal
% Simulação da tecla '1' do telefone (697 Hz + 1209 Hz)
sinal_dtmf = sin(2*pi*697*t_audio) + sin(2*pi*1209*t_audio);

L = length(sinal_dtmf);
X_dtmf = fft(sinal_dtmf);
f_eixo_hz = (0:L-1)*fs_audio/L;

figure;
subplot(2,1,1);
plot(t_audio, sinal_dtmf);
xlim([0 0.02]); title('Q10 - Sinal de Áudio Real (DTMF Tecla 1) no Tempo');
xlabel('Tempo (s)'); ylabel('Amplitude'); grid on;

subplot(2,1,2);
plot(f_eixo_hz(1:floor(L/2)), abs(X_dtmf(1:floor(L/2)))/L);
title('Q10 - Espectro de Frequências em Hz');
xlabel('Frequência (Hz)'); ylabel('Magnitude'); grid on;

fprintf('Simulações finalizadas com sucesso!\n');
