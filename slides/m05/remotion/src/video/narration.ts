import type {Narration} from './timeline';

/**
 * The narration of the video: narration[slide number][stage index (0 = the first)] = lines. Each line is one speech bubble, typed
 * with its own keystrokes; the lines of one stage are typed one after the other, each in a new bubble below the last. Two bubbles
 * are on screen at most.
 *
 * How it is written:
 * - A stage's note starts only after the slide has finished animating, so nothing moves on the slide while a note is being read.
 * - The first line often says what the slide shows (the slide's own words, in the chat, so the eye can stay with the bubble);
 *   the next line adds what the slide does not say: why, how to read it, what to compare.
 * - A line is one short plain sentence (at most 64 characters). No answer on a question slide: it ends with a prompt to think.
 * Draft text: edit freely, then run `npm run video:audio` and `npm run video`.
 */
export const narration: Narration = {
  1: {0: ['Modularity Q gives one score to a grouping.', "Let's see where that score misleads us."]},
  2: {
    0: ['Four triangles, joined by single edges, form a ring.'],
    1: ['Group each triangle on its own: Q = 0.500.', 'Q rewards dense groups with few edges between them.'],
    2: ['Pair the neighbours instead: Q = 0.375.'],
  },
  3: {
    0: ['Now we add triangles, one at a time.'],
    1: ['The same two groupings, now with ten triangles.', 'Take a moment: which one has the higher Q?'],
  },
  4: {
    0: ['Single triangles give Q = 0.650, pairs give 0.675.', 'With ten triangles, pairing the neighbours wins.'],
    1: ['Two neighbouring triangles share one edge.', 'Chance alone would give 0.8 edges between them.'],
    2: ['As n grows, the expected number of edges falls.'],
    3: ['The two triangles did not change; the network grew.', "Q depends on the whole network's size: the resolution limit."],
  },
  5: {
    0: ['Louvain finds four groups in the club, with Q = 0.407.'],
    1: ['Merge one group and move one node: Q = 0.402.'],
    2: ['Louvain was run 400 times with different seeds.', 'It returned 16 different splits, with Q from 0.385 to 0.420.'],
  },
  6: {
    0: ['A network built without any groups: random edges.'],
    1: ['We run Louvain on it anyway.', 'Take a moment: what Q would you expect?'],
  },
  7: {
    0: ['Louvain still finds five groups; its Q is 0.346.'],
    1: ['200 random networks, all above the usual 0.3 threshold.'],
    2: ["The club's Q of 0.420 lies outside this cloud."],
    3: ['With 100 nodes, random networks score as high as the club.', 'A high Q does not prove that groups exist.'],
  },
  8: {0: ['How close are the groups a method found to the groups we know?']},
  9: {
    1: ['A method found groups A and B; node 5 landed in A.'],
    2: ['Each cell of the matrix is one pair of nodes.'],
  },
  10: {
    0: ['Shade a cell when the two nodes share a true group.'],
    2: ['A check: both matrices say together, or both say apart.', 'A cross: one says together, the other says apart.'],
    3: ['21 of the 28 pairs agree: the Rand index is 0.75.'],
  },
  11: {1: ['We shuffle the labels at random.', 'Take a moment: what Rand index would you expect?']},
  12: {
    0: ['Forty shuffles: random labels still score near 0.71.'],
    1: ['Subtract the chance level and rescale: the ARI.'],
    2: ['Back to the eight nodes: the ARI is 0.49.'],
  },
  13: {
    0: ['So far we counted pairs. Why not count single nodes?'],
    1: ['Each node goes to its (true group, found group) cell.'],
  },
  14: {
    0: ['Match A with blue and B with orange: 7 of 8 on the diagonal.'],
    1: ['Swap the columns: the same split, but only 1 of 8.'],
    2: ['With three found groups there is no diagonal at all.'],
    3: ['Names and order are arbitrary, so we need probabilities.'],
  },
  15: {1: ['Divide by 8 nodes: each cell is a joint probability.']},
  16: {
    0: ['Add up each row: the marginal probability of each true group.'],
    1: ['Add up each column for the found groups.'],
  },
  17: {
    0: ['If the splits were unrelated, joint = marginal x marginal.'],
    1: ['Divide the real joint by that product.', 'Above 1: the pair occurs more often than chance.'],
  },
  18: {
    0: ['Each cell contributes joint x log2(ratio).'],
    2: ['The sum is the mutual information: I = 0.549 bits.'],
  },
  19: {
    0: ["Each split is a disc; its area is its own entropy."],
    1: ['Slide them together: the overlap is I = 0.549.'],
    2: ['Divide by the average entropy: NMI = 0.562.'],
    3: ['Identical splits give 1, unrelated splits give 0.'],
  },
  20: {
    1: ['Rand looks fine at 0.57, but the ARI is 0.00.'],
    2: ['For random labels NMI averages 0.215; ARI is about 0.'],
  },
  21: {
    1: ['Four groups: NMI 0.586, ARI 0.450.'],
    2: ['Three groups: NMI 0.568, ARI 0.591.'],
    3: ['NMI prefers four groups; ARI prefers three.'],
    4: ['They agree with each other more than with the real split.'],
  },
  22: {0: ['Now we turn the question around.', 'Instead of finding groups, we generate a network from groups.']},
  23: {
    1: ['Two nodes connect with a probability set by their groups.'],
    2: ['Nodes 1 and 2 are both blue: nine tickets of ten say edge.'],
    3: ['Nodes 1 and 6: one ticket in ten says edge. This draw: no edge.'],
    4: ['We repeat this for every other pair of nodes.'],
  },
  24: {0: ['The same network, with its nodes in a shuffled order.', 'Take a moment: can you see the two groups?']},
  25: {
    1: ['Sort the rows and columns by group.'],
    2: ['Nothing changed but the order. Two dense blocks appear.'],
  },
  26: {0: ['Now swap the table: 0.1 inside groups, 0.9 between.', 'Take a moment: what does the network look like?']},
  27: {
    0: ['With 0.9 inside and 0.1 between: 12 edges, Q = 0.413.'],
    1: ['Turn the dials: now 15 edges, nearly all between groups.'],
    2: ['Both probabilities 0.45: a random network, Q = 0.000.'],
    3: ['One model, three kinds of network.'],
  },
  28: {
    0: ['Now the other way: see the network, guess the groups.'],
    1: ['Score the guess: the log-probability of this network, -17.5.'],
    3: ['The true grouping scores highest: -6.4.'],
  },
  29: {
    0: ['L(c, p) is the probability of the network A given c and p.'],
    1: ['For one pair: an edge has probability p, no edge 1 - p.'],
    2: ['Both cases fit in one expression.'],
    3: ['Multiply over all pairs of nodes: the likelihood.'],
    4: ['Group the pairs by block: m_rs edges among n_rs pairs.'],
    5: ['Take the log: the products become sums.'],
  },
  30: {
    0: ['Find the c and p that make the network most likely.'],
    1: ['First fix c: color the nodes, and count m and n per block.'],
    3: ['The best p_rs is edges over pairs: m_rs / n_rs.'],
  },
  31: {
    0: ['Put p back: only the grouping c is left in the formula.'],
    1: ['For this c, the log-likelihood is -6.44.'],
    2: ['Now maximize over c: the best-scoring grouping wins.'],
  },
  32: {
    0: ['The best log L never decreases as K grows.'],
    1: ['More groups, more parameters, a better fit.'],
    2: ['K = 8 fits perfectly, and the groups mean nothing.'],
  },
  33: {
    0: ['A real network: links between political blogs.', 'Take a moment: what separates the two groups?'],
    1: ['Blue is the high-degree core, yellow is the rest.'],
  },
  34: {
    0: ['The karate club has a few hubs: degrees 17 and 16.'],
    1: ['A random network of the same size has no node above 8.'],
    2: ['In an SBM, all nodes of a group have the same expected degree.', 'To fit the hubs, it puts them in a group of their own.'],
  },
  35: {
    0: ['In the SBM, only the groups decide whether an edge appears.'],
    1: ['The degree-corrected SBM gives each node a number, theta.', 'A large theta means many edges (Karrer and Newman, 2011).'],
  },
  36: {
    0: ['Same recipe: write the log-likelihood, now with three unknowns.'],
    2: ["Each theta is the node's share of its group's total degree."],
  },
  37: {
    0: ['Put them back: a formula in c alone.'],
    1: ['The score is m times a mutual information, as in the NMI.'],
  },
  38: {
    0: ['Back to the blogs. Left: plain SBM. Right: degree-corrected.'],
    1: ['Its split matches the political labels far better.', 'NMI with the known labels: 0.72 against 0.0001.'],
  },
  39: {
    0: ['The Bayesian SBM scores a grouping by description length.'],
    1: ['Eight-node network: the shortest description is at K = 2.'],
  },
  40: {0: ['Tiago Peixoto implemented this in graph-tool, a Python library.']},
  41: {
    1: ["We fit the club with graph-tool's Bayesian SBM."],
    2: ['It returns a single group.', 'The two factions are no stronger than in a random network.'],
  },
};
