# Discussão Técnica dos Resultados das Simulações

## Questão 1: Identificação de Frequência Dominante
No gráfico gerado para o comprimento $N=128$, observa-se um pico perfeitamente nítido e espelhado. A frequência dominante detectada no eixo normalizado ocorre exatamente em $f_0 = 0.1$ (e sua imagem simétrica em $f = 0.9$, equivalente a $-0.1$). Isso confirma que a FFT mapeou perfeitamente o comportamento temporal para o espectral.

## Questão 2: Distinção de Duas Senoides
Ao somar componentes em $f_1 = 0.1$ e $f_2 = 0.25$, o domínio do tempo exibe uma forma de onda complexa de difícil interpretação visual direta. No entanto, no domínio da frequência, a FFT separa de forma limpa as duas senoides, exibindo dois picos isolados com magnitudes proporcionais. Isso ilustra o poder da análise espectral: transformar problemas complexos de sobreposição temporal em uma simples separação linear de frequências.

## Questão 3: Interpretação Física do Aliasing
Ao reduzir drasticamente a taxa de amostragem, frequências que antes estavam abaixo de Nyquist passam a violar o critério fundamental. No gráfico subamostrado, a componente original de alta frequência foi rebatida para uma frequência visivelmente mais baixa. Fisicamente, as amostras tornaram-se insuficientes para capturar a oscilação rápida, fazendo o sinal de alta frequência se comportar falsamente como um sinal lento.

## Questão 4: Mitigação de Vazamento Espectral por Janelamento
Com a aplicação da janela retangular (sinal sem janela), o espectro exibiu lóbulos secundários espalhados pelas bandas laterais, mascarando o comportamento real do sinal (vazamento). Ao aplicar a janela de **Hamming**, as descontinuidades nas extremidades do bloco temporal foram suavizadas. Como resultado, o gráfico em dB mostrou uma atenuação massiva dos lóbulos secundários, limpando o ruído de vazamento e provando sua eficácia no isolamento de componentes próximos.

## Questão 5: Isolamento de Sinais em Ambientes Ruidosos
Mesmo sob um ruído de forte intensidade (que deforma totalmente o sinal no domínio do tempo), a análise espectral via FFT conseguiu extrair o pico da senoide principal em $f = 0.15$. Como o ruído gaussiano espalha sua energia de forma uniforme por todo o espectro (ruído branco), a energia concentrada da senoide sobressai na frequência correta. Isso valida o uso da FFT como filtro conceitual para instrumentação e diagnóstico.

## Questão 6: DFT Direta vs Algoritmo FFT
Ambos os métodos apresentaram resultados numericamente idênticos, com erro de aproximação de ordem infinitesimal ($10^{-16}$). Contudo, o tempo de execução da DFT direta cresce exponencialmente, enquanto a FFT realiza o cálculo quase instantaneamente. Para vetores longos, o cálculo da DFT direta se torna computacionalmente proibitivo.

## Questão 7: Análise de Estabilidade via Resposta ao Impulso
A resposta ao impulso da função de transferência $H(z) = \frac{1}{1 - 0.8z^{-1}}$ decai exponencialmente conforme o número de amostras $n$ cresce, tendendo assintoticamente a zero ($h[n] = 0.8^n u[n]$). Como a sequência é absolutamente somável, conclui-se numericamente que o sistema é **estável**. Isso corrobora a teoria, pois o polo do sistema está em $z = 0.8$, localizado dentro do círculo unitário ($|0.8| < 1$).

## Questão 8: Influência do Número de Amostras na Resolução
Ao comparar $N=32$ com $N=256$, o pico espectral para $N=32$ se mostra largo, indefinido e com poucos pontos discretos de amostragem no eixo da frequência. Já com $N=256$, o pico espectral torna-se extremamente estreito, agudo e bem definido. Conclusão: quanto maior a janela de observação temporal (maior $N$), maior é a resolução espectral ($\Delta f = 1/N$), permitindo distinguir frequências muito próximas.

## Questão 9: Diagnóstico de Falhas por Harmônicos
O gráfico espectral gerado evidencia o pico fundamental acompanhado do seu 3º harmônico. Na engenharia mecânica, máquinas rotativas (motores, turbinas) geram padrões harmônicos específicos quando há desalinhamento, folga estrutural ou falhas em rolamentos. A identificação desses picos via FFT permite realizar a manutenção preditiva antes que ocorra um colapso mecânico catastrófico.

## Questão 10: Aplicação em Sinal Real (Sistema DTMF)
A simulação do sinal de áudio de telefonia DTMF (tecla '1') demonstrou de forma prática como as ferramentas se unem. O gráfico temporal apresenta um sinal oscilatório duplo distorcido. A análise espectral revelou com precisão cirúrgica dois picos de frequência absolutos em **697 Hz** e **1209 Hz**. Essa decodificação é exatamente a mesma realizada pelas centrais telefônicas para identificar qual número o usuário digitou.

---

## 🧭 Resolução do Problema Norteador (Metodologia PBL)

> *Como identificar, a partir do conteúdo espectral de um sinal real, informações relevantes sobre o comportamento dinâmico de um sistema físico e quais limitações práticas devem ser consideradas durante a aquisição e análise desses dados?*

**Resposta:**
Para identificar o comportamento dinâmico de um sistema físico real, aplicamos ferramentas computacionais como a FFT sobre os dados coletados no tempo, transformando os dados brutos em picos e bandas de energia no domínio da frequência. A posição desses picos entrega diretamente as frequências naturais de vibração, rotações por minuto, harmônicos indesejáveis ou portadoras de comunicação de um sistema.

Contudo, na prática da engenharia, devemos nos atentar a três limitações severas na aquisição:
1.  **O Aliasing:** Se o hardware coletar amostras de forma muito lenta, frequências altas se disfarçarão como baixas, gerando falsos diagnósticos. Deve-se usar filtros analógicos anti-aliasing antes da conversão digital.
2.  **O Vazamento Espectral:** Como janelas de leitura de dados são sempre finitas, o corte abrupto gera espalhamento de energia. O uso de janelas de suavização (como Hamming ou Blackman) é indispensável para limpar o espectro.
3.  **Ruído Aleatório:** Sinais reais vêm acompanhados de ruídos térmicos e magnéticos. Coletas com tempos de integração maiores ($N$ elevado) e médias espectrais ajudam a mitigar as flutuações e isolar a verdadeira dinâmica do sistema físico analisado.
