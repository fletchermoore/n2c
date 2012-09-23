n2c
===

Converts a formatted notes file to tab delimited cards


Example
-------
An input file written as such:
```
* cystic fibrosis
{symptoms} 
chronic cough
wheezing
other problems // this isn't everything
{most commonly mutated gene} delF508
{<<} most common autosomal recessive disorder in caucasians
{<<associated with} pancreatic insufficiency

? what about other mutations?

* CTFR
{stands for} cystic fibrosis transmembrane regulator // right?

*cystic fibrosis
{acronym|stands for} CF 
{:} an inherited autosomal recessive disorder
```

will produce an output file that looks like:
```
cystic fibrosis: symptoms	chronic cough<br>wheezing<br>other problems
cystic fibrosis: most commonly mutated gene	delF508
most common autosomal recessive disorder in caucasians	cystic fibrosis
pancreatic insufficiency: associated with	cystic fibrosis
CTFR: stands for	cystic fibrosis transmembrane regulator
cystic fibrosis: acronym	CF
CF: stands for	cystic fibrosis
cystic fibrosis	an inherited autosomal recessive disorder
learn: what about other mutations?	(no back)
```


Explanation
-----------

`*` followed by some text sets the current subject. all subsequent
cards will be related to this subject. The subject must be one line.

Curly brackets establish a card. The simplest card uses `{:}`. The
current subject become the front and the text that follows the `}`
becomes the back. The back can be multiple lines. Line breaks are
converted to HTML `<br>` tag.

If text is given between the curly brackets, that text is suffixed to
the subject.

`{<<text}` creates a reverse card with `text` as the prompt

`{forward prompt|reverse prompt}` creates two cards: a forward and a
reverse card, each with the respective prompt as a suffix.



Current Issues
--------------
Only handles linux style line breaks `\n`.


TODO
----
* Implement as Anki 2 plugin.
* Fix line breaks for windows.
* Change output file name.
