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

# Configuration

_Example data has been included that works on app start._

This app has been designed to work with a directory of files. These files are text file indexes pointing to vcf/bam locations (ie. individual reports).

eg. For the example data in this repo `crispr/data-index-example` contains one 'report' ExampleData. That file contains the VCF file location on one line, and the BAM on the next. Create further files in this directory pointing to more reports, with your own data in their own locations

To override this index location with your own index location containing files that point to your own data:

Create a directory off the root (crispr_results) one called `instance`, create a `config.py` inside and put `DATA_INDEX_DIRECTORY = '<YOUR PATH HERE>'`. Then fill that directory with text files pointing to vcf, bam files much like `crispr/data-index-example` and the `ExampleData` file.

