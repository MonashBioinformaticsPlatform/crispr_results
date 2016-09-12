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

def sub_bam_filename(bam_file):
    prefix = bam_file.rsplit('.')
    bam_file = "%s_sub.bam" % prefix[0]
    return bam_file

def sub_sample_bam(bam_file):
    if os.path.isfile(bam_file):
        return    
    
    import subprocess
    # todo handle different subsample
    process = subprocess.Popen(('samtools view -s 0.0003 -b %s > %s') % \
                               (bam_file,
                               sub_bam_filename(bam_file)),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True)
    # todo handle non zero
    process.wait()
    for line in process.stdout:
        print line
    
    for line in process.stderr:
        print line

def sub_index_bam(bam_file):  
    if os.path.isfile(bam_file):
        return
    
    import subprocess

    process = subprocess.Popen(('samtools index %s') % \
                               (bam_file),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True)
    # todo handle non zero
    process.wait()
    for line in process.stdout:
        print line
    
    for line in process.stderr:
        print line        

def render_indel_html(chrom, pos, ref_seq, alt_seq,
                      twobit_file = 'ref/mm10.2bit', boundary = 20):
    import twobitreader
    
    boundary = boundary + 1

    twobit_ref = twobitreader.TwoBitFile(twobit_file)
    
    ref_length = len(ref_seq)
    alt_length = len(alt_seq)
    
    # pad by whichever seq is longest
    bounds = [ref_length + boundary, alt_length + boundary]
    boundary_end = max(bounds)
    
    # is indel a direct sub, a delete or insert?
    # this affects colours rendered in sequence also
    in_or_del = 'sub'
    if ref_length > alt_length:
        in_or_del = 'delete'
    elif ref_length < alt_length:
        in_or_del = 'insert'
    
    startpos = pos - boundary
    endpos = pos + boundary

    prefix = twobit_ref[chrom][startpos:pos-1]
    suffix = twobit_ref[chrom][pos+ref_length-1:endpos+ref_length-2]
    
    #raise    
    
    bp_text = ''
    bp_calc = alt_length

    if in_or_del == 'sub':
        bp_text = "<strong class='%s'>%sbp substitution</strong>" \
        % (in_or_del, bp_calc)
    elif in_or_del == 'insert':
        bp_calc = alt_length - ref_length
        bp_text = "<strong class='%s'>%sbp insert</strong>" \
        % (in_or_del, bp_calc)
    else:
        bp_calc = ref_length - alt_length
        bp_text = "<strong class='%s'>%sbp deletion</strong>" \
        % (in_or_del, bp_calc)

    ref_html = '<strong>REF: </strong>' + prefix + \
        '<strong class="' + in_or_del + '">' + \
        ref_seq.ljust(alt_length, '-') + '</strong>' + suffix
    
    alt_html = '<strong>ALT: </strong>' + prefix \
        + '<strong class="' + in_or_del + '">' + \
        alt_seq.ljust(ref_length, '-') + '</strong>' + suffix
    
    return '<pre>%s<br/>%s<br/>%s</pre>' % (bp_text, ref_html, alt_html)

        
import sys, re, os, argparse
import gzip

def crispr_report_sample_list(vcfFiles):
    sample_list=list()
    
    vcfs = os.listdir(vcfFiles)
    
    for item in sorted(vcfs, key=natural_keys):
        if item.endswith(".vcf.gz") or item.endswith('.vcf'):
            sample_list.append(item)
            
    return sample_list


def crispr_report_sample_info(vcfFiles, bamFiles, vcf, threshold = 1000,
                              quality_lim = 60000):
    
    change_list = dict()
    
    # lazy refactor :)
    item = vcf
    
    gziped = item.split('.')[-1]
    gzipped_vcf = False

    if gziped == 'gz':
        vcfFile = gzip.open(os.path.join(vcfFiles, item), 'rb')
        gzipped_vcf = True
    else: 
        vcfFile = open(os.path.join(vcfFiles, item))
        gzipped_vcf = False

    #bamFile = open(os.path.join(bamFiles, item.split("_")[0]+"_sorted.bam"))
    bamFile = item.split(".")[0]
    bamFile = bamFile.split("_")[0]+"_sorted.bam"

    full_bam_path = os.path.join(bamFiles, bamFile)
    sub_sample_bam(full_bam_path)
    sub_index_bam(sub_bam_filename(full_bam_path))

    tmpName = item.split(".")[0]
    name = 'Sample-%s' % tmpName
    counter=0
    check=''
    change_list=list() 

    for i in vcfFile:
        items = i.strip().split()

        if not i.startswith("#"):
            m = re.search("(DP=)([0-9]+)", items[7])
            af = re.search("(AF=)([0-9]*\.[0-9]+|[0-9]+)",
                           items[7]).group(2)
            ab = re.search("(AB=)([0-9]*\.[0-9]+|[0-9]+)",
                           items[7]).group(2)            
            depth = int(m.group(2))
            chrom = items[0]
            position = int(items[1])
            upstream = position-200
            downstream = position+200
            locus = "%s:%s-%s" % (chrom, upstream, downstream)
            #igvLink = igvTemplate % (bamFile, bamFile, locus)

            #if position == 77242386:
            #    raise

            # LOGIC HERE
            #print depth
            quality = items[5]
            if m and depth > threshold and float(quality) > quality_lim:

                tmp_changedict = dict()
                tmp_changedict['name'] = name
                tmp_changedict['vcf'] = item
                tmp_changedict['chrom'] = chrom
                tmp_changedict['locus'] = locus
                tmp_changedict['bam'] = bamFile
                tmp_changedict['bam_sub'] = sub_bam_filename(bamFile)
                tmp_changedict['position'] = position
                tmp_changedict['reference'] = items[3]
                tmp_changedict['alternative'] = items[4]
                tmp_changedict['quality'] = items[5]
                tmp_changedict['depth'] = depth
                tmp_changedict['allele_frequency'] = \
                    "{0:.0f}%".format(float(af) * 100) # as %
                tmp_changedict['alt_read_ratio'] = \
                    "{0:.0f}%".format(float(ab) * 100) # as %                    
                tmp_changedict['indel_html'] = \
                    render_indel_html('chr' + chrom, position, items[3], items[4])

                #print tmp_changedict

                change_list.append(tmp_changedict)
    
    return change_list

#vcfFiles = '/home/kirill/projects/MichelleMeilak/firstRun-pilotGenotype/freebiTestRun'
#bamFiles = '/home/kirill/projects/MichelleMeilak/firstRun-pilotGenotype/bams-arch'

#print crispr_report_sample_list(vcfFiles)
#print crispr_report_sample_info(vcfFiles, bamFiles, '22_freebayes.vcf')