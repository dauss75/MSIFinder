###########MSIFinder##############
requested other softwares as follow:
bedtools(v2.28.0)
msisensor(v0.6)
fastahack
requested python packages as follow:
pandas(0.23.4)
pysam(0.15.1)
Bams file:
Quality control and preprocessing of FASTQ files was done by fastp (version 0.19.3), to obtain clean reads. Next, clean reads mapping against the human reference genome (hg19/GRCh37) and alignment processing were performed using BWA (version 0.7.12-r1039) and SAMtools (version 0.1.19-96b5f2294a). Subsequently, sample-level, fully local indel realignment was performed using GATK (version 4.1.0.0) and duplicate reads removed using Picard (version 1.72). Quality score recalibration was then performed using GATK to generate the final realignment and recalibration BAM, which was used for subsequent analyses.
###First###
use scan_msiloc.py get all ms loc in your panel 
such as "python scan_msiloc.py -msisensor /yourpath/msisensor -ref hg19 -bed yourpanel -o all_msi_loc.txt"
###Second###
use model 'make control' of MSIdetect_v3.py and all_msi_loc.txt to analyze your control normal bams files
such as "python MSIdetect_v3.py -mkc True -fastahack /youpath/fastahack -rf hg19 -bam bamfile -bed all_msi_loc.txt -o control_normal_bams_outdir -p patientid" for all your control normal bam files
###Third###
use create_baseline_v2.py to assess the results of model 'make control' of MSIdetect_v3.py to obtain the average depth file
such as "python create_baseline_v2.py -d control_normal_bams_outdir/*_MSIscore.xls -o MSI_average_depth.txt"
###Fourth###
use “train1.py” to analyze the training set(some MSI-positive samples and MSI-negative samples)
such as "python train1.py -fastahack /youpath/fastahack -qc MSI_average_depth.txt -rf hg19 -bam bamfile -bed all_msi_loc.txt -o positive_dir -p patientid" for your MSI-positive sample's bam files
such as "python train1.py -fastahack /youpath/fastahack -qc MSI_average_depth.txt -rf hg19 -bam bamfile -bed all_msi_loc.txt -o negative_dir -p patientid" for your MSI-negative sample's bam files
###Fifth###
use “train2.py” to analyze the training data results get bed.txt and peaks.txt
such as "python train2.py -qc MSI_average_depth.txt -positive_dir positive_dir -negative_dir negative_dir"
###Sixth###
use MSIdetect_v3.py to analyze your new sample's bams files and get this sample's MS status
such "python MSIdetect_v3.py -fastahack /youpath/fastahack -rf hg19 -bam new_bamfile -bed bed.txt -ctr peaks.txt -o outdir -p patientid"