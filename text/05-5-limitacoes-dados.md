---
secao: 5.5
titulo: Limitações dos dados
status: rascunho
responsavel:
insumos:
  - nenhum
  - ESTADO.md §5 itens 7, 12, 15, 16, 17 e 26
fontes:
  - results/qualidade_dados.csv
excecoes:
  - 285
paginas_alvo: 2
---

# Limitações dos dados

Os dados do Bacen são abundantes no que diz respeito a contagens e escassos no que diz respeito a decisões. Esta seção lista o que não é observável e, para cada lacuna, o que ela impede o trabalho de afirmar.

**O lance individual não é observado.** Nenhum arquivo traz o percentual ofertado, quem ofertou, quantos ofertaram ou qual foi o lance vencedor. O que se observa é quantas cotas foram contempladas por lance em cada administradora e trimestre. A política de lance $\pi_\phi$ é, por isso, identificada apenas pelos seus efeitos agregados. O trabalho não pode afirmar nada sobre a distribuição dos lances ofertados, nem sobre o lance médio vencedor, além do que o modelo implica; qualquer número sobre lances nos capítulos seguintes é resultado do modelo calibrado, e não medição. Essa é a restrição que dá origem à afirmação metodológica da tese: se a dominância de um desenho pode ser estabelecida assim, ela o é a partir de observação agregada.

**O canal da contemplação só existe no grão de administradora e trimestre.** O arquivo por grupo não separa sorteio de lance. Não é possível, portanto, medir a fração de lance de um grupo, nem relacioná-la diretamente à idade, ao prazo ou ao saldo do grupo. A relação entre tamanho e fração de lance usada no teste de H2 é uma relação entre administradoras, com o tamanho medido pela mediana dos grupos de cada uma.

**As duas fontes de fluxo não batem.** A soma trimestral de contemplações no arquivo por UF difere da soma de três meses nos grupos, com razão agregada de 1,095 e divergências grandes em algumas administradoras (`results/qualidade_dados.csv`; seção 5.2). A causa não foi identificada. Por isso nenhum momento combina fluxos das duas fontes, e a calibração não pode usar, por exemplo, a razão entre contemplações por lance e cotas ativas, que exigiria as duas.

**O excluído contemplado aparece sem canal e sem valor.** O arquivo por UF conta os excluídos contemplados no trimestre, mas não informa quanto foi restituído. O teto de restituição $\bar r$ é identificado pelo número de restituições, e não pelo valor, e seu valor calibrado depende da hipótese de que cada restituição devolve exatamente o que a cota pagou até a exclusão, sem multa nem dedução.

**As cláusulas dos contratos não são publicadas pelo Bacen.** O destino da sobra, o teto do lance embutido e a forma do sorteio de excluídas vêm da leitura de regulamentos de quatro administradoras, todos posteriores à Resolução BCB n. 285/2023. Essas administradoras estão entre as maiores do segmento, mas não são uma amostra da população, e não se sabe qual cláusula as demais adotam. Por isso, o destino da sobra é fixado pelo regulamento nas administradoras cujo contrato foi lido e, nas demais, sorteado com a probabilidade $\eta_0$ observada entre os regulamentos (seção 4.2). O que se perde é a garantia de que as administradoras não lidas sigam a mesma proporção.

**Taxa de administração, fundo de reserva e valor dos bens ficam de fora.** O valor médio do bem é observado por grupo, mas o modelo normaliza o crédito a 1 e não o usa. A taxa de administração e o fundo de reserva não são observados de forma utilizável por grupo e, de todo modo, estão fora do escopo (seção 4.5). O trabalho não pode, por isso, dizer nada sobre a receita da administradora sob os diferentes desenhos.

**O período é curto.** O regime posterior à Resolução tem 23 meses no painel por grupo e sete trimestres no painel por administradora. Mudanças lentas, como o envelhecimento das carteiras ou a resposta das administradoras à nova norma, não podem ser separadas do ruído. Os momentos tratam o período como um único regime estacionário.

**O participante não é observado.** Nada nos dados informa urgência, liquidez, renda ou motivo de adesão. As distribuições $F_\theta$ e $F_\lambda$ são hipóteses, fixadas e não estimadas (seção 4.2). Os resultados sobre bem-estar dependem delas, e o trabalho não pode afirmar que os ganhos ou perdas de um desenho valem para uma população de participantes com outras características.
