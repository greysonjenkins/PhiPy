# Theory *(WIP)*
To-do: Complete draft, proofing, revisions, additional sections
## Boolean Logic

---
## Propositional Logic

---
## Predicate Logic
Predicate logic (also called first-order logic or quantified logic) builds on the fundamentals of propositional calculus/sentential logic.

---
## Finite State Machines (FSMs)
A finite state machine (FSM) is a type of computational model, usually represented by a state diagram. An FSM reads a string of symbols to changes states; the state it transitions to depends on its current state and input. Finite automatons are one type of finite state machine.

Formally, we can define a finite automaton as a 5-tuple (_Q_, Σ, δ, _q<sub>0</sub>_, _F_), where:
- _Q_ is a finite set of **states**,
- Σ is a finite set of symbols called the **alphabet**,
- δ: _Q_ × Σ → _Q_ is a **transition function**,
- _q<sub>0</sub>_ ∈ _Q_ is the **start state**,
- _F_ ⊆ _Q_ is a set of **accept states**.

We can think of δ as any other type of function that takes inputs and produces outputs:\
It uses two inputs, the current state and a symbol, to compute its output, which is the state to transition to. 
For example, δ(_q<sub>0</sub>_, 1) = _q<sub>1</sub>_ is a function that transitions from the current state _q<sub>0</sub>_ to _q<sub>1</sub>_ if the input is 1.

---
### Example: Constructing Finite Automata
Let _M_<sub>1</sub> be a finite automaton (_Q_, Σ, δ, _q<sub>1</sub>_, _F_), where:
1. _Q_ = {_q<sub>1</sub>_, _q<sub>2</sub>_, _q<sub>3</sub>_}
2. Σ = {0,1}
3. δ = {\
_q<sub>1</sub>_ × 0 → _q<sub>1</sub>_\
_q<sub>1</sub>_ × 1 → _q<sub>2</sub>_\
_q<sub>2</sub>_ × 0 → _q<sub>3</sub>_\
_q<sub>2</sub>_ × 1 → _q<sub>2</sub>_\
_q<sub>3</sub>_ × 0 → _q<sub>2</sub>_\
_q<sub>3</sub>_ × 1 → _q<sub>2</sub>_\
}
4. Start state = _q<sub>1</sub>_
5. _F_ = _q<sub>2</sub>_

That's not very helpful, but it's pretty straightforward to design the corresponding finite state machine which should be more useful.
First, let's consider what the above definition tells us:

_M_<sub>1</sub> is a finite automaton with three states, _q<sub>1</sub>_, _q_<sub>2</sub>, _q_<sub>3</sub>. The alphabet consists of two symbols, 0 and 1.
From the start state _q_<sub>1</sub>, we loop back to _q_<sub>1</sub> if the symbol is 0, and transition to _q<sub>2</sub>_ if the symbol is 1.
From _q_<sub>2</sub>, transition to _q_<sub>3</sub> on 0 and _q_<sub>2</sub> on 1. From _q_<sub>3</sub>, we transition to _q_<sub>2</sub> on 0 or 1.
Now, let _A_ be the set of all strings that _M_<sub>1</sub> accepts. We say _M_<sub>1</sub> **recognizes** _A_ if it accepts all possible strings in _A_. A string is accepted by a finite automaton if the string terminates in a final state.

[FSM diagrams soon]

---
## Context-Free Grammars (CFGs)
Context-free grammars are one way to describe languages. Compared to regular expressions or finite automata, they capture greater 
nuance in languages because of the way they describe relationships between concepts and phrases. For example, verb phrases might 
contain noun phrases, and noun phrases may contain verb phrases. More abstract propositional/sentential logic is too high-level to 
capture these kinds of linguistic structures and relations.

Formally, we can define a CFG using a 4-tuple (*V*, Σ, *R*, *S*), where:
- _V_ is a finite set of **variable** symbols,
- Σ is a finite set, disjoint with _V_, of **terminal** symbols,
- _R_ is a finite set of *rules*, and each rule is a variable producing a string of variables and/or terminals, and
- _S_ ∈ _V_ is the start variable.

Take grammar *G<sub>1</sub>* as an example:

_G_<sub>1</sub> = ({_A_, _B_}, {0, 1, #}, _R_, _A_)

Where the set of rules _R_ =
- _A_ → 0*A*1
- _A_ → _B_
- _B_ → #

*G<sub>1</sub>* has two variable symbols: _A_ and _B_. _A_ is the start symbol.
The grammar also has three terminal symbols: 0, 1, and #. _A_ and _B_ are non-terminal variables, which means they can produce other variable symbols.
By contrast, terminal symbols cannot produce additional variables. Each line in the grammar is a _rule of production_.
You might also think of them as substitution rules. In *G<sub>1</sub>*, the first rule tells us that the symbol _A_ can be replaced by 0*A*1.
The _A_ in 0A1 can once again produce 0*A*1 or _B_. Additionally, notice that the variable symbol _A_ occurs twice on the left-hand side of the rules.
We can simplify the rule set by combining the first two lines into one, such that _R_ =
- _A_ → 0*A*1 | _B_ (read as _A_ produces 0*A*1 **OR** _A_ produces _B_)
- _B_ → #

Furthermore, we can also simplify the rules of production by converting the grammar into *Chomsky normal form*. A grammar is in Chomsky normal form if it has the following form:
- _A_ → _BC_
- _A_ → a,

where:
- a is any terminal symbol,
- _A_, _B_, and _C_ are variable symbols **AND** _B_ and _C_ are not the start variable, and
- The rule _S_ → ε is permitted, where _S_ is the start symbol and can produce the empty string (ε).

---
## Deriving Strings
Here is how we might derive a string using the grammar (the parentheses indicate the terminals introduced in that step of deriving a string):

A → (0A1) → 0(0A1)1 → 00(0A1)11 → 000(B)111 → 000(#)111

The above shows a *derivation* of a string, 000#111, from _G_<sub>1</sub>. The first rule of production used was _A_ → 0*A*1. Then, rule one was used again to derive 00*A*11, and then a third time to derive 000*A*111.
Then, we used the second rule, _A_ → _B_, yielding the string 000*B*111. Now that we no longer have _A_ in the string, we cannot produce 0*A*1.
Instead, as we now have B in the string, we can only derive the final string 000#111. This is because _B_ can only produce the # symbol, which does not have any further production rules in the grammar.

You might have noticed that the grammar can only yield a specific type of string: one with # as the middle symbol, with _n_ 0's to the left and _n_ 1's to the right.
Here's the grammar in its original form again:\
_G<sub>1</sub>_ = ({_A_, _B_}, {0, 1, #}, _R_, _A_)

Where the set of rules _R_ =
- _A_ → 0*A*1
- _A_ → _B_
- _B_ → #

For clarity, all of the following strings could then be derived from _G_<sub>1</sub>:
- _A_ → _B_ → #
- _A_ → 0*A*1 → 0*B*1 → 0#1
- _A_ → 0*A*1 → 00*A*11 → 00*B*11 → 00#11
- _A_ → 0*A*1 → 00*A*11 → 000*A*111 → 000*B*111 → 000#111
- _A_ → 0*A*1 → 00*A*11 → 000*A*111 → 0000*A*1111 → 0000*B*1111 → 0000#1111

Thus, we can describe the *language* of *G<sub>1</sub>* as *L*(*G<sub>1</sub>*) = {0<sup>n</sup>#1<sup>n</sup> | n ≥ 0}. In other words, the language is the set of all strings that can be generated by the grammar. Languages generated by context-free grammars are called *context-free languages* (CFLs)

