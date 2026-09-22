# Bibliografia verificada — TCC Consórcios

Todas as referências do Bloco A foram conferidas em busca nesta sessão contra fonte
primária ou lista de referências de artigo publicado. Estão em `refs/refs.bib`.
As do Bloco B são candidatas que **não** verifiquei — não entraram no `.bib` e não
devem ser citadas até você confirmar.

Fluxo: baixar o PDF → `refs/pdfs/<chave>.pdf` → rodar o prompt P3 → fichamento em
`refs/fichamentos/`. A auditoria acusa toda citação sem PDF, então o `.bib` só fica
limpo quando os arquivos estiverem em disco.

---

## Controle de status

Ciclo: `candidata` → `verificada` → `pdf baixado` → `fichada` → `citada`.
Só entra em `refs/refs.bib` a partir de `verificada`. Atualize esta tabela ao mudar de estado.

| Chave | Status | Próxima ação |
|---|---|---|
| brasil2008lei11795 | verificada | baixar PDF (texto consolidado, Planalto) |
| bcb2009circ3432 | verificada | baixar PDF (normativos.bcb.gov.br) |
| bcb2023res285 | verificada | baixar PDF |
| bcb2026consorcios | verificada | salvar página/CSV de referência |
| abac2026anuario | verificada | baixar anuário |
| besley1993economics | verificada | baixar PDF |
| kovsted1999rotating | verificada | baixar PDF |
| handa1999economics | verificada | baixar PDF |
| vandenbrink1997microeconomics | verificada | baixar PDF |
| klonner2003rotating | verificada | baixar PDF |
| klonner2008private | verificada | baixar PDF — **ler primeiro** |
| kuo1993loans | verificada | localizar (periódico taiwanês; não bloqueante) |
| guerre2000optimal | verificada | baixar PDF |
| athey2002identification | verificada | baixar PDF — **ler primeiro** |
| athey2007nonparametric | verificada | baixar PDF — **ler primeiro** |
| campo2011semiparametric | verificada | baixar PDF |
| aradillas2013identification | verificada | baixar PDF |
| calvano2020artificial | verificada | baixar PDF |
| calvano2021imperfect | verificada | baixar PDF |
| banchio2022artificial | verificada | baixar PDF (arXiv:2202.05947) — **ler primeiro** |
| khezr2025use | verificada | baixar PDF |
| canese2021multiagent | verificada | baixar PDF |
| Besley-Coate-Loury *allocative performance* | candidata | confirmar versão publicada |
| Calomiris e Rajaraman (1998) | candidata | confirmar periódico e páginas |
| Anderson e Baland (2002) | candidata | confirmar |
| Gouriéroux, Monfort e Renault (1993) | candidata | **confirmar — sustenta o cap. 6.3** |
| McFadden (1989) | candidata | **confirmar — sustenta o cap. 6.3** |
| Duffie e Singleton (1993) | candidata | **confirmar — sustenta o cap. 6.3** |
| Klonner e Rai | candidata | confirmar |
| Guerre, Perrigne e Vuong (2009) | candidata | confirmar |
| *Literatura brasileira* | **vazio** | esgotar BDTD, Teses USP, CAPES, SciELO, SPELL, WPs do BCB |

---

## Antes das referências: dois achados institucionais que mudam o Capítulo 4

Apareceram na busca e são mais importantes que qualquer artigo desta lista, porque
afetam a formalização do modelo. Ambos precisam ser confirmados no normativo do
Bacen antes de virar hipótese de modelagem.

**1. O número de contemplações por lance é endógeno ao saldo do fundo comum.** A
administradora verifica o caixa do grupo, deduz os créditos dos contemplados por
sorteio, e só então define quantas contemplações por lance cabem naquela assembleia.
Se não há recurso, não há contemplação — mesmo com lance vencedor, e o valor ofertado
é devolvido.

