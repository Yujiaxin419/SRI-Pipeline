## prepare transcrips for jcvi
ls test_data/*gff3 | while read fileName; 
  do echo -e "basename ${fileName/gff3}" >> sample.list;
  done

less sample.list;while read sample;
  do python -m jcvi.formats.gff bed --type=mRNA --key=ID test_data/${sample}.gff3 > test_data/${sample}.bed
  python -m jcvi.formats.bed uniq test_data/${sample}.bed
  mv test_data/${sample}.uniq.bed > test_data/${sample}.bed
  cut -f 4 test_data/${sample}.bed |seqkit grep -f - ${sample}.cds > test_data/${sample}.cds
  done
  
## generate commands of jcvi
less sample.list | while read sample1;
  do
  (less sample.list | while read sample2;
    do
    ( if [ "${sample1}" != "${sample2}" ]; then
    echo "python -m jcvi.compara.catalog ortholog ${sample1} ${sample2}" >>cmd.list;
    fi)
    done)
  done
  
ParaFly -c cmd.list -CPU 12 -failed_cmds faild.sh

## syndex
ls *lifted.anchors > 0
awk 'BEGIN{FS="."} {print $1".bed"}' > 1
awk 'BEGIN{FS="."} {print $2".bed"}' > 2
paste 0 1 2 > syn.config
rm 0 1 2

python SRI-pipeline.py syn.config syndex_out.txt
