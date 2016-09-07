from flask import Flask, abort, redirect, url_for, \
    render_template

import vcfParse

app = Flask(__name__)

@app.route('/')
def report():

    
    vcfFiles = '/home/kirill/projects/MichelleMeilak/firstRun-pilotGenotype/freebiTestRun'
    bamFiles = '/home/kirill/projects/MichelleMeilak/firstRun-pilotGenotype/bams-arch'

    #print vcfParse.crispr_report_sample_list(vcfFiles)
    name = '22_freebayes.vcf'
    vcf = vcfParse.crispr_report_sample_info(vcfFiles, bamFiles, name)
    
    return render_template('report.html', name=name, vcf=vcf)