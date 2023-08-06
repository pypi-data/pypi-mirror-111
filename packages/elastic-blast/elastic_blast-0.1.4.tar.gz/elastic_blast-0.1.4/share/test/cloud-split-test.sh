#!/bin/bash -e
# Bash script for EB-974
RESULTS_BUCKET=${1:-"s3://elasticblast-test"}

ELB_NO_SEARCH=1 ELB_USE_1_STAGE_CLOUD_SPLIT=1 elastic-blast.py submit --cfg share/etc/elb-aws-split-only-local-ssd-mane.ini --results $RESULTS_BUCKET/cloud_split/split-only-local-ssd-mane
elastic-blast.py status --wait --cfg share/etc/elb-aws-split-only-local-ssd-mane.ini --results $RESULTS_BUCKET/cloud_split/split-only-local-ssd-mane
elastic-blast.py run-summary --cfg share/etc/elb-aws-split-only-local-ssd-mane.ini --results $RESULTS_BUCKET/cloud_split/split-only-local-ssd-mane > split-only-local-ssd-mane-summary.json
elastic-blast.py delete --cfg share/etc/elb-aws-split-only-local-ssd-mane.ini --results $RESULTS_BUCKET/cloud_split/split-only-local-ssd-mane

ELB_NO_SEARCH=1 ELB_USE_1_STAGE_CLOUD_SPLIT=1 elastic-blast.py submit --cfg share/etc/elb-aws-split-only-local-ssd-vht2.ini --results $RESULTS_BUCKET/cloud_split/split-only-local-ssd-vht2
elastic-blast.py status --wait --cfg share/etc/elb-aws-split-only-local-ssd-vht2.ini --results $RESULTS_BUCKET/cloud_split/split-only-local-ssd-vht2
elastic-blast.py run-summary --cfg share/etc/elb-aws-split-only-local-ssd-vht2.ini --results $RESULTS_BUCKET/cloud_split/split-only-local-ssd-vht2 > split-only-local-ssd-vht2-summary.json
elastic-blast.py delete --cfg share/etc/elb-aws-split-only-local-ssd-vht2.ini --results $RESULTS_BUCKET/cloud_split/split-only-local-ssd-vht2

ELB_NO_SEARCH=1 ELB_USE_1_STAGE_CLOUD_SPLIT=1 elastic-blast.py submit --cfg share/etc/elb-aws-split-only-local-ssd-viralmeta.ini --results $RESULTS_BUCKET/cloud_split/split-only-local-ssd-viralmeta
elastic-blast.py status --wait --cfg share/etc/elb-aws-split-only-local-ssd-viralmeta.ini --results $RESULTS_BUCKET/cloud_split/split-only-local-ssd-viralmeta
elastic-blast.py run-summary --cfg share/etc/elb-aws-split-only-local-ssd-viralmeta.ini --results $RESULTS_BUCKET/cloud_split/split-only-local-ssd-viralmeta > split-only-local-ssd-viralmeta-summary.json
elastic-blast.py delete --cfg share/etc/elb-aws-split-only-local-ssd-viralmeta.ini --results $RESULTS_BUCKET/cloud_split/split-only-local-ssd-viralmeta
