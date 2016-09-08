from flask import Flask, abort, redirect, url_for, \
    render_template

import os
import vcfParse

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('crispr.config')
app.config.from_pyfile('config.py', silent=True)

def get_data_index_dir():
    dir_from_cfg = app.config['DATA_INDEX_DIRECTORY']
    
    data_index_dir = ''
    if not dir_from_cfg.startswith(os.path.sep):
        #relative
        data_index_dir = os.path.join(app.root_path, dir_from_cfg)
    else:
        data_index_dir = dir_from_cfg    

    return data_index_dir


def get_data_index_files():
    return os.listdir(get_data_index_dir())    


def get_reports_from_data_index_file(index_file):
    
    vcf = ''
    bam = ''
    datadirs = dict()
        
    with open(os.path.join(get_data_index_dir(),index_file), 'r') as f:
        for line in f.readlines():
            if len(line.strip()) == 0:
                continue
            
            if not vcf:
                if line.strip().startswith(os.path.sep):
                    vcf = line.strip()
                else:
                    vcf = os.path.join(app.root_path, line.strip())
                
            if not bam:
                if line.strip().startswith(os.path.sep):
                    bam = line.strip()
                else:
                    bam = os.path.join(app.root_path, line.strip())
    
    datadirs['vcf'] = vcf
    datadirs['bam'] = bam
    return datadirs


# TODO get data index
@app.route('/')
def index():
    
    return render_template('index.html', reports=get_data_index_files())


# TODO make sample index and GET
@app.route('/report/<report_name>')
def report(report_name):

    name = report_name
    
    datadirs = get_reports_from_data_index_file(name)
    vcf = vcfParse.crispr_report_sample_list(datadirs['vcf'])
    
    return render_template('report.html', name=name, samples=vcf)


# TODO make data index
@app.route('/report/<report_name>/<sample_name>')
def sample(report_name, sample_name):
    
    datadirs = get_reports_from_data_index_file(report_name)
   
    #vcfFiles = '/home/kirill/projects/MichelleMeilak/firstRun-pilotGenotype/freebiTestRun'
    #bamFiles = '/home/kirill/projects/MichelleMeilak/firstRun-pilotGenotype/bams-arch'
    
    vcf = vcfParse.crispr_report_sample_info(datadirs['vcf'], datadirs['bam'], sample_name, threshold=1000)
    
    print sample_name
    
    return render_template('sample.html', name=vcf[0]['name'], vcf=vcf)