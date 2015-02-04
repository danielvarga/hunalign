# DCEP sentence aligned corpora for 276 langugage pairs

## Basic usage

Example: How to get Danish-Lithuanian sentence-aligned text?

###### Get monolingual data

Enter a directory where the corpus building will take place.
(You can build several language pairs in this same directory.)

Download and extract the two sentence-segmented monolingual corpora:

```
wget http://optima.jrc.it/Resources/DCEP-2013/sentences/DCEP-sentence-DA-pub.tar.bz2
wget http://optima.jrc.it/Resources/DCEP-2013/sentences/DCEP-sentence-LV-pub.tar.bz2
tar jxf DCEP-sentence-DA-pub.tar.bz2
tar jxf DCEP-sentence-LV-pub.tar.bz2
```

The sentence segmented text is now in the `./DCEP/sentence/(xml|sgml)/(DA|LV)` subdirectories.

###### Get alignment data

Download and extract the alignment information:

```
wget http://people.mokk.bme.hu/~daniel/DCEP/langpairs/DCEP-DA-LV.tar.bz2
tar jxf DCEP-DA-LV.tar.bz2
```

The alignment information contains correspondence between numerical indices
of sentences, in the next step we will turn these into actual sentence pairs.

Note that the order is alphabetical in language code: `DA-LV` is good, `LV-DA` is not.
The alignment information is now in the `aligns/DA-LV` subdirectory,
and the index describing the correspondence between text documents is in the `indices/DA-LV` text file.
Bidocuments are indentified by 6 digit numeric ids.

###### Create bicorpus

Now we download, extract, and run the tool that generates the bicorpus from the above data:

```
wget http://people.mokk.bme.hu/~daniel/DCEP/DCEP-tools.tgz
tar zxvf DCEP-tools.tgz
./src/languagepair.py DA-LV > DA-LV-bisentences.txt
```

You have to have python version 2.[567] installed to run the tool.

The output is a tab-delimited UTF-8 text file with two columns.
It contains all corresponding sentence pairs identified by hunalign, the
automatic sentence aligner we used to create the alignment information.
The information about the source document of the sentence pair is lost
in this output format. See below for command line switches that can alter this
behavior.

If you don't roll your own sentence filter, we recommend to use the `--numbering-filter`
option that drops much of the numberings that are very common in the corpus:

```
./src/languagepair.py --numbering-filter DA-LV > DA-LV-bisentences.txt
```

See below for more detail.


## Advanced usage

`./src/languagepair.py -h` shows the available command line options.
Here we give a bit more background for them.

The original document structure is preserved with the `--no-merge` option.
This will create aligned text documents in `./bitexts/DA-LV`.
The numeric ids are used as file names, e.g. `bitexts/DA-LV/013563`.
The `indices/DA-LV` table can be used to find the correspondence between the bidocument and the
original DCEP filenames.

By default, the script looks for the index file describing the document pairings
at `indices/DA-LV`. This behavior can be changed with the `--index-file` argument.
Here is a Unix example that only processes the first 10 documents of the index:

```./src/languagepair.py --index-file <( head -10 indices/DA-LV ) > DA-LV-bisentences.txt```

With the `--not-just-bisentences` switch, the output format changes:
It is one alignment unit per line, where an alignment unit consists of
two tab-separated columns, one for both languages. In each column,
there is a `" ~~~ "`-separated list of sentences. It is possible that one
of the columns is empty: that means that the aligner did not find matching
pair for the other column. The default `" ~~~ "` can be changed with the
`--delimiter` command line argument.

There are command line arguments that can be used to throw away suspicious
bisentences if extra precision is required, at the expense of recall.

The `--numbering-filter` is a crude but useful heuristic that attempts to drop numberings
and short titles from the output. It works simply by matching sentences on both sides
against a Unicode regex that looks for two alphabetic characters with space between them.

The `--length-filter-level=LENGTH_FILTER_LEVEL` argument is used to throw away as suspicious
all bisentences where the ratio of the shorter and the longer sentence (in character length)
is less than `LENGTH_FILTER_LEVEL` percent.

The `--topo-filter-level=TOPO_FILTER_LEVEL` argument is used to throw away
bisentences that appear in suspicious blocks of bisegments. A block of
bisegments is determined to be suspicious if the ratio of 1-to-1 bisegments it contains
is less than `TOPO_FILTER_LEVEL` percent. The heuristic works with blocks of size 100.
This heuristic is useful to identify and remove segments of text where the original
documents differed in larger parts. (Parts were left untranslated, different order of chapters, etc.)