Isso não é detalhe. Significa que o número de vencedores por rodada é uma variável de
estado, não um parâmetro; que existe um acoplamento direto entre inadimplência e
probabilidade de contemplação; e que o "leilão" do consórcio é de múltiplas unidades
com oferta estocástica. Nenhum dos modelos de ROSCA da literatura tem essa
característica — eles assumem um pote por período. **É possivelmente a sua principal
fonte de originalidade em relação a Klonner e a Besley-Coate-Loury.**

**2. O critério de desempate é percentual, não absoluto.** Quando dois consorciados do
mesmo grupo têm créditos de valores diferentes e ofertam lances iguais em valor,
vence quem ofertou o maior percentual do próprio crédito contratado. E o critério pode
variar por contrato.

Consequência para o modelo: a ação do agente é naturalmente o percentual do crédito,
não o valor em reais. Isso muda o espaço de ações e normaliza a heterogeneidade de
ticket entre participantes do mesmo grupo.

---

## Bloco A — Verificadas

### A.1 ROSCAs (Capítulo 3.2)

**Besley, Coate e Loury (1993).** *The Economics of Rotating Savings and Credit
Associations.* American Economic Review, 83(4), 792–810.
O artigo fundador. Compara alocação aleatória e por lance num modelo de poupança para
bem durável indivisível. O resultado central é o que você precisa: sob hipótese
razoável de preferências, a alocação aleatória é preferível **quando os indivíduos têm
gostos idênticos** — e essa conclusão não se sustenta quando há heterogeneidade.
É a formulação teórica exata da sua H3, e a heterogeneidade é justamente o que seu
modelo introduz. Comece a revisão por este.

**Kovsted e Lyk-Jensen (1999).** *Rotating Savings and Credit Associations: The Choice
between Random and Bidding Allocation of Funds.* Journal of Development Economics,
60(1), 143–172.
Trata diretamente da escolha entre os dois mecanismos — o mesmo par que a regulação
brasileira fixou. Precedente direto da pergunta de pesquisa.

**Klonner (2003).** *Rotating Savings and Credit Associations When Participants Are
Risk Averse.* International Economic Review, 44(3), 979–1005.
Modela a ROSCA como sequência de leilões ascendentes com participantes avessos a risco
e renda estocástica. É a ponte formal entre ROSCA e teoria de leilões, e a aversão a
risco é hipótese plausível para o consorciado brasileiro.

**Klonner (2008).** *Private Information and Altruism in Bidding Roscas.* The Economic
Journal, 118(528), 775–800.
**O precedente metodológico mais próximo do seu trabalho.** Apresenta técnica de
estimação estrutural semiparamétrica para leilões de ROSCA e identifica interações
entre características do grupo e comportamento dos participantes. Leia antes de
escrever o Capítulo 6 — ele já resolveu parte do problema de identificação que você
vai enfrentar, em contexto vizinho.

**Handa e Kirton (1999).** *The Economics of Rotating Savings and Credit Associations:
Evidence from the Jamaican 'Partner'.* Journal of Development Economics, 60(1), 173–194.
Evidência empírica em ROSCA de país em desenvolvimento. Útil como comparação de
magnitude, não como método.

**van den Brink e Chavas (1997).** *The Microeconomics of an Indigenous African
Institution: The Rotating Savings and Credit Association.* Economic Development and
Cultural Change, 45(4), 745–772.
Microfundamentação institucional. Secundário.

**Kuo (1993).** *Loans, Bidding Strategies and Equilibrium in the Discount Bid Rotating
Credit Association.* Academia Economic Papers, 21, 261–303.
Equilíbrio de estratégias de lance em ROSCA de lance com desconto. Difícil de obter —
periódico taiwanês. Se não achar, não é bloqueante.

### A.2 Econometria estrutural de leilões (Capítulo 3.4 e 6.3)

