import type {Narration} from './timeline';

/**
 * The narration of the video: narration[slide number][stage index (0 = the first)] = lines. Each line is one speech bubble, typed
 * with its own keystrokes; two lines in one stage are typed one after the other, the second in a new bubble below.
 * Keep it minimal: a line is one short plain sentence (at most 64 characters), a stage has one or two lines, and most stages have none.
 * A question slide gets no answer. Draft text: edit freely, then run `npm run video:audio` and `npm run video`.
 */
export const narration: Narration = {
  2: {0: ['A ring of four triangles.'], 2: ['Merging neighbours lowers Q.']},
  3: {0: ['Now add more triangles.']},
  4: {1: ['One edge seen, 0.8 expected by chance.'], 3: ['From n = 8 on, merging pairs wins.']},
  5: {0: ['The karate club, in four groups.'], 2: ['Louvain returns different splits across runs.']},
  6: {0: ['34 nodes, 78 random edges.']},
  7: {1: ['200 random networks, all above 0.3.'], 3: ["100-node random networks reach the club's Q."]},
  9: {1: ['Found groups put node 5 with the blue nodes.'], 2: ['Every cell is a pair of nodes.']},
  10: {2: ['Check where the two matrices agree.'], 3: ['21 of the 28 pairs agree.']},
  11: {0: ['Thirty nodes, five groups.']},
  12: {0: ['Forty random relabelings.'], 2: ['ARI is 0.49 for the eight nodes.']},
  14: {0: ['Match A with blue, B with orange.'], 1: ['Swap the columns and the count changes.']},
  15: {1: ['Divide by 8: joint probabilities.']},
  16: {0: ['Row sums, then column sums.']},
  17: {0: ['Unrelated splits: joint = marginal times marginal.']},
  18: {2: ['Add the shares: I = 0.549.']},
  19: {1: ['The overlap is the mutual information.'], 2: ['Divide by the average entropy: NMI.']},
  20: {1: ['Every node alone: ARI is 0.']},
  21: {3: ['NMI and ARI prefer different splits.']},
  23: {0: ['Two groups, no edges yet.'], 2: ['Draw from ten tickets: nine say edge.']},
  24: {0: ['Same network, shuffled order.']},
  25: {2: ['Sorted by group, two dense blocks appear.']},
  26: {0: ['Now the two probabilities are swapped.']},
  27: {2: ['At 0.45 everywhere, it is a random network.']},
  28: {0: ['Guess the groups, then score the guess.'], 3: ['The true grouping scores highest.']},
  29: {0: ['A formula for the probability of the network.'], 3: ['Multiply over all pairs: the likelihood.']},
  30: {1: ['Fix c first.'], 3: ['The best p is edges over pairs.']},
  31: {2: ['Now only c is left.']},
  32: {1: ['More groups always fit at least as well.'], 2: ['K = 8 fits perfectly and means nothing.']},
  33: {0: ['A real network: political blogs.'], 1: ['Hubs, not politics, decide the split.']},
  34: {1: ['No hubs in a random network.'], 2: ['The SBM spends a group on the hubs.']},
  35: {1: ['Give every node its own theta.']},
  36: {1: ['Same recipe: fix c first.']},
  37: {1: ['This is m times a mutual information.']},
  38: {1: ['Degree correction recovers the political split.']},
  39: {1: ['The shortest description picks K = 2.']},
  40: {0: ['graph-tool fits this model.']},
  41: {2: ['graph-tool finds a single group.']},
};
