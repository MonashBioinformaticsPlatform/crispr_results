from flask import Flask, abort, redirect, url_for, \
    render_template, send_from_directory

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


def get_data_dirs():
    return [name for name in os.listdir(get_data_index_dir())
            if os.path.isdir(os.path.join(get_data_index_dir(), name))]


def get_reports_from_data_dir(index_dir):

    datadir = os.path.join(get_data_index_dir(), index_dir)
    datadirs = dict()
    
    datadirs['vcf'] = os.path.join(datadir,'vcf')
    datadirs['bam'] = os.path.join(datadir,'bam')
    return datadirs


@app.route('/data/<path:path>')
def send_data(path):
    return send_from_directory('data', path)


# TODO get data index
@app.route('/')
def index():

    return render_template('index.html', reports=get_data_dirs(),
                           data_dir=get_data_index_dir())


# TODO make sample index and GET
@app.route('/report/<report_name>')
def report(report_name):

    name = report_name
    
    datadirs = get_reports_from_data_dir(name)
    vcf = vcfParse.crispr_report_sample_list(datadirs['vcf'])
    
    ## remove.. testing get info for all samples in report

    #for v in vcf:
    #    vcfParse.crispr_report_sample_info(datadirs['vcf'],
    #                                         datadirs['bam'], v, threshold=1000)
    ## remove above    
    
    return render_template('report.html', report_name=name, samples=vcf)


# TODO make data index
@app.route('/report/<report_name>/<sample_name>')
def sample(report_name, sample_name):
    
    boundary = app.config['SEQ_DISPLAY_BOUNDARY']
    
    datadirs = get_reports_from_data_dir(report_name)
   
    #vcfFiles = '/home/kirill/projects/MichelleMeilak/firstRun-pilotGenotype/freebiTestRun'
    #bamFiles = '/home/kirill/projects/MichelleMeilak/firstRun-pilotGenotype/bams-arch'
    
    vcf = vcfParse.crispr_report_sample_info(datadirs['vcf'],
                                             datadirs['bam'], sample_name, threshold=1000,
                                             quality_lim=60000)
    
    #full os path.. bam_dir=datadirs['bam']
    
    return render_template('sample.html', sample_name=sample_name, report_name=report_name,
                           vcf=vcf, boundary=boundary,
                           pileup_js_enabled=app.config['PILEUP_JS_ENABLED'])


# TODO get data index
@app.route('/pileup')
def pileup():
    
    return render_template('pileup.html')