**Athey e Haile (2002).** *Identification of Standard Auction Models.* Econometrica,
70(6), 2107–2140.
**A referência que sustenta a viabilidade metodológica do seu TCC.** O resultado que
importa: o modelo mais simples — valores privados independentes e simétricos — é
identificado não-parametricamente **mesmo quando se observa apenas o preço de
transação de cada leilão**. Para modelos mais ricos, a identificação depende de
informação adicional: identidade do vencedor, algum lance além do preço, variação
exógena no número de participantes, ou covariáveis dos participantes. Você tem
variação no tamanho do grupo e covariáveis de grupo — ou seja, está dentro das
condições que o artigo mapeia. Esta é a citação que responde à pergunta "como você
pode estimar isso sem observar os lances".

**Athey e Haile (2007).** *Nonparametric Approaches to Auctions.* Handbook of
Econometrics, 6A, cap. 60, 3847–3965.
Capítulo de handbook. É o que você lê primeiro para se orientar no campo, antes do
artigo de 2002.

**Guerre, Perrigne e Vuong (2000).** *Optimal Nonparametric Estimation of First-Price
Auctions.* Econometrica, 68(3), 525–574.
O método de referência quando se observam todos os lances. Você cita como o que
**não** dá para fazer no seu caso, e é assim que se justifica o SMM.

**Campo, Guerre, Perrigne e Vuong (2011).** *Semiparametric Estimation of First-Price
Auctions with Risk-Averse Bidders.* The Review of Economic Studies, 78(1), 112–147.
Aversão a risco na estimação estrutural. Complementa Klonner (2003).

**Aradillas-López, Gandhi e Quint (2013).** *Identification and Inference in Ascending
Auctions with Correlated Private Values.* Econometrica, 81(2), 489–534.
Valores correlacionados em leilão ascendente. Relevante se você admitir que os
consorciados de um grupo têm valorações correlacionadas — o que é plausível, dado que
compartilham segmento de bem e, com frequência, região.

### A.3 Aprendizado por reforço em mercados (Capítulo 3.5)

