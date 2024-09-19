---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---

# Ladder Lottery

```{admonition} Ladder Lottery
:class: tip

Ladder Lottery is a fun East Asian game, also known as "鬼腳圖" (Guijiaotu) in China, "阿弥陀籤" (Amida-kuzi) in Japan, "사다리타기" (Sadaritagi) in Korea, and "Ladder Lottery" in English. The game is played as follows:
1. A player is given a board with a set of vertical lines.
2. The player chooses a line and starts to move along the line
3. When hitting a horizontal line, the player must move along the horizontal line and then continue to move along the next vertical line.
4. The player wins if the player can hit a marked line at the bottom of the board.
5. You cannot see the horizontal lines in advance!

Play the {{ '[Ladder Lottery Game! 🎮✨]( BASE_URL/vis/amida-kuji.html?)'.replace('BASE_URL', base_url) }} and try to answer the following questions:

1. Is tehre a strategy to maximize the probability of winning?
2. How does the probability of winning change as the number of horizontal lines increases?

![](https://upload.wikimedia.org/wikipedia/commons/6/64/Amidakuji_2022-05-10.gif)

```