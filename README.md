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
```
# sample1 & sample2 is a pair of genomes who needs to compare.
python -m jcvi.compara.catalog ortholog --no_strip_names ${sample1} ${sample2}
```

## Syndex calculating
```
```