**Banchio e Skrzypacz (2022).** *Artificial Intelligence and Auction Design.*
Proceedings of the 23rd ACM Conference on Economics and Computation (EC '22).
arXiv:2202.05947.
**A referência central da sua H1.** Estuda leilões repetidos jogados por agentes de
Q-learning e encontra que leilões de primeiro preço sem feedback adicional convergem
para resultados tacitamente colusivos — lances abaixo das valorações — enquanto os de
segundo preço convergem para o equilíbrio de Nash estático. Ou seja: **agentes que
aprendem divergem da previsão de equilíbrio estático, e a divergência depende do
formato do leilão.** É exatamente a estrutura da sua H1, num contexto vizinho, com
metodologia publicada. Se existe um artigo para ancorar seu trabalho, é este.

**Calvano, Calzolari, Denicolò e Pastorello (2020).** *Artificial Intelligence,
Algorithmic Pricing, and Collusion.* American Economic Review, 110(10), 3267–3297.
O trabalho que legitimou a agenda de agentes de Q-learning em modelos econômicos
canônicos, publicado no periódico mais exigente da área. Mostra que os algoritmos
aprendem consistentemente a cobrar preços supracompetitivos sem comunicação entre si,
e que o resultado é robusto a assimetrias de custo e demanda, ao número de jogadores e
a formas de incerteza. Cite-o para justificar a escolha metodológica: agentes simples
que aprendem produzem resultados economicamente interpretáveis e replicáveis.
Código e dados estão públicos no openICPSR.

**Calvano et al. (2021).** *Algorithmic Collusion with Imperfect Monitoring.*
International Journal of Industrial Organization, 79, 102712.
Extensão para monitoramento imperfeito — situação do consorciado, que não observa os
lances dos demais. Diretamente aplicável.

**Khezr e Taylor (2025).** *The Use of Artificial Intelligence for Auction Design.*
Journal of Economic Surveys.
Survey recente do campo. Serve para o posicionamento do 3.6 e para garantir que você
não perdeu trabalho relevante.

**Canese et al. (2021).** *Multi-Agent Reinforcement Learning: A Review of Challenges
and Applications.* Applied Sciences, 11(11), 4948.
Revisão técnica de MARL. Referência de método para o 6.2.

---

## Bloco B — Candidatas não verificadas

Apareceram como citações em listas de referência de terceiros ou vieram do meu
conhecimento prévio, e **não** confirmei contra fonte primária. Confirme antes de
usar. Não estão no `refs.bib`.

| Candidata | O que seria | Por que importa |
|---|---|---|
| Besley, Coate e Loury — *On the Allocative Performance of ROSCAs* | Existe como working paper (Princeton 163; BU IED 26, 1992). A versão publicada e seus dados bibliográficos precisam ser confirmados | Complemento direto do artigo de 1993 |
| Calomiris e Rajaraman (1998) | Sobre o papel das ROSCAs: bens duráveis indivisíveis vs. seguro contra eventos | Citado por Klonner; fundamenta a interpretação de urgência |
| Anderson e Baland (2002), QJE | ROSCAs e alocação intradomiciliar | Motivação alternativa para participação |
| Gouriéroux, Monfort e Renault (1993) | Inferência indireta | Base metodológica do seu SMM |
| McFadden (1989), Econometrica | Método de momentos simulados | Idem |
| Duffie e Singleton (1993), Econometrica | Estimação por momentos simulados para séries temporais | Idem |
| Klonner e Rai | Racionamento de crédito e inadimplência em ROSCAs sul-indianas | Ponte com o seu critério de estabilidade do fundo |
| Guerre, Perrigne e Vuong (2009) | Aversão a risco e identificação | Complemento de Campo et al. (2011) |

As três de SMM são as mais urgentes de confirmar, porque sustentam o Capítulo 6.3
inteiro. São referências canônicas e certamente existem — mas eu não as verifiquei
nesta sessão, e a regra do projeto é que isso significa que elas não entram.

---

## Sobre a literatura brasileira: um resultado negativo relevante

Busquei literatura acadêmica brasileira sobre o mecanismo de contemplação — desenho,
comportamento de lance, eficiência alocativa — e **não localizei nada**. O que aparece
é material institucional da ABAC, conteúdo comercial de administradoras, e literatura
jurídica sobre consórcios públicos, que é outro objeto inteiramente.

Isso é bom sinal para a originalidade e ruim para o rigor: ausência de resultado em
busca aberta não é prova de ausência de literatura. Antes de afirmar ineditismo no
Capítulo 3.6 — e a banca vai cobrar essa afirmação —, esgote as bases próprias:

- **BDTD** (Biblioteca Digital Brasileira de Teses e Dissertações)
- **Biblioteca Digital de Teses e Dissertações da USP**
- **Catálogo de Teses e Dissertações da CAPES**
- **SciELO** e **SPELL** (periódicos de administração e economia)
- **Working papers do próprio Banco Central** — o regulador publica série de trabalhos
  técnicos e é o candidato mais provável a ter estudado o próprio setor

Strings sugeridas, em português e inglês: *consórcio contemplação lance eficiência*;
*consórcio mecanismo alocação*; *consórcio reserva técnica atuarial*; *Brazilian
consortium ROSCA*; *consorcio bidding allocation Brazil*.

Registre a busca — bases, strings, datas, resultados — enquanto executa. A seção 3.1
exige isso, e reconstruir depois é retrabalho.

---

## Ordem de leitura sugerida

1. Athey e Haile (2007) — orientação no campo
2. Besley, Coate e Loury (1993) — a pergunta teórica
3. Klonner (2008) — o precedente metodológico mais próximo
4. Banchio e Skrzypacz (2022) — a âncora da H1
5. Athey e Haile (2002) — a justificativa de identificação
6. Calvano et al. (2020) — a legitimação metodológica
7. O restante, conforme os capítulos exigirem

Os quatro primeiros bastam para você escrever o Capítulo 3.6 em rascunho e defender a
tese numa conversa com o Cugnasca.
