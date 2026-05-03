<div align="center">
   <img src="https://www.ifpb.edu.br/imagens/logotipos/campina-grande/@@images/image-1200-119374a47048af0ba09197e64453797c.png" width="100px">

  <h2>Estudo Dirigido – Parte 2</h2>
  <h3>Convolução e Sistemas LTI</h3>
  <h4>Disciplina: Processamento Digital de Sinais</h4>
  <h4>Professor: Moacy Pereira da Silva</h4>
</div>

#### 1. Objetivos da Atividade

Ao final desta atividade, o estudante deverá ser capaz de:

- compreender o conceito de sistemas lineares e invariantes no tempo (LTI);
- interpretar a resposta ao impulso como elemento fundamental para a caracterização
    de sistemas discretos;
- calcular a saída de um sistema discreto por meio da convolução;
- relacionar convolução com equações de diferenças;
- analisar comportamento transitório, causalidade e estabilidade de sistemas;
- aplicar esses conceitos em problemas de filtragem e suavização de sinais.

#### 2. Resumo Teórico

Em Processamento Digital de Sinais, um sistema linear e invariante no tempo (LTI)
é completamente caracterizado por sua resposta ao impulso, denotada por $h[n]$.
Se a entrada do sistema é $x[n]$, a saída $y[n]$ é obtida pela convolução discreta entre
a entrada e a resposta ao impulso:

$$y[n] = x[n]∗ h[n]$$

ou, de forma expandida,

$$y[n] = \sum_{k=-\infty}^{+\infty} x[k] \, h[n - k]$$

Esse resultado mostra que a saída pode ser interpretada como uma composição ponderada de versões deslocadas da resposta ao impulso.

##### 2.1 Resposta ao impulso
A resposta ao impulso $h[n]$ corresponde à saída do sistema quando a entrada é o impulso
discreto $\delta[n]$. Como qualquer sequência pode ser decomposta em impulsos deslocados,
conhecer $h[n]$ equivale a conhecer completamente o sistema LTI.


##### 2.2 Convolução
A convolução é a operação matemática que permite determinar a saída de um sistema LTI
para qualquer entrada conhecida. Em termos práticos, ela aparece em aplicações como:

- filtragem de ruídos em sensores;
- suavização de medições;
- média móvel;
- análise da dinâmica de sistemas discretos.

##### 2.3 Equações de diferenças
Muitos sistemas discretos são descritos por equações de diferenças, como por exemplo:

$$y[n]− ay[n− 1] = bx[n]$$

ou ainda

$$y[n] = ay[n− 1] + bx[n]$$

Essas equações descrevem a evolução temporal da saída e são análogas às equações
diferenciais no caso contínuo.

##### 2.4 Resposta transitória
A resposta transitória corresponde ao comportamento inicial do sistema após a aplicação
de uma entrada. Em sistemas com memória, a saída pode levar alguns instantes para
atingir um regime mais estável ou permanente.

##### 2.5 Causalidade e estabilidade
Um sistema discreto é:

- causal se a saída em um instante depende apenas de valores presentes e passados
    da entrada;
- estável no sentido BIBO se toda entrada limitada produzir saída limitada.
Para sistemas LTI, uma condição suficiente e necessária de estabilidade BIBO é:

$$y[n] = \sum_{n=-\infty}^{+\infty} \left\|h[n]\right\|<\infty$$

#### 3. Conteúdos a Serem Estudados

Nesta parte do estudo dirigido, o aluno deverá revisar e compreender os seguintes tópicos:

- resposta ao impulso;
- convolução discreta;
- equações de diferenças;
- resposta transitória;
- estabilidade e causalidade.

#### 4. Aplicações Práticas

Os conceitos desta atividade aparecem em diversos problemas reais de engenharia, tais
como:

- filtragem de sinais provenientes de sensores;
- suavização de sinais ruidosos;
- implementação de filtros digitais simples;
- análise temporal de sistemas discretos.

#### 5. Atividades Propostas

###### Atividade 1 – Interpretação conceitual
Responda, com suas próprias palavras:
1) O que significa afirmar que um sistema é linear e invariante no tempo?
2) Por que a resposta ao impulso é suficiente para caracterizar um sistema LTI?
3) Qual o significado físico da convolução em sistemas discretos?
4) Qual a diferença entre resposta transitória e regime permanente?
5) O que se entende por sistema causal?
6) O que se entende por sistema estável?

