## The hunalign sentence aligner

### Introduction

hunalign aligns bilingual text on the sentence level. Its input is
tokenized and sentence-segmented text in two languages. In the
simplest case, its output is a sequence of bilingual sentence pairs
(bisentences). 

In the presence of a dictionary, hunalign uses it, combining this
information with Gale-Church sentence-length information. In the absence
of a dictionary, it first falls back to sentence-length information,
and then builds an automatic dictionary based on this alignment. Then it
realigns the text in a second pass, using the automatic dictionary.

Like most sentence aligners, hunalign does not deal with changes of
sentence order: it is unable to come up with crossing alignments, i.e.,
segments A and B in one language corresponding to segments B' A' in the
other language.

There is nothing Hungarian-specific in hunalign, the name simply 
reflects the fact that it is part of the hun* NLP toolchain.

hunalign was written in portable C++. It can be built under
basically any kind of operating system.

### Download

Hunalign source code package: 

[
         ftp://ftp.mokk.bme.hu/Hunglish/src/hunalign/latest/hunalign-1.1.tgz](ftp://ftp.mokk.bme.hu/Hunglish/src/hunalign/latest/hunalign-1.1.tgz)

You can browse this package online here:

[
         ftp://ftp.mokk.bme.hu/Hunglish/src/hunalign/latest/hunalign-1.1/](ftp://ftp.mokk.bme.hu/Hunglish/src/hunalign/latest/hunalign-1.1/)

For convenience, precompiled Windows binaries are provided here:

[
         ftp://ftp.mokk.bme.hu/Hunglish/src/hunalign/latest/hunalign-1.1-windows.zip](ftp://ftp.mokk.bme.hu/Hunglish/src/hunalign/latest/hunalign-1.1-windows.zip)

Note that this is not a complete hunalign distribution, just the Windows binaries alone.
The source package is still a recommended download, complementing the binaries with
offline documentation, language resources and additional tools.

### Build

#### Build under Linux/Unix/Mac OS X:

<pre>tar zxvf hunalign-1.1.tgz
cd hunalign-1.1/src/hunalign
make
</pre>

The make yields a single application binary src/hunalign/hunalign .

#### Build under Windows:

As already noted, precompiled Windows binaries are provided.
But it is easy to build from source under Windows, too.
With CYGWIN installed, make should work.
Using MSVC++, just create a project with the
src/hunalign/\*.cpp and src/utils/\*.cpp files in it, excluding the obsolete
src/hunalign/DOMTreeErrorReporter.cpp
src/hunalign/similarityEvaluator.cpp and
src/hunalign/TEIReader.cpp source files.
The src/include directory must be in the include path.

### Basic usage

Let us assume that you are in the top level directory (where
this readme file resides). All referenced files are meant relative to this directory.
If you use the precompiled Windows binaries, copy them here from their directory.

The build can be tested and basic usage can be understood by typing the following:

<pre>src/hunalign/hunalign data/hu-en.stem.dic examples/demo.hu.stem examples/demo.en.stem \
    -hand=examples/demo.manual.ladder -text > /tmp/align.txt
less /tmp/align.txt
</pre>

Similarly, for Windows, this would be (in one line):

<pre>hunalign.exe data\hu-en.stem.dic examples\demo.hu.stem examples\demo.en.stem
    -hand=examples\demo.manual.ladder -text > align.txt
more align.txt
</pre>

Here, the input files 'examples/demo.hu.stem' and
'examples/demo.en.stem' contain Hungarian and English test data
respectively, both segmented into sentences (one sentence per line) and
into tokens (delimited by space characters). The output
(in this case the file '/tmp/align.txt') contains the aligned segments (one
aligned segment per line). As a result of the option '-text', the
actual text of the segments (rather than their indexes) are written to
the output making it suitable for human reading. For details see
section "File formats". The argument '-hand' specifies a file
containing a manual alignment. This argument can be omitted, but when
given, the automatic alignment is evaluated against the manual
alignment.

### Command-line arguments

The simple argument-parser accepts switches (e.g. -realign) or
key-value pairs, where value can be integer or string. The key and
value can be separated by the '=' sign, but whitespace is NOT allowed.
For string values, the '=' is mandatory. For example, "-thresh50",
"-thresh=50" and "-hand=manual.align" are OK, "-thresh 50", "-hand
manual.align" and "-handmanual.align" are not. The order of the
arguments is free.

Usage (either):

<pre>hunalign [ common_arguments ] [ -hand=hand_align_file ] dictionary_file source_text target_text
</pre>

or (batch mode, see section Batch mode):

<pre>hunalign [ common_arguments ] -batch dictionary_file batch_file
</pre>
where common_arguments ::= [ -text ] [ -bisent ] [ -utf ] [ -cautious ]
[ -realign [ -autodict=filename ] ]
[ -thresh=n ] [ -ppthresh=n ] [ -headerthresh=n ] [ -topothresh=n ]

The dictionary argument is mandatory. This is not a real
restriction, though. In lack of a real bilingual dictionary, one can
provide a zero-byte file such as data/null.dic.

The non-mandatory options are the following:

<pre>
-text
    The output should be in text format, rather than the default (numeric) ladder format.

-bisent
    Only bisentences (one-to-one alignment segments) are printed. In non-text mode, their
    starting rung is printed.

-cautious
    In -bisent mode, only bisentences for which both the preceding and the following
    segments are one-to-one are printed. In the default non-bisent mode, only rungs
    for which both the preceding and the following segments are one-to-one are printed.

-hand=file
    When this argument is given, the precision and recall of the alignment is calculated
    based on the manually built ladder file. Information like the following is written
    on the standard error: 
    53 misaligned out of 6446 correct items, 6035 bets.
    Precision: 0.991218, Recall: 0.928017

  Note that by default, 'item' means rung. The switch -bisent also changes the semantics
    of the scoring from rung-based to bisentence-based and in this case 'item' means bisentences.
    See File formats about the format of this input align file.

-realign
    If this option is set, the alignment is built in three phases.
    After an initial alignment, the algorithm heuristically adds items
    to the dictionary based on cooccurrences in the identified bisentences.
    Then it re-runs the alignment process based on this larger dictionary.
    This option is recommended to achieve the highest possible alignment quality.
    It is not set by default because it approximately triples the running time
    while the quality improvement it yields are typically small.

-autodict=filename
    The dictionary built during realign is saved to this file. By default, it is not saved.

-utf
    The system uses the character counts of the sentences as information for the
    pairing of sentences. By default, it assumes one-byte character encoding such
    as ISO Latin-1 when calculating these counts. If our text is in UTF-8 format,
    byte counts and character counts are different, and we must use the -utf switch
    to force the system to properly calculate character counts.
    Note: UTF-16 input is not supported.

Postfiltering options:
There are various postprocessors which remove implausible rungs based on various heuristics.

-thresh=n
    Don't print out segments with score lower than n/100.

-ppthresh=n
    Filter rungs with less than n/100 average score in their vicinity.

-headerthresh=n
    Filter all rungs at the start and end of texts until finding a reliably
    plausible region.

-topothresh=n
    Filter rungs with less than n percent of one-to-one segments in their vicinity.

All these 'thresh' values default to zero (i.e., no postfiltering).
Typical sensible values are -ppthresh=30 -headerthresh=100 -topothresh=30
Postfiltering is only recommended if there are large or frequent mismatching
segments AND you want to optimize heavily for precision at the expense of recall.
</pre>

### Batch mode

If we use the -batch switch the aligner expects a batch file instead of the
usual two text files. The batch file contains jobs, one per row. A job is
tab-separated sequence of three file names containing the source text, the
target text, and the output, respectively. The batch mode saves time over
shell-based batching of jobs by reading the dictionary into memory only once.

In batch mode, for every job, there is an align quality value written on standard error.
This line has the format "Quality \t output_file \t quality_value" so it can be automatically
processed.

### File formats

The aligner reads and/or writes the following file formats:

#### Bicorpus:

The input files containing the texts to be aligned are standard text
files. Each line is one sentence and word tokens are separated by spaces. If a
line consists of a single &lt;p&gt; token, it is treated specially, as a paragraph
delimiter. Paragraph separators are treated as virtual sentences, the aligner
tries to match these with each other and never aligns them with a real
sentence.

#### Alignments:

The format of the alignment output comes in two flavors: 
text style (-text switch) or ladder style (default).

- Text format of alignments. Each line is tab-separated into three
columns. The first is a segment of the source text. The second is a
(supposedly corresponding) segment of the target text. The third column is a
confidence value for the segment. Such segments of the source or target text
will typically (or hopefully) consist of exactly one sentence on both
sides. But it can consist of zero or more than one sentences also. In the
latter case, the separating sequence " ~~~ " is placed between sentences. So
if this sequence of characters may appear in the input, one should use the
ladder format output.

- Ladder format of alignments. Alignments are described by a newline-separated
list of pairs of integers represented by the first two columns of the ladder
file. Such a pair is called a rung. The first coordinate denotes a position in
the source language, the second coordinate denotes a position in the target
language. A rung (n,m) means the following: The first n sentences of the
source text correspond to the first m sentences of the target text. The rungs
cannot intersect (e.g., (10,12) (11,10) is not allowed), which means that the
order of sentences are preserved by the alignment. The first rung is always
(0,0), the last one is always
(sentenceNumber(sourceText),sentenceNumber(targetText)). The third column of
the ladder format is a confidence value for the segment starting with the
given rung. The columns of the ladder file are separated by a tab.
The ladder2text tool (see below) can be used to build human-readable
text format from a ladder format file.

 The format of the input alignment file (manually aligned file for
evaluation, see '-hand' option in section Command line arguments) can only be
given as a ladder. This format is identical to the first two columns of output
ladder format just described.

#### Dictionary:

The dictionary consists of newline-separated dictionary items. An item
consists of a target language phrase and a source language phrase, separated by
the " @ " sequence. Multiword phrases are allowed. The words of a phrase are
space-separated as usual. IMPORTANT NOTE: In the current version, for
historical reasons, the target language phrases come first. Therefore the ordering is
the opposite of the ordering of the command-line arguments or the results.

### Tools

There are several tools aiding hunalign.

#### ladder2text

The preferred output format for hunalign is the ladder format. The scripts/ladder2text.py
tool can turn this into text format. Usage:

<pre>scripts/ladder2text.py ladder_file corpus_in_first_lang corpus_in_second_lang > aligned_text</pre>

Note that you can run hunalign on tokenized (or even tokenized and stemmed) text,
and then run ladder2text on the original nontokenized text to get nontokenized,
aligned bitext.

#### partialAlign

hunalign starts to eat a bit too much memory when the number of sentences in the input files
is above about ten thousand. scripts/partialAlign.py is a tool to work this around.
It cuts a very large sentence-segmented unaligned bicorpus into smaller parts manageable
for hunalign.

Usage (write in one line): 
<pre>scripts/partialAlign.py huge_text_in_one_language huge_text_in_other_language
    output_filename name_of_first_lang name_of_second_lang
    [ maximal_size_of_chunks=5000 ] > hunalign_batch
</pre>

The two input files must have one line per sentence. Whitespace-delimited tokenization
is preferred. The output is a set of files named output_filename_[123..].name_of_lang
The standard output is a batch job description for hunalign, so this command can and should be
followed by:

<pre>hunalign dictionary.dic -batch hunalign_batch</pre>

partialAlign works by finding words that occur exactly twice in the bidocument,
once on the left and once on the right side.
After collecting all such correspondences, the algorithm uses dynamic programming
to find the longest possible chain of correspondences that does not contain
crossings. (A crossing is an incompatible pair of correspondences that can not
be refined into an alignment.) The chain is then thinned to make final chunk sizes close to
maximal_size_of_chunks.

A file named output_filename.poset is written that logs which correspondences are
used and which are excluded as false positives. This log can be used to manually check for mistakes,
but normally this is not necessary, as the output of the algorithm is very reliable.

#### LF Aligner

<p>András Farkas wrote and maintains a very useful wrapper around hunalign and partialAlign.
Its input is a document pair in some popular rich text format, and its output
is a set of extracted bisentences in txt, xls or tmx (translation memory) formats.
It deals with document format conversion, sentence segmentation and other stuff,
hiding all the messy details from the user. For most people other than natural
language processing professionals, it is recommended over hunalign.

[LF Aligner has its own page.](http://sourceforge.net/projects/aligner/)
It bundles hunalign so its users don't even have to set hunalign up for themselves.

### For developers

If you intend to modify the hunalign source code, note that 
there are some parameters of the algorithm which are hardwired into the source
code because modifying them does not seem to result in any improvements. These
arguments are local variables (typically bool or double), and always have
variable names of the form quasiglobal_X, X being some mnemonic name for the
parameter in question, e.g., 'stopwordRemoval'. In some cases these variables
hide nontrivial functionality, e.g., quasiglobal_stopwordRemoval,
quasiglobal_maximalSizeInMegabytes. It is quite straightforward to turn these
quasiglobals to proper command line arguments of the program.

### License

hunalign is licensed under the GNU LGPLv3 or later.

### Reference

If you use the software, please reference the following paper:

D. Varga, L. Németh, P. Halácsy, A. Kornai, V. Trón, V. Nagy (2005).
**Parallel corpora for medium density languages**
_In Proceedings of the RANLP 2005_, pages 590-596.
[(pdf)](http://www.kornai.com/Papers/ranlp05parallel.pdf)


hunalign was developed under the Hunglish Project to build the
[Hunglish Corpus](http://mokk.bme.hu/resources/hunglishcorpus).
