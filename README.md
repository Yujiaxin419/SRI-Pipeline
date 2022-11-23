# Syndex-pipeline
## Introduction
**Syn**(teny) (in)**dex** is a score that quantifies synteny between two genomes. syndex calculating is based on the result of JCVI [links](https://github.com/tanghaibao/jcvi). This pipeline contains few steps:

## Syntenty inference through JCVI
1. get longest uniq transcripts
```

python -m jcvi.formats.gff bed --type=mRNA --key=ID ${gff3} > ${gff3/gff3/bed}
python -m jcvi.formats.bed uniq ${gff3/gff3/bed}
mv uniq.bed ${sample}.bed
cut -f 4 ${sample}.bed |seqkit grep -f - ${gff3/gff3/cds} > ${sample}.cds
```
2. Syntenty inference
```bash
# sample1 & sample2 is a pair of genomes who needs to compare.
python -m jcvi.compara.catalog ortholog --no_strip_names ${sample1} ${sample2}
```

## Syndex calculating
```
python syndex.py <syn.config> <output>
```
- the format of `syn.config` file should be:
```
## Anchore file from jcvi A.bed B.bed
A6-26.E4-63.lifted.anchors      A6-26.bed       E4-63.bed
A6-26.PG0009.lifted.anchors     A6-26.bed       PG0009.bed
A6-26.PG1008.lifted.anchors     A6-26.bed       PG1008.bed
```

## Output
- The ouput file looks like:
```
#sample_pair    syndex
An-1,C24        0.9769
An-1,Cvi        0.9757
An-1,Eri        0.9773
Kyo,An-1        0.9732
An-1,Ler        0.9754
Sha,An-1        0.9719
```