###### Atividade 2 – Cálculo manual de convolução
Considere:

$x[n] =$ {1, 2, 1}   $h[n] =$ {1, 1}

1) Calcule manualmente a convolução $y[n] = x[n]∗h[n]$.
2) Apresente o resultado em forma de sequência.
3) Explique o significado do resultado obtido.


###### Atividade 3 – Sistema descrito por equação de diferenças
Considere o sistema:

$$y[n] = 0. 8 y[n− 1] + x[n]$$

admitindo condição inicial nula e entrada impulso $x[n] = \delta[n]$.
1) Determine os primeiros valores de $h[n]$ para $0 ≤ n≤ 5$.
2) A partir da resposta ao impulso obtida, discuta se o sistema parece ser estável.
3) Verifique se o sistema é causal.

###### Atividade 4 – Implementação computacional da convolução
Implemente no Octave ou MATLAB a convolução das sequências da Atividade 2 utilizando
o comando conv.

###### Código base

```
clc;
clear;
close all;

x = [1 2 1];
h = [1 1];
y = conv(x,h);

disp(’Sequencia x[n]:’);
disp(x);
disp(’Sequencia h[n]:’);
disp(h);
disp(’Convolucao y[n] = x[n] * h[n]:’);
disp(y);

n = 0: length(y) -1;
stem(n,y,’filled ’);
grid on;
xlabel(’n’);
ylabel(’y[n]’);
title(’Resultado da convolucao discreta ’);
```

1) Execute o código e compare o resultado com o cálculo manual.
2) Explique a forma do sinal de saída obtido.
3) Modifique a entrada para $x[n] =${ 1 , 1 , 1 , 1 } e interprete o novo resultado.

##### Atividade 5 – Suavização de sinais
Considere um sinal de sensor representado por: $x[n] =${2 , 5 , 4 , 6 , 8 , 7 , 5 , 4}

e um filtro de média simples:  $h[n] = \frac{1}{3}$ {1 , 1 , 1}

1) Realize a convolução entre $x[n]$ e $h[n]$.
2) Apresente o gráfico do sinal original e do sinal filtrado.
3) Explique por que esse filtro atua como suavizador.

##### Código sugerido

```
clc;
clear;
close all;

x = [2 5 4 6 8 7 5 4];
h = (1/3) *[1 1 1];
y = conv(x,h);

figure;
stem (0: length(x)-1,x,’filled ’);
grid on;
xlabel(’n’);
ylabel(’x[n]’);
title(’Sinal original ’);
figure;
stem (0: length(y)-1,y,’filled ’);
grid on;
xlabel(’n’);
ylabel(’y[n]’);
title(’Sinal suavizado por convolucao ’);
```

###### Atividade 6 – Análise de estabilidade e causalidade
Para cada sistema abaixo, discuta se ele é causal e se pode ser considerado estável.

a) $y[n] = x[n] + x[n− 1]$

b) $y[n] = x[n + 1]$

c) $h[n] = (0.5)^nu[n]$

d) $h[n] = 2^nu[n]$

Justifique cada resposta com base nos conceitos estudados.

#### 6. Desafio Proposto

Considere um sistema de aquisição de dados em que a leitura de um sensor apresenta
ruídos rápidos e indesejados. Explique como a convolução com um filtro de média móvel
pode melhorar a qualidade do sinal medido.
Em sua resposta, procure comentar:

- qual é o papel da resposta ao impulso do filtro;
- por que ocorre a suavização;
- quais são as possíveis limitações desse procedimento.

#### 7. Orientações para Entrega

A entrega deverá conter:

- respostas teóricas das questões;
- cálculos manuais solicitados;
- códigos desenvolvidos em Octave ou MATLAB;
- gráficos gerados;
- comentários interpretativos sobre os resultados.
Sugere-se organizar a entrega em seções, identificando claramente cada atividade.

#### 8. Referências Bibliográficas

- OPPENHEIM, A. V.; SCHAFER, R. W. Discrete-Time Signal Processing. 3.
    ed. Pearson, 2010.
- PROAKIS, J. G.; MANOLAKIS, D. G. Digital Signal Processing: Principles,
    Algorithms, and Applications. 4. ed. Pearson, 2007.
- LYONS, R. G. Understanding Digital Signal Processing. 3. ed. Pearson,
    2011.

### Bom estudo!
