#!/usr/bin/env bash

# Generates the Table of contents for a Markdown
# file and inserts the TOC in the file


mdfile="README.md"
tmpfile=$(mktemp)

toc_begin="[//]: # (AUTO TOC BEGIN)"
toc_end="[//]: # (AUTO TOC END)"


# escaping special characters to use variables in regex
toc_begin_reg=${toc_begin/[/\\[}
toc_begin_reg=${toc_begin_reg//\//\\/}
toc_begin_reg=${toc_begin_reg/(/\\(}
toc_begin_reg=${toc_begin_reg/\)/\\\)}

toc_end_reg=${toc_end/[/\\[}
toc_end_reg=${toc_end_reg//\//\\/}
toc_end_reg=${toc_end_reg/(/\\(}
toc_end_reg=${toc_end_reg/\)/\\\)}


# delete everything before TOC  (including the TOC itself)
perl -0777 -p -e "s/.*$toc_end_reg//s" $mdfile > $tmpfile

# delete all lines except headlines (starting with '#')
perl -p -i -e 's/^[^#].*\n//' $tmpfile

# delete all empty lines
perl -p -i -e 's/^\n//' $tmpfile


# replace all '#' at beginning with same amount of double spaces (indenting)
perl -p -i -e 's/^ *(#+)/"  " x (length($1)-1)/eg' $tmpfile

# surround headline with [] and add (#...) lowercase anchor
perl -p -i -e 's/^( *) (.*)/"$1* [$2](#".lc($2).")"/e' $tmpfile


# replace non alphanum characters in anchor
perl -p -i -e 's/(?: *\* *\[.*\]\(#|\G(?<!^))(?:[a-z0-9 ]+)*\K[^a-z0-9 \n]//g&&s/$/)/' $tmpfile

# replace space in anchor with hyphen
perl -p -i -e 's/(?: *\* *\[.*\]\(#|\G(?<!^))(?:[^ ]+)*\K /-/g' $tmpfile


# insert TOC in readme
toc=$(cat $tmpfile)
perl -0777 -p -i -e "s/(?<=$toc_begin_reg).*(?=$toc_end_reg)/\n\n$toc\n\n/s" $mdfile


rm $tmpfile
