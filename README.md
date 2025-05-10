# Busy Beaver project
 This project aim to familiarize myself with the Busy Beaver problem and the multiple methods and mathematical concepts used in this challenge. I profusely use the [bbchallenge.org](https://bbchallenge.org) Wiki/Documentation to make this p    roject possible. The code will mainly be in Python but I do not exclude a future where I see myself using C/C++ as it isn't a language I am at ease with. I will try to keep a [log](https://docs.google.com/document/d/1KZJ1Nu9Quzz82vr_PGDgmZnZ-_PK_ruw39SiqjyxU7U/edit?usp=sharing) (in the form of a Google Docs) of what I came across, what I find useful and what is to come. The [Tasks](#tasks) section will keep the record of the project's progress

## Tasks

First, I will focus on the $BB(2)$ problem. Trying to find the champion and verify the well known result: $BB(2)=6$. Bellow is a list of tasks to achieve this goal:

- [ ] Create ```TuringMachine``` class, $n$-states, $m$-symbol, $0$-all tape: 

  - [ ] From a list of string (ex: ```1RB---_1LB1LB```), initialize the machine
  - [ ] With a time/space limit, run the TM and label it (```HALT```, ```NON-HALT```, ```HOLDOUT```)
  - [ ] Implement a Space-time diagrams function to visualize the TM.

- [ ] For $n=2$, create naively the dataset of all the 2-state TM in the correct [format](https://bbchallenge.org/method#format) and save them on a binary file.
- [ ] For $n>2$, create thee dataset using methods like Tree Normal Form (TNF)

- [ ] Implement a Decider for [Translated Cycler TM](https://wiki.bbchallenge.org/wiki/Translated_cycler)


