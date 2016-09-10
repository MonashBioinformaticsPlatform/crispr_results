# Crispr Results

Crispr Experiment Report Viewer.

[Screenshot](https://dl.dropboxusercontent.com/u/172498/host/crispr_reports_160910.PNG)

## Running

```
# from crispr/ dir
export FLASK_APP=crispr.py
export FLASK_DEBUG=1
flask run
```

Tests:
```
python tests/crispr_tests.py
```

## Dependencies

Python: Flask
Nodejs: Pileup.js (install into `static/js`)
2bit mm10 reference: Run `./getmm10.sh` from `crispr/ref` dir

## Configuration

_Example data has been included that works on app start._

You can insert your own data into the `crispr/data` directory under the following scheme:

```
/MyReportName/
   /bam/
   /vcf/
```

To override this data location with your own location.

Create a directory off the root (crispr_results) one called `instance`, create a `config.py` inside and put `DATA_INDEX_DIRECTORY = '<YOUR PATH HERE>'`.
