
# Excellent LLM Quiz Questions

## Amahury 🎉

**Q**: True or False (justify briefly): Adding any number of isolated nodes (degree 0) to an undirected, unweighted graph can change which partition maximizes standard modularity.

**Answer**: False. Isolates have k_i=0 and no edges, so for any partition their terms A_ij and (k_i k_j)/(2m) are zero; 2m is unchanged. The modularity of all non-isolate assignments is identical, so the argmax set is unchanged (isolates can be placed arbitrarily).

## Shingai 🎉

**Q**: In a 2-community SBM with n=100 per community, if k=20 and δk=0, what is the expected modularity of any partition?

**Answer**: Zero. When δk=0, p_in = p_out, so the network is an Erdős-Rényi random graph with no assortative structure.

## Ted 🎉

**Q**: If you fix the number of communities k in advance for a cut‐based method, you automatically avoid the resolution limit issue found in modularity maximisation.

**Answer**: False. The resolution limit is tied to how the objective scales with network size and structure, fixing k doesn't guarantee avoidance of missing small communities.


## Urvi 🎉

**Q**: You remove one weak inter-community edge and modularity decreases. What does that imply?

**Answer**: The removed edge contributed to balancing expected vs. observed edges; modularity is non-monotonic.
