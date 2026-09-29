# Pitch ao Prof. Cugnasca — troca de tema do TCC

*Roteiro de fala para a reunião, ~7 minutos + perguntas. Levar impresso junto: a proposta (`build/proposta-tcc-consorcios.pdf`, com as datas revisadas) e os capítulos 1 e 2.*

---

## 1. A troca, em 30 segundos

Professor, a gente abandonou a estufa. O senhor já tinha apontado o problema: não estava claro qual era a pergunta de engenharia nem como saber se foi respondida. Olhando de perto, a plataforma do Laboratório de Embarcados é didática demais para a otimização ter ganho mensurável. O que foi feito da parte física, uns 15–20% do trabalho, vai para a própria disciplina de embarcados. Nada se perdeu, só mudou de destino.

O tema novo é a **avaliação computacional do mecanismo de contemplação dos consórcios brasileiros**.

## 2. O problema, em uma frase

O consórcio decide quem recebe o crédito a cada mês por **sorteio** e por **lance**, e essas regras foram fixadas por lei e por norma do Banco Central, sem que ninguém tenha comparado esse desenho com alternativas. A gente quer responder: **o desenho atual é eficiente, ou existe regra alternativa, dentro da mesma lei, que seja melhor para os participantes sem fragilizar o grupo?**

Por que importa: são mais de 12 milhões de participantes ativos e centenas de bilhões de reais em crédito comercializado por ano *(conferir os números no anuário ABAC antes da reunião)*. É um mecanismo de alocação operando na escala de um mercado de crédito nacional.

## 3. Por que é Engenharia de Computação, não Economia

Essa é a pergunta que eu espero do senhor, e acho que da banca também.

- **O objeto é um sistema.** Um grupo de consórcio é um conjunto de agentes autônomos disputando um recurso escasso e indivisível sob um protocolo explícito, com orçamento duro e informação privada. Desenho de mecanismo e simulação multiagente são as ferramentas para essa classe de sistema.
- **A dificuldade é computacional.** O jogo é dinâmico, com informação privada em duas dimensões (urgência e liquidez), população que diminui a cada contemplação e número de vagas que depende do saldo do fundo. Não tem solução fechada para grupo de tamanho real. Tem que simular, e aí o problema passa a ser provar que a simulação está certa.
- **A contribuição metodológica é de identificação com observação incompleta.** O Bacen não publica lance individual, só quantos foram contemplados por lance e por sorteio. Mostrar que dá para recuperar parâmetros de comportamento só a partir de agregado é algo que serve para qualquer sistema instrumentado só no agregado.

## 4. Como a gente vai fazer, em quatro passos

1. **Dados.** Painel com as bases públicas de consórcio do Bacen, recortado em imóveis e no regime da Resolução BCB 285/2023 (a partir de 2024, para não atravessar mudança de norma no meio da série).
2. **Modelo.** O grupo formalizado como jogo dinâmico e implementado como simulação. O comportamento de lance é uma política paramétrica simples, de 3 ou 4 parâmetros.
3. **Calibração e validação.** Os parâmetros são calibrados por método de momentos simulados: o modelo precisa reproduzir o que o Bacen mostra, e depois acertar momentos que ficaram de fora da calibração. Antes disso, o simulador tem que recuperar os equilíbrios conhecidos nos casos-limite que a literatura resolve analiticamente. Se não recuperar, isso vira resultado; não se ajusta até passar.
4. **Comparação.** O desenho atual contra dois ou três alternativos, sob três critérios: bem-estar dos participantes, dispersão do tempo de espera e estabilidade do fundo. A gente não afirma o tamanho do ganho, só a ordenação, e só se ela aguentar a incerteza da calibração.

À parte, um experimento de aprendizado por reforço sobre o ambiente já calibrado testa se agentes que aprendem jogando se comportam diferente do que a teoria clássica de leilão prevê.

## 5. O que já existe

