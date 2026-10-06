import type {Narration} from './timeline';

/**
 * The narration of the M05MOD video: narration[slide number][stage index (0 = the first)] = lines; each line is one terminal line of the chat (at most 64 characters).
 * The slide's own sentences are typed first, from prose.json; the lines here ADD to them (why, how to read the picture, what to compare).
 * '@mirror' puts the slide's sentences somewhere else in the stage. Rules: slides/NARRATED_VIDEO_GUIDE.md, "Writing the narration".
 * This is a draft by the agent: the lecturer edits it. Numbers: scripts/verify_numbers.py. Nodes are numbered 1 to 34 on the slides (node 5 of the data is node 6 here).
 */
export const narration: Narration = {
  // 0 = the introduction, typed with the title on screen and the narrator in the middle; then the narrator moves up and slide 1 starts
  0: {
    0: [
      'Hello everyone.',
      'This video is about modularity, a score for a grouping of nodes.',
      'In the first half we build the score, step by step.',
      'In the second half we search for a grouping with a high score.',
      'Newman and Girvan proposed the score in 2004.',
      'The search algorithms are Louvain and Leiden.',
      'I will type short notes here while each slide plays.',
      "Let's start with the karate club.",
    ],
  },
  1: {
    0: ['The karate club: a social network studied by Zachary in 1977.', 'Each node is a member. Each edge is a friendship.'],
    1: ['The club split in two after a dispute. Colours show the sides.', '@mirror', 'Take a moment to think about what "strong" should mean.'],
  },
  2: {
    0: ['Edges inside a colour are drawn in that colour.', 'Edges between the two colours are grey.'],
    1: ['We divide the inside count by M, the number of edges.'],
    2: ['@mirror', 'A high fraction means strong groups.'],
  },
  3: {
    0: ['@mirror', 'Think about moving nodes between the two groups.', 'Take a moment to guess.'],
    1: ['Move the orange nodes into the blue group, one by one.', 'The score first drops, then climbs to 1.'],
    2: ['@mirror', 'This score is not useful. We need a fairer comparison.'],
  },
  4: {
    0: ['Call this the inside fraction. M is the number of edges.'],
    1: ['@mirror', 'Then Q is the gap between the two.'],
    2: ['@mirror', 'With everyone in one group, both terms are 1.'],
  },
  5: {
    0: ['A small example: two triangles joined by one edge.', 'Each node has a degree k, its number of edges.'],
    1: ['Cut every edge in the middle.', 'Each edge becomes two half-edges, called stubs.', 'Node 3 has three stubs because its degree is 3.'],
    2: ['Now join the stubs again, two at a time, at random.', '@mirror'],
    3: ['On the left, 6 of 7 edges are inside the groups.', 'After rewiring, only 2 of 7 are inside.', '@mirror', 'The rewired network has no communities by construction.'],
  },
  6: {
    0: ['Now we ask about one pair of nodes, i and j.', 'The 14 stubs are in a row, grouped by node.'],
    1: ['Take one stub of node i.', '@mirror'],
    2: ['k_j of the other stubs belong to node j.', 'So the chance is about k_j over 2M.'],
  },
  7: {
    0: ['@mirror', 'Node i has k_i stubs and node j has k_j stubs.'],
    1: ['@mirror', 'Multiply: k_i k_j pairs, each joined with chance 1 over 2M.'],
    2: ['@mirror', 'Starting from j gives k_j k_i over 2M, the same number.', 'It is one edge seen from both ends, so it counts once.'],
  },
  8: {
    0: ['Try the two biggest hubs of the club.', '@mirror', 'Strictly, it is the expected number of edges between i and j.'],
    1: ['@mirror', 'So for most pairs we may read it as a probability.'],
    2: ['@mirror', 'We use it as it is, for sparse networks.'],
  },
  9: {
    0: ['This matrix has one cell for every pair of nodes.', 'Rows and columns are nodes. The diagonal is a node with itself.'],
    1: ['@mirror', 'This is the adjacency matrix, A.'],
  },
  10: {
    0: ['Next, we write the degree of each node beside it.', 'A second matrix holds k_i times k_j over 2M.'],
    1: ['Row by row. Nodes 3 and 4 give 3 times 3 over 14.'],
    2: ['@mirror', 'It knows the degrees and nothing else.'],
  },
  11: {
    0: ['Place A and E side by side.', 'We subtract E from A, cell by cell.'],
    1: ['The result is the modularity matrix, B.'],
    2: ['Nodes 3 and 4: the edge exists, and chance gave only 0.64.', '@mirror'],
    3: ['@mirror', 'So putting everyone in one group gives a total of 0.'],
  },
  12: {
    0: ['@mirror', 'The two blocks along the diagonal are the two groups.'],
    1: ['Now E: the same shape, with smooth values.'],
    2: ['Edges sit mostly in the diagonal blocks. B is positive there.'],
  },
  13: {
    0: ['Give each node a group label c_i. It is its colour.'],
    1: ['Keep only the cells where i and j are in the same group.', 'The delta is 1 for the same group and 0 otherwise.'],
    2: ['Add up the kept cells of B, then divide by 2M.', '2M is the sum of all the degrees.'],
    3: ['@mirror', 'Newman and Girvan introduced this score in 2004.', 'For the karate club, Q is 0.358.'],
  },
  14: {
    0: ['Now we compare partitions of the club by their Q.', 'Every node alone gives a negative Q.'],
    1: ['Everyone in one group gives exactly 0.'],
    2: ['The two sides of the club give 0.358.'],
    3: ['Four groups give 0.420, higher than the two sides.', 'These four groups come from the algorithm we meet next.'],
    4: ['@mirror', 'Next: how to find the grouping with the highest Q.'],
  },
  15: {
    0: ['@mirror', 'That is the Bell number for 34 nodes.'],
    1: ['@mirror', 'So we start from a guess and improve it with small moves.'],
  },
  16: {
    0: ['@mirror', 'Each label is just the node number. Q is below 0.'],
    1: ['Visit the nodes in a fixed order.', '@mirror', 'The plot shows Q after each move.'],
    2: ['The moves go on, 36 in total.', 'Q rises with every move.'],
    3: ['@mirror', 'We end with 5 groups and Q = 0.399.'],
  },
  17: {
    0: ['We check every node and every neighbouring group.', '@mirror'],
    1: ['Try node 6: it moves from the dark group to the orange group.', 'Q falls from 0.399 to 0.386.'],
    2: ['@mirror', 'The two small groups would make a better group together.', 'A single move breaks a small group apart, so it never sees this.'],
  },
  18: {
    0: ['Louvain treats each group as one node.'],
    1: ['Each group shrinks to one disc.', '@mirror', 'Edges inside a group become a loop, so nothing is lost.'],
    2: ['@mirror', 'Now the groups can move, as one unit each.'],
  },
  19: {
    0: ['@mirror', 'Now we have 5 nodes instead of 34.'],
    1: ['@mirror', 'This is the merge we tried a moment ago.'],
    2: ['Expand the nodes back into the original network.', 'We now have 4 groups, and Q is 0.420.'],
  },
  20: {
    0: ['This is Louvain.', 'Move nodes. Merge groups into nodes. Repeat.', 'Stop when Q no longer rises.'],
    1: ['Q was -0.050 at the start.', '0.399 after the first level, and 0.420 after the second.', 'A third level changes nothing, so we stop.'],
    2: ['Louvain is by Blondel and colleagues, from 2008.', 'It is fast and works on large networks.'],
  },
  21: {
    0: ['Louvain has a weak point: a group can fall apart.', 'This small network is built to show the problem.'],
    1: ['The bridge node has more edges to the orange group.', 'Moving it to orange raises Q from 0.222 to 0.357.'],
    2: ['@mirror', 'Putting the two blue triangles in one group lowers Q.'],
    3: ['@mirror', 'Traag, Waltman and van Eck reported this in 2019.'],
  },
  22: {
    0: ['Leiden was made to fix exactly this.'],
    1: ['@mirror', 'Splitting the blue group raises Q to 0.482.'],
    2: ['The loop gets one more step: a split before the merge.'],
    3: ['Leiden guarantees that every group is connected.', 'The authors also report that it runs faster than Louvain.'],
  },
  23: {
    0: ['@mirror', 'This is the score we built.'],
    1: ['Louvain climbs in two kinds of steps: nodes, then groups.', '@mirror'],
    2: ['@mirror', 'Leiden adds a split step.'],
    3: ['@mirror', 'Merging too much comes from Q itself. Leiden does not fix it.'],
  },
};
