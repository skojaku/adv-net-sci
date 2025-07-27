# M04 Concepts: The Friendship Paradox

## What We Learn in This Module

In this module, we will learn about the friendship paradox. Specifically:
- Friendship paradox: what is it, why it's important, and what are the consequences?
- **Keywords**: friendship paradox, degree bias

## In-Class Experiment

"Your friends have more friends than you" is a well-known phenomenon in social networks. It appears everywhere from physical social networks to online social networks, and even random networks!
OK. Let's do not "think" but "feeeeel" this paradox through the following in-class experiment.

## Experiment Materials and Procedure

**Materials:**
- [📇 Friendship card](./friendship-cards.pdf)
- 🖊️ Pen

**Friendship Network Experiment:**

```
┌─────────────────────────────────────────────────────────────┐

   1. [📇] Receive Your Card
      Get a card with a unique letter

   2. [🤝] Meet and Greet (5 mins)
      Move around, exchange cards with at least one friend

   3. [🧮] Count Connections (2 mins)
      Count received cards, write number, return cards

   4. [📈] Calculate Average (2 mins)
      Calculate average 'friend count' of your friends

   5. [📝] Fill Form
      Write your average and your own friend count
      in a separate sheet

└─────────────────────────────────────────────────────────────┘

❗ Important Notes:
  • This is a fun experiment, not a popularity contest
  • Be respectful and inclusive during the meet and greet
  • If you finish early, wait patiently for further instructions
```

## The Friendship Paradox Explained

## The Origin of the Friendship Paradox

The paradox arises not because of the way we form friendships. It's about measurement! For example a person with 100 friends generates 100 cards, while a person with 1 friend generates only 1 card. If we average friend counts over the cards, popular people are counted more. This is where the friendship paradox comes from.

In network terms, cards represent edges and people represent nodes. The friendship paradox arises because we measure at different levels: nodes or edges. The average friend count at the node level is lower than at the edge level because popular people are counted more often at the edge level.

## Key Questions to Consider

- **🎉 Fun Challenge**: Can you create a network where your friends have the most friends? 🤔💡 Give it a try in this [Friendship Paradox Game! 🎮✨](../assets/vis/friendship-paradox-game.html)

- **Question**: Can you create a network where the friendship paradox is absent? In other words, can you create a graph, where your friends have the same number of friends as you?

## Practical Applications: Vaccination Game

Beyond an interesting trivia, the friendship paradox has many practical utilities.

## Strategic Vaccination

The friendship paradox has important implications for public health strategies. By understanding that highly connected individuals are more likely to be selected through their connections, we can develop more effective vaccination strategies.

- **🎉 Fun Challenge**: Can you control the spread of a virus by strategically vaccinating individuals? 🤔💡 Give it a try in this [Vaccination Game! 🎮✨](../assets/vis/vaccination-game.html)

## Why Vaccination Strategy Works

When we vaccinate people chosen through the friendship paradox principle:
1. We're more likely to vaccinate highly connected individuals
2. Highly connected people are more likely to spread diseases
3. Vaccinating them creates a disproportionate impact on disease spread
4. This strategy is more effective than random vaccination

## Mathematical Foundation

The friendship paradox can be understood through the concept of degree bias:

- **Node sampling**: Selecting people randomly gives equal weight to everyone
- **Edge sampling**: Selecting people through their connections gives higher weight to popular people
- **Result**: Edge sampling systematically overrepresents high-degree nodes

This mathematical insight has applications beyond friendships, including:
- Social network analysis
- Epidemiology and disease control
- Marketing and influence strategies
- Network robustness and vulnerability assessment