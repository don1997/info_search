# Dependencies
1. nltk

## Usage
1. To startup enter: $ python3 assignment.py

2. To search for an individual token simply type the token and press enter.

3. To use a search operator such as and, or, and not.
    1. Enter the operator and ? after it.
    * ex: and? educators the
    * ex: or? the to
    2. The and_not operation requires another set of args after it.
    Enter the opertor with the ?. Then enter your terms to match and the terms to exclude with a ? in between them.
    Syntax for and_not: and_not? 'terms to match' ? 'terms to exclude'
    * ex: and_not? educators ? example
