# Overview

Example for visual inspection.

# Testing

To test evaluation of an image, wwe can use http-Trigger and name a special blob.

Local Debugging: [http://localhost:7071/api/HttpTrigger1?blob=cast_def_0_9966.jpeg](http://localhost:7071/api/HttpTrigger1?blob=cast_def_0_9966.jpeg)


# Setup

python3.11

install requirements

 Make sure ODBC driver is installe dlocally: [https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16)

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

# Logging
## Application Insights

```KQL
traces
| where timestamp > ago(1d) // Adjust the timeframe as needed
| where severityLevel >= 3  // Filter for errors and critical issues
| order by timestamp desc   // Orders the output by time, most recent first
| project timestamp, message, severityLevel, operation_Id // Customize the output columns
```

Logs
![alt text](readme/appIns.png)

If fail with
```(Failed, Id=eefc8b9b-e29f-437a-adbc-1ca2eca864bb, Duration=23ms)```
then use
```KQL
traces
| where customDimensions.InvocationId == "eefc8b9b-e29f-437a-adbc-1ca2eca864bb"
```
or for exceptions:
```KQL
exceptions
| where customDimensions.InvocationId == "777e93a7-f96a-47dd-b347-1ab5ac40d800"
```

Also possible to live monitor if right click in vscode on teh fucntion app. Will open new browser tab.

Search where logs contain:
```KQL
traces
| where message contains "download_file_from_blob"
| project timestamp, message, severityLevel, operation_Id
| order by timestamp desc
```