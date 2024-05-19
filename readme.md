# Overview

Example for visual inspection.

# Setup

python3.11
install requirements

# Files

- **train_model.py**: run whole workbook to train network and save trained model. Might take some time.
- **use_model.py**: Use a pretrained model.
- **in/qualityInsepction.zip**: zip-file of all images.

# Azure functions

Fucntion is triggered when uplaoded to path. Improtant to use local file **local.settings.json** for debugging. Important to use key **AzureWebJobs**connectionVisualInspection and not just connectionVisualInspection.

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "***AccountName=rglobadvccdaib694***",
    "AzureWebJobsconnectionVisualInspection": "***AccountName=visualdetection***",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
    "44c30b_STORAGE": "UseDevelopmentStorage=true"
  }
}
```