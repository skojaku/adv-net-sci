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
    0: ['M is the number of edges.'],
    1: [],
    2: [],
  },
  5: {
    0: ['A star joined to a triangle. Each node has a degree k.'],
    1: ['Cut every edge in the middle. Each half-edge is a stub.'],
    2: ['Join the stubs again at random.', '@mirror'],
    3: ['Before: 5 of 6 edges inside. After: 3 of 6.', '@mirror'],
  },
  6: {
    0: ['Node i is the hub, in blue. Node j is in orange.'],
    1: ['k_i and k_j are their numbers of stubs.'],
  },
  7: {
    0: [],
    1: ['This is the expected number of edges between i and j.', 'From j it is k_j k_i over 2M: the same number.'],
  },
  8: {
    0: ['One cell for every pair of nodes, diagonal included.'],
    1: ['@mirror', 'This is the adjacency matrix, A.'],
  },
  9: {
    0: ['Write each degree beside its node.', 'The second matrix holds k_i times k_j over 2M.'],
    1: ['Nodes 1 and 5: 3 times 2 over 12 is 0.50.'],
    2: [],
  },
  10: {
    0: ['Subtract E from A, cell by cell.'],
    1: ['The result is the modularity matrix, Q_ij.'],
    2: ['Nodes 1 and 2 share an edge. A random network expects 0.25.', '@mirror'],
    3: ['@mirror', 'So one group for everyone gives Q = 0.'],
  },
  11: {
    0: [],
    1: ['Now E: the same shape.'],
    2: ['Q_ij is positive where the edges sit, in the diagonal blocks.'],
  },
  12: {
    0: ['Each node has a group label c_i, its colour.'],
    1: ['Keep the cells where i and j share a group: delta = 1.'],
    2: ['Add up the kept cells of Q_ij, then divide by 2M.'],
    3: ['@mirror', 'Newman and Girvan introduced this score in 2004.', 'For the karate club, Q is 0.358.'],
  },
  13: {
    0: ['Compare partitions of the club by Q.', 'Every node alone: Q is negative.'],
    1: ['Everyone in one group: exactly 0.'],
    2: ['The two sides of the club: 0.358.'],
    3: ['Four groups: 0.420, higher than the two sides.', 'They come from the algorithm we meet next.'],
    4: ['@mirror', 'Next: how to find the grouping with the highest Q.'],
  },
  14: {
    0: ['@mirror', 'That is the Bell number for 34 nodes.'],
    1: ['@mirror', 'So we start from a guess and improve it with small moves.'],
  },
  15: {
    0: ['@mirror', 'Each label is just the node number. Q is below 0.'],
    1: ['Visit the nodes in a fixed order.', '@mirror', 'The plot shows Q after each move.'],
    2: ['The moves go on, 36 in total.', 'Q rises with every move.'],
    3: ['@mirror', 'We end with 5 groups and Q = 0.399.'],
  },
  16: {
    0: ['We check every node and every neighbouring group.', '@mirror'],
    1: ['Try node 6: it moves from the dark group to the orange group.', 'Q falls from 0.399 to 0.386.'],
    2: ['@mirror', 'The two small groups would make a better group together.', 'A single move breaks a small group apart, so it never sees this.'],
  },
  17: {
    0: ['Louvain treats each group as one node.'],
    1: ['Each group shrinks to one disc.', '@mirror', 'Edges inside a group become a loop, so nothing is lost.'],
    2: ['@mirror', 'Now the groups can move, as one unit each.'],
  },
  18: {
    0: ['@mirror', 'Now we have 5 nodes instead of 34.'],
    1: ['@mirror', 'This is the merge we tried a moment ago.'],
    2: ['Expand the nodes back into the original network.', 'We now have 4 groups, and Q is 0.420.'],
  },
  19: {
    0: ['This is Louvain.', 'Move nodes. Merge groups into nodes. Repeat.', 'Stop when Q no longer rises.'],
    1: ['Q was -0.050 at the start.', '0.399 after the first level, and 0.420 after the second.', 'A third level changes nothing, so we stop.'],
    2: ['Louvain is by Blondel and colleagues, from 2008.', 'It is fast and works on large networks.'],
  },
  20: {
    0: ['Louvain has a weak point: a group can fall apart.', 'This small network is built to show the problem.'],
    1: ['The bridge node has more edges to the orange group.', 'Moving it to orange raises Q from 0.222 to 0.357.'],
    2: ['@mirror', 'Putting the two blue triangles in one group lowers Q.'],
    3: ['@mirror', 'Traag, Waltman and van Eck reported this in 2019.'],
  },
  21: {
    0: ['Leiden was made to fix exactly this.'],
    1: ['@mirror', 'Splitting the blue group raises Q to 0.482.'],
    2: ['The loop gets one more step: a split before the merge.'],
    3: ['Leiden guarantees that every group is connected.', 'The authors also report that it runs faster than Louvain.', 'Merging too much comes from Q itself. Leiden does not fix it.', 'That limit of Q is next.'],
  },
};
