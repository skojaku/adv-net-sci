# Exercises and Assignments

## Pen-and-Paper Exercise: Why is our social network small world?

- ✍️ [It's a small world!! 6 degrees of separation](http://estebanmoro.org/pdf/netsci_for_kids/6_degrees_of_separation.pdf) {footcite}`esteban-moro-worksheet`

## Assignment

We will compute the average path length of a network of scientists. The network is constructed from {footcite:p}`sinatra2016quantifying`, where each node represents a scientist and two scientists are connected if they have co-authored a paper in Physical Review Journals from American Physical Society.

- **For students enrolled in SSIE 641**
  - You will receive a dedicated link to the assignment repository from the instructor.
- *For those who are not enrolled in SSIE 641*
  - You can access the assignment repository at [Github](https://github.com/sk-classroom/adv-net-sci-small-world).
  - This repository does not offer auto-grading. But you can grade the assignment by yourself by
    - `bash grading-toolkit/grade_notebook.sh tests/test_01.py assignment/assignment.ipynb`
    - `bash grading-toolkit/grade_notebook.sh tests/test_02.py assignment/assignment.ipynb`