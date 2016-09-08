#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# mostly written by Kirill Tsyganov

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]

import sys, re, os, argparse
import gzip

def crispr_report_sample_list(vcfFiles):
    sample_list=list()
    
    vcfs = os.listdir(vcfFiles)
    
    for item in sorted(vcfs, key=natural_keys):
        if item.endswith(".vcf.gz") or item.endswith('.vcf'):
            sample_list.append(item)
            
    return sample_list


def crispr_report_sample_info(vcfFiles, bamFiles, vcf, threshold = 1000):
    
    change_list = dict()
    
    # lazy refactor :)
    item = vcf
    
    gziped = item.split('.')[-1]
    if gziped == 'gz':
        vcfFile = gzip.open(os.path.join(vcfFiles, item), 'rb')
    else: 
        vcfFile = open(os.path.join(vcfFiles, item))

        #bamFile = open(os.path.join(bamFiles, item.split("_")[0]+"_sorted.bam"))
        bamFile = item.split(".")[0]
        bamFile = bamFile.split("_")[0]+"_sorted.bam"
        tmpName = item.split(".")[0]
        name = 'Sample-%s' % tmpName
        counter=0
        check=''
        change_list=list() 

        for i in vcfFile:
            items = i.strip().split()

            if not i.startswith("#"):
                m = re.search("(DP=)([0-9]+)", items[7])
                depth = int(m.group(2))
                chrom = items[0]
                position = int(items[1])
                upstream = position-200
                downstream = position+200
                locus = "%s:%s-%s" % (chrom, upstream, downstream)
                #igvLink = igvTemplate % (bamFile, bamFile, locus)

                # LOGIC HERE
                #print depth
                if m and depth > threshold:

                    tmp_changedict = dict()
                    tmp_changedict['name'] = name
                    tmp_changedict['vcf'] = item
                    tmp_changedict['chrom'] = chrom
                    tmp_changedict['locus'] = locus
                    tmp_changedict['bam'] = bamFile             
                    tmp_changedict['position'] = position
                    tmp_changedict['reference'] = items[3]
                    tmp_changedict['alternative'] = items[4]
                    tmp_changedict['quality'] = items[5]
                    tmp_changedict['depth'] = depth    

                    change_list.append(tmp_changedict)
    
    return change_list

#vcfFiles = '/home/kirill/projects/MichelleMeilak/firstRun-pilotGenotype/freebiTestRun'
#bamFiles = '/home/kirill/projects/MichelleMeilak/firstRun-pilotGenotype/bams-arch'

#print crispr_report_sample_list(vcfFiles)
#print crispr_report_sample_info(vcfFiles, bamFiles, '22_freebayes.vcf')