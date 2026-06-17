# Processamento Digital de Sinais (PDS) - Estudo Dirigido: Filtros Digitais
**Instituição:** Instituto Federal da Paraíba (IFPB)  
**Curso:** Engenharia da Computação / Engenharia de Telemática  
**Discente:** Lavoisier Chaves Ramos  

---

## 📁 Estrutura do Repositório
Conforme as diretrizes metodológicas estabelecidas, o repositório encontra-se mapeado da seguinte forma:
* `teoria/`: Contém a fundamentação conceitual detalhada.
* `simulacoes/`: Códigos de implementação em Python contendo as modelagens matemáticas e simulações.
* `resultados/`: Imagens e gráficos gerados automaticamente pelas simulações.
* `README.md`: Este relatório executivo integrando teoria, prática e conclusões.

---

## 📚 Resumo Teórico Fundamentado

Os filtros digitais operam como Sistemas Lineares Invariantes no Tempo (LTI), cuja principal propriedade é a modificação seletiva do espectro de frequências de uma sequência discreta de entrada. De acordo com a literatura clássica de **Oppenheim & Schafer**, a resposta em frequência $H(e^{j\omega})$ dita matematicamente as alterações de magnitude e fase impostas ao sinal original.

### 1. Classificação Estrutural: FIR vs IIR
* **Filtros FIR (Finite Impulse Response):** Caracterizados por uma resposta ao impulso de duração estritamente finita. Matematicamente, não possuem realimentação (são não recursivos). Segundo **Proakis & Manolakis**, sua equação de diferenças é expressa exclusivamente por coeficientes de avanço do sinal de entrada ($b_k$):
    $$y[n] = \sum_{k=0}^{M} b_k x[n-k]$$
    *Vantagens primordiais:* Estabilidade absoluta inerente (todos os polos estão localizados nativamente na origem $z=0$) e capacidade de atingir **fase linear exata**.
* **Filtros IIR (Infinite Impulse Response):** Apresentam resposta ao impulso de duração teoricamente infinita devido à realimentação de saídas anteriores (sistemas recursivos). A equação de diferenças engloba os coeficientes $b_k$ e $a_m$:
    $$y[n] = \sum_{k=0}^{M} b_k x[n-k] - \sum_{m=1}^{N} a_m y[n-m]$$
    *Vantagens primordiais:* Alta seletividade espectral utilizando ordens computacionais drasticamente menores se comparadas aos filtros FIR.

### 2. Resposta em Frequência, Fase e Atraso de Grupo
* **Resposta em Frequência & Fase:** A magnitude de $H(e^{j\omega})$ define a atenuação ou ganho em dB das componentes de frequência. A fase delimita o deslocamento angular temporal introduzido.
* **Atraso de Grupo (Group Delay):** Definido como a derivada negativa da fase em relação à frequência ($\tau_g(\omega) = -\frac{d\theta(\omega)}{d\omega}$). Em termos físicos descritos por **Lathi**, se o atraso de grupo for constante (fase linear), todas as componentes harmônicas sofrem rigorosamente o mesmo atraso temporal ao atravessar o sistema, blindando o sinal contra distorções de fase. Isso é crítico em comunicações digitais e modulações digitais complexas.

### 3. Análise de Estabilidade no Domínio Z
A estabilidade de um filtro digital IIR está umbilicalmente ligada ao mapeamento de sua função de transferência $H(z)$. Um sistema causal é BIBO estável (Bounded-Input Bounded-Output) se, e somente se, **todos os seus polos complexos estiverem localizados estritamente dentro do círculo unitário** no plano Z ($|p_i| < 1$). Caso algum polo se desloque para fora do círculo unitário, qualquer perturbação residual resultará em oscilação geométrica divergente, inutilizando o hardware.

---

## 📈 Discussão Técnica das Questões e Resultados

### Q1 a Q3. Filtragem de Componentes e Redução de Ruído
* **Discussão:** Sinais contaminados por alta frequência ou ruído branco gaussiano foram submetidos a estruturas FIR (janelamento) e IIR (Butterworth). O filtro FIR exige uma ordem de $N=80$ para atingir atenuações severas nas bandas de rejeição, enquanto o filtro IIR Butterworth cumpre papel equivalente com ordem $N=4$. O decaimento assintótico do IIR preserva a banda passante com transição suave (característica maximalmente plana do Butterworth).

