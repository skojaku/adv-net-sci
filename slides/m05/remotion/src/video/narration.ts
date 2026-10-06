import type {Narration} from './timeline';

/**
 * The narration of the video: narration[slide number][stage index (0 = the first)] = lines. Each line is one speech bubble, typed with its
 * own keystrokes; the lines of one stage are typed one after the other, each in a new bubble below the last. Two bubbles are on screen at most.
 *
 * How it works:
 * - The video leaves the slides' own sentences off the slides (src/components/Text.tsx) and types them here in the chat instead, so nothing
 *   on a slide competes with the bubble. Those sentences are collected from the slides (`npm run video:prose` writes src/video/prose.json) and are
 *   typed first in their stage; write '@mirror' in a stage's lines to put them somewhere else. The lines below only ADD to them: why, how to
 *   read the picture, what to compare. Labels, numbers, figures and formulas stay on the slide.
 * - A stage's notes start only after the slide has finished animating (the slide is still while a note types).
 * - One continuous talk: the three section dividers (S1, S8, S22) are not in the video, and the chat is never cleared: the bridge from one
 *   part to the next is the first lines of the next slide (S9, S23).
 * - A line is one short plain sentence (at most 64 characters). No answer on a question slide: it ends with a prompt to think.
 * Draft text: edit freely, then run `npm run video:audio` and `npm run video`.
 */
