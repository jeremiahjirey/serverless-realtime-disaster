CREATE TABLE source (
  event_id STRING,
  location STRING,
  magnitude DOUBLE,
  timestamp BIGINT,
  type STRING
) WITH (
  'connector' = 'kinesis',
  'stream' = 'disaster-stream',
  'aws.region' = 'us-east-1',
  'format' = 'json'
);

CREATE TABLE sink (
  event_id STRING,
  location STRING,
  magnitude DOUBLE,
  timestamp BIGINT,
  type STRING,
  PRIMARY KEY (event_id) NOT ENFORCED
) WITH (
  'connector' = 'dynamodb',
  'table-name' = 'disasters',
  'aws.region' = 'us-east-1'
);

INSERT INTO sink SELECT * FROM source;