### Q4 e Q6. Resposta em Frequência e Resposta ao Impulso
* A análise do gráfico de magnitude (`q4_resposta_frequencia.png`) comprova a economia de recursos do IIR: um filtro leve de 4ª ordem replica a rejeição de um FIR pesado de 80 coeficientes.
* O gráfico da resposta ao impulso (`q6_resposta_impulso.png`) elucida a física do sistema: o gráfico FIR zera de forma abrupta após a amostra $n=80$, enquanto o gráfico IIR decai de maneira geométrica assintótica tendendo a zero, mas prolongando-se infinitamente devido aos coeficientes de feedback ($a_m$).

### Q5. Análise do Plano Z
* O gráfico gerado (`q5_polos_zeros.png`) expõe os polos do filtro Butterworth projetado. Nota-se que os polos estão dispostos simetricamente em formato de arco bem recuados para o interior do círculo unitário, o que atesta a **estabilidade robusta** e margem segura contra oscilações e transbordamentos numéricos em ponto fixo.

### Q8 e Q9. Comportamento de Fase e Atraso de Grupo
* O filtro FIR exibe uma resposta de fase perfeitamente retilínea (fase linear). Como consequência direta, seu gráfico de Atraso de Grupo é uma linha horizontal perfeitamente constante.
* Em contrapartida, o filtro IIR Butterworth apresenta severas distorções de fase não-lineares, especialmente nas proximidades da frequência de corte ($\omega_c = 20\text{ Hz}$), onde o atraso de grupo sofre um pico agudo. Em sistemas de áudio de alta fidelidade ou transmissão de dados estruturados, essa distorção de fase dispersaria os pacotes de energia harmônica do sinal no tempo.

---

## 🚜 Solução do Problema Norteador (Metodologia PBL)

**Cenário:** Ruídos ambientais e de chaveamento elétrico corrompendo os dados analógicos de sensores em um sistema agrícola, prejudicando algoritmos de tomada de decisão baseados em Inteligência Artificial Embarcada (**TinyML**).

### Engenharia da Solução Aplicada:
Para o problema proposto, implementamos um caso prático replicado na **Questão 10** (`q10_aplicacao_pratica.png`). O sinal brutificado do sensor continha uma oscilação parasita espúria (simulando a indução magnética de acionamento de uma bomba d'água próxima a 120 Hz). 

1.  **Escolha Estrutural:** Optou-se por um filtro **IIR Butterworth de 2ª ordem** com frequência de corte agressiva em $5\text{ Hz}$.
2.  **Justificativa de Engenharia:** Como os dados agronômicos de solo (umidade, condutividade e temperatura) são variáveis de dinâmica extremamente lentas (frequências próximas a DC), as distorções de fase introduzidas pelo filtro IIR na região de transição não trazem prejuízos práticos à física do fenômeno. 
3.  **Vantagem Computacional:** A escolha do modelo IIR permitiu condicionar o sinal utilizando apenas **5 coeficientes multiplicadores** no microcontrolador embarcado. Se utilizássemos um filtro FIR para obter o mesmo nível de atenuação nessa banda tão estreita, precisaríamos de centenas de coeficientes, estourando a memória RAM/Flash restrita do dispositivo de borda (TinyML). O sinal purificado resultante permite o correto funcionamento das árvores de decisão e redes neurais embarcadas sem falsos positivos.

---

## 📚 Referências Bibliográficas

* **OPPENHEIM, Alan V.; SCHAFER, Ronald W.** *Discrete-Time Signal Processing*. 3rd ed. Prentice Hall, 2009.
* **PROAKIS, John G.; MANOLAKIS, Dimitris G.** *Digital Signal Processing: Principles, Algorithms, and Applications*. 4th ed. Pearson, 2007.
* **LATHI, B. P.** *Sinais e Sistemas Lineares*. 2ª ed. Porto Alegre: Bookman, 2007.
