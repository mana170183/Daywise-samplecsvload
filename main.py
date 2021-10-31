import os
from google.cloud import bigquery

def daywise_csv_loader(data, context):
        client = bigquery.Client()
        dataset_id = os.environ['DATASET']
        dataset_ref = client.dataset(dataset_id)
        job_config = bigquery.LoadJobConfig()
        job_config.schema = [
                bigquery.SchemaField('Day', 'DATE'),
                bigquery.SchemaField('Country_Name', 'STRING'),
                bigquery.SchemaField('Operator_Name', 'STRING'),
                bigquery.SchemaField('Attempts', 'INTEGER'),
                bigquery.SchemaField('Answered', 'INTEGER'),
                bigquery.SchemaField('A_Release', 'STRING'),
				bigquery.SchemaField('NER', 'STRING'),
				bigquery.SchemaField('ASR', 'STRING'),
				bigquery.SchemaField('ConVTime_Min', 'INTEGER'),
				bigquery.SchemaField('ACT_Sec', 'INTEGER'),
				bigquery.SchemaField('CST_Sec', 'INTEGER')
                ]
        job_config.skip_leading_rows = 1
        job_config.source_format = bigquery.SourceFormat.CSV

        # get the URI for uploaded CSV in GCS from 'data'
        uri = 'gs://' + os.environ['BUCKET'] + '/' + data['name']

        # lets do this
        load_job = client.load_table_from_uri(
                uri,
                dataset_ref.table(os.environ['TABLE']),
                job_config=job_config)

        print('Starting job {}'.format(load_job.job_id))
        print('Function=daywise_csv_loader, Version=' + os.environ['VERSION'])
        print('File: {}'.format(data['name']))

        load_job.result()  # wait for table load to complete.
        print('Job finished.')

        destination_table = client.get_table(dataset_ref.table(os.environ['TABLE']))
        print('Loaded {} rows.'.format(destination_table.num_rows))