- **Capítulo 1 em rascunho** (contexto, problema, hipóteses, objetivos) e **capítulo 2 completo em rascunho** (mecânica, regras de contemplação, regulação, inadimplência, e a ponte para o modelo formal).
- **Documento de escopo fechado**: tese, pergunta, três hipóteses falseáveis, notação, e uma lista escrita do que o trabalho *não* é (não é estudo jurídico, não propõe redação de norma, não é software para administradora).
- **Bibliografia**: 22 referências verificadas contra fonte primária, com a literatura de ROSCAs (Besley–Coate–Loury, Klonner), identificação em leilões (Athey–Haile, Guerre–Perrigne–Vuong) e RL em mercados (Calvano et al.).
- **Infraestrutura**: repositório versionado; texto em markdown compilando para LaTeX abnTeX2; e um script de auditoria que barra qualquer número no texto sem arquivo de resultado de origem e qualquer citação sem o PDF em disco.

**O que ainda não existe, e eu prefiro falar antes que o senhor pergunte:** dados baixados, código de simulação e resultado. Tudo isso começa agora.

## 6. O maior risco e a saída

O trabalho depende de uma coisa verificável: os dados públicos precisarem ter variação suficiente na fração de contemplações por lance, entre grupos e ao longo do tempo, para identificar os parâmetros. É a primeira coisa que a gente checa, na primeira semana.

Se não tiver, o trabalho não muda de tema. Muda de estimação para **calibração por alvos declarados**: parâmetros fixados pela literatura e pelos agregados, e a hipótese de adequação empírica vira afirmação de consistência. Custa um dia de reescrita e preserva o núcleo, que é a comparação entre desenhos.

## 7. Calendário

*[Datas a fechar entre os três antes da reunião. Proposta abaixo, que troca a entrega de 12/10 por 26/10 — ver nota.]*

| Até | Entrega |
|---|---|
| 04/10 | Painel do Bacen, fatos estilizados, marco de identificação; capítulo 4 (modelo formal) em rascunho |
| 11/10 | Versão ponta a ponta, ainda simples: um mecanismo alternativo, calibração com dois momentos, primeira tabela |
| 18/10 | Demais mecanismos, teste fora da amostra, RL, robustez. **Resultados congelados** |
| 25/10 | Redação dos capítulos restantes, revisão, formatação ABNT |
| 26/10 | Entrega |

## 8. O que eu preciso do senhor

1. **O enquadramento na área convence?** Se não, que ênfase deixaria mais sólido para a banca.
2. **Critérios de avaliação.** Bem-estar, espera e estabilidade do fundo, e como pesar um contra o outro. É a decisão mais consequente do trabalho e a gente quer fechar com o senhor antes de implementar.
3. **Prazo e formato.** A data real de entrega e de defesa na unidade, e o padrão de formatação esperado.
4. **Acompanhamento.** Duas reuniões com material em mãos: uma com o modelo formal e os fatos estilizados, outra com a versão completa.

---

## Perguntas prováveis — respostas curtas

**"Isso não é trabalho de economia?"** O objeto é um mecanismo de alocação e o método é simulação multiagente com estimação computacional; a economia entra como domínio, do mesmo jeito que a biologia entraria num trabalho de estufa. Seção 3 acima.

**"Se não dá para resolver analiticamente, como vocês sabem que a simulação está certa?"** Casos-limite: onde a literatura tem solução fechada (leilão estático, ROSCA com prêmio único), o simulador tem que reproduzir. É condição para seguir, não apêndice.

**"Política paramétrica não é assumir a resposta?"** Ela restringe a forma do comportamento, não a ordenação entre mecanismos. E a validação fora da amostra testa justamente se a forma aguenta. O RL entra como verificação de que agentes sem forma imposta não caem num comportamento completamente diferente.

**"Um mecanismo alternativo seria legal?"** O espaço de desenhos é restrito ao que a Lei 11.795/2008 admite: continua havendo sorteio e lance, e o que muda é como cada canal é parametrizado (por exemplo, sorteio ponderado por tempo de espera, ou regra de preço do lance). Proposta de reforma normativa está fora do escopo. *(A admissibilidade de cada alternativa ainda precisa ser checada contra a Resolução 285.)*

**"Três pessoas, como dividem?"** Por trilha vertical: dados, modelo, calibração e resultados. Cada trilha tem entregável próprio, e as duas interfaces entre elas (formato do painel e assinatura do simulador) são fixadas por escrito na primeira semana.

**"Por que dá para fazer em um mês?"** Porque o escopo já foi cortado para caber: um segmento, um regime, política paramétrica na calibração, RL como experimento único, ~70 páginas. O que não se corta é validação; se atrasar, sai mecanismo alternativo, nunca validação.