export const narration: Narration = {
  2: {
    0: ['Modularity Q gives one score to a grouping.', "Let's see where that score misleads us."],
    1: ['Q rewards dense groups with few edges between them.'],
    2: ['Pair the neighbours instead: Q = 0.375.', '@mirror'],
  },
  3: {
    0: ['Now we add triangles, one at a time.'],
    1: ['@mirror', 'Take a moment to guess.'],
  },
  4: {
    0: ['With ten triangles, pairing the neighbours wins.'],
    1: ['Chance alone would give 0.8 edges between them.', 'One edge beats 0.8, so merging raises Q.'],
    2: ['As n grows, the expected number of edges falls.'],
    3: ['@mirror', 'Q compares each group with chance over the whole network.'],
  },
  5: {
    0: ['Louvain finds four groups, with Q = 0.407.'],
    1: ['Merge one group and move one node: Q = 0.402.'],
    2: ['Louvain was run 400 times with different seeds.', '@mirror'],
  },
  6: {
    0: ['Here is a network built without any groups.', '@mirror'],
    1: ['@mirror', 'Take a moment to guess.'],
  },
  7: {
    0: ['Louvain still finds five groups; its Q is 0.346.'],
    1: ['Every one of 200 random networks scores above 0.3.'],
    2: ["The karate club's Q of 0.420 lies outside this cloud.", '@mirror'],
    3: ['@mirror', 'A high Q does not prove that groups exist.'],
  },
  9: {
    0: ['So far we scored one grouping with Q.', 'Now: how close is a found grouping to a known one?'],
    1: ['Node 5 landed in A, with the blue nodes.'],
    2: ['Turn the found row on its side to get a matrix of pairs.', '@mirror'],
  },
  10: {
    0: ['@mirror', 'A shaded cell means this pair is together.'],
    2: ['A check: both say together, or both say apart.', 'A cross: one says together, the other says apart.'],
    3: ['The Rand index is the share of pairs that agree.'],
  },
  11: {1: ['Now we shuffle the labels at random.', '@mirror', 'Take a moment to guess.']},
  12: {
    0: ['Shuffle forty times: the Rand index lands near 0.71.'],
    1: ['Subtract the chance level and rescale: the ARI.'],
    2: ['Back to the eight nodes: the ARI is 0.49.'],
  },
  13: {
    0: ['So far we counted pairs of nodes.', '@mirror'],
    1: ['Each node goes to its cell: (true group, found group).', '@mirror'],
  },
  14: {
    0: ['@mirror', 'Then 4 + 3 = 7 of the 8 nodes sit on the diagonal.'],
    1: ['@mirror', 'Now only 0 + 1 = 1 node sits on the diagonal.'],
    2: ['With three found groups there is no diagonal at all.'],
    3: ['@mirror', 'We will build such a score from probabilities.'],
  },
  15: {
    0: ['True groups are the rows, found groups the columns.'],
    1: ['Divide by 8 nodes: each cell is a joint probability.', '@mirror'],
  },
  16: {0: ['@mirror', 'A marginal ignores the other split.'], 1: ['@mirror']},
  17: {
    0: ['If the splits were unrelated, what would a cell hold?', '@mirror'],
    1: ['Divide the real joint probability by that product.', '@mirror'],
  },
  18: {
    0: ['Each cell adds joint probability x log of its ratio.'],
    1: ['@mirror', 'Cells above 1 add; cells below 1 subtract.'],
    2: ['The sum is the mutual information: I = 0.549 bits.', '@mirror'],
  },
  19: {
    0: ['Each split becomes a disc whose area is its entropy.'],
    1: ['Slide them together: the overlap is I = 0.549.'],
    2: ['Divide by the average entropy: NMI = 0.562.'],
    3: ['Identical splits give NMI = 1, unrelated splits give 0.'],
  },
  20: {
    0: ['Now a split that puts every node alone.'],
    1: ['Rand looks fine at 0.57, but the ARI is 0.00.', '@mirror'],
    2: ['For random labels on 30 nodes, NMI averages 0.215.', '@mirror'],
  },
  21: {
    0: ["The karate club's real split: 17 and 17."],
    1: ['Four groups: NMI 0.586, ARI 0.450.'],
    2: ['Three groups: NMI 0.568, ARI 0.591.'],
    3: ['NMI prefers four groups; ARI prefers three.', '@mirror'],
    4: ['@mirror', 'They agree with each other more than with the real split.'],
  },
  23: {
    0: ['Now we turn the question around.', 'Instead of finding groups, we generate a network from groups.'],
    1: ['Two nodes connect with a probability set by their groups.'],
    2: ['Nodes 1 and 2 are both blue: probability 0.9.'],
    3: ['Nodes 1 and 6 are in different groups: probability 0.1.', '@mirror'],
    4: ['We repeat this for every other pair of nodes.', 'The result is a network with 12 edges.'],
  },
  24: {0: ['The same network, with its nodes in a shuffled order.', '@mirror', 'Take a moment to look.']},
  25: {
    1: ['Sort the rows and columns by group.'],
    2: ['@mirror', 'Edges are dense inside groups and sparse between them.'],
  },
  26: {0: ['Now swap the table: 0.1 inside groups, 0.9 between.', '@mirror', 'Take a moment to guess.']},
  27: {
    0: ['With 0.9 inside and 0.1 between we get 12 edges.'],
    1: ['Turn the dials: now 15 edges, nearly all between groups.'],
    2: ['Set both probabilities to 0.45.', '@mirror'],
    3: ['@mirror', 'The table of probabilities is the whole difference.'],
  },
  28: {
    0: ['Now the other way: we see the network and guess the groups.', '@mirror', 'A first guess: odd nodes against even nodes.'],
    1: ['@mirror', 'Under this guess the score is -17.5.'],
    2: ['Moving one node gives -15.5; one big group gives -19.1.'],
    3: ['The true grouping scores highest: -6.4.', '@mirror'],
  },
  29: {
    0: ['L(c, p) is the probability of A given c and p.'],
    1: ['An edge has probability p; no edge has 1 - p.'],
    2: ['The exponent A_ij switches between p and 1 - p.'],
    3: ['Multiply over all pairs of nodes: the likelihood.'],
    4: ['Each block has m_rs edges among n_rs pairs of nodes.'],
    5: ['Take the log: the products become sums.'],
  },
  30: {
    0: ['Find the c and p that make the network most likely.'],
    1: ['First fix c: color the nodes by the grouping.'],
    2: ['Set the derivative with respect to p_rs to zero.'],
    3: ['The best p_rs is edges over pairs: m_rs / n_rs.'],
  },
  31: {
    0: ['Put that p back: only the grouping c is left.'],
    1: ['For this c, the log-likelihood is -6.44.'],
    2: ['@mirror', 'The grouping with the highest score is our answer.'],
  },
  32: {
    0: ['The best log L never decreases as K grows.'],
    1: ['@mirror', 'From K = 5 on the fit is perfect: log L = 0.'],
    2: ['K = 8 fits perfectly, and the groups mean nothing.'],
  },
  33: {
    0: ['A real network: links between political blogs.', '@mirror', 'Take a moment to think.'],
    1: ['Blue is the high-degree core, yellow is the rest.', '@mirror'],
  },
  34: {
    0: ['The karate club has a few hubs: degrees 17 and 16.'],
    1: ['@mirror', 'No node has more than 8 edges.'],
    2: ['@mirror', 'Hubs link up more often simply because they have more edges.'],
  },
  35: {
    0: ['In the SBM, only the groups decide whether an edge appears.'],
    1: ['Karrer and Newman (2011) give each node a number, theta.', 'A large theta means the node tends to have many edges.'],
  },
  36: {
    0: ['Same recipe: write the log-likelihood, now with three unknowns.'],
    1: ['Fix c first, then find the best theta and omega.'],
    2: ['@mirror', 'Each omega is the number of edges between the groups.'],
  },
  37: {
    0: ['Put them back: a formula in c alone.'],
    1: ['@mirror', 'The score is m times a mutual information.'],
    2: ['It has the same shape as before: joint over marginals.'],
    3: ['All that is left is to maximize over c.'],
  },
  38: {
    0: ['Back to the political blogs: plain SBM left, corrected right.'],
    1: ['@mirror'],
  },
  39: {
    0: ['The Bayesian SBM scores a grouping by its description length.', '@mirror'],
    1: ['Eight-node network: the shortest description is at K = 2.', '@mirror'],
    2: ['The full model infers K, nests groups, and corrects degrees.', '@mirror'],
  },
  40: {
    0: ['Tiago Peixoto implemented this model.', '@mirror'],
    1: ['One function call fits the model.'],
  },
  41: {
    0: ['Back to the karate club, with its two known factions.'],
    1: ["We fit the club with graph-tool's Bayesian SBM."],
    2: ['It returns a single group.', '@mirror'],
  },
};
