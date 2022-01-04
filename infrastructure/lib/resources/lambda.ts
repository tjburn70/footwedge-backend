import * as cdk from '@aws-cdk/core'
import * as lambda from '@aws-cdk/aws-lambda'
import * as dynamo from '@aws-cdk/aws-dynamodb'
import {
  DynamoEventSource,
  SqsEventSource,
} from '@aws-cdk/aws-lambda-event-sources'
import { Bucket } from '@aws-cdk/aws-s3'
import { Queue } from '@aws-cdk/aws-sqs'
import * as path from 'path'

export interface FootwedgeApiProps {
  envName: string
  serviceName: string
  cognitoRegion: string
  cognitoUserPoolId: string
  cognitoWebClientId: string
  dynamoDbUrl: string
  footwedgeDynamoTableName: string
}

export function generateFootwedgeApiLambda(
  scope: cdk.Construct,
  props: FootwedgeApiProps
): lambda.Function {
  const id = 'footwedge-api'
  return new lambda.Function(scope, id, {
    runtime: lambda.Runtime.PYTHON_3_7,
    code: lambda.Code.fromAsset(path.join(__dirname, `../../../${id}/target`)),
    handler: 'handler.lambda_handler',
    functionName: `${props.envName}-${props.serviceName}-${id}`,
    memorySize: 512,
    timeout: cdk.Duration.minutes(5),
    environment: {
      ENV_NAME: props.envName,
      PYTHONPATH: 'src',
      COGNITO_REGION: props.cognitoRegion,
      COGNITO_USER_POOL_ID: props.cognitoUserPoolId,
      COGNITO_WEB_CLIENT_ID: props.cognitoWebClientId,
      DYNAMO_DB_URL: props.dynamoDbUrl,
      FOOTWEDGE_DYNAMO_TABLE: props.footwedgeDynamoTableName,
    },
  })
}

export function generateSearchServiceLambda(
  scope: cdk.Construct,
  envName: string,
  serviceName: string,
  algoliaAppId: string,
  algoliaApiKey: string
): lambda.Function {
  const id = 'searchService'
  const searchServiceLambda = new lambda.Function(scope, id, {
    runtime: lambda.Runtime.NODEJS_14_X,
    code: lambda.Code.fromAsset(path.join(__dirname, `../../../dist/${id}`)),
    handler: 'index.lambdaHandler',
    functionName: `${envName}-${serviceName}-${id}`,
    memorySize: 512,
    timeout: cdk.Duration.minutes(5),
    environment: {
      ENV_NAME: envName,
      ALGOLIA_FOOTWEDGE_APP_ID: algoliaAppId,
      ALGOLIA_API_KEY: algoliaApiKey,
    },
  })

  return searchServiceLambda
}

export function generatePostConfirmationLambda(
  scope: cdk.Construct,
  envName: string,
  serviceName: string,
  footwedgeApiDomainName: string
): lambda.Function {
  const id = 'post-confirmation-service'
  const footwedgeApiUrl = `https://${footwedgeApiDomainName}/v1`
  return new lambda.Function(scope, id, {
    runtime: lambda.Runtime.PYTHON_3_7,
    code: lambda.Code.fromAsset(path.join(__dirname, `../../../${id}/target`)),
    handler: 'handler.lambda_handler',
    functionName: `${envName}-${serviceName}-${id}`,
    memorySize: 512,
    timeout: cdk.Duration.minutes(2),
    environment: {
      FOOTWEDGE_API_URL: footwedgeApiUrl,
      ENV_NAME: envName,
    },
  })
}

export interface StreamServiceProps {
  envName: string
  serviceName: string
  cognitoDomain: string
  cognitoRegion: string
  streamServiceCognitoClientId: string
  streamServiceCognitoClientSecret: string
  footwedgeTable: dynamo.Table
  footwedgeApiDomainName: string
  searchServiceDomainName: string
}

export function generateStreamServiceLambda(
  scope: cdk.Construct,
  props: StreamServiceProps
): lambda.Function {
  const id = 'stream-service'
  const footwedgeApiUrl = `https://${props.footwedgeApiDomainName}/v1`
  const searchServiceApiUrl = `https://${props.searchServiceDomainName}`
  const fn = new lambda.Function(scope, id, {
    runtime: lambda.Runtime.PYTHON_3_7,
    code: lambda.Code.fromAsset(path.join(__dirname, `../../../${id}/target`)),
    handler: 'handler.lambda_handler',
    functionName: `${props.envName}-${props.serviceName}-${id}`,
    memorySize: 512,
    timeout: cdk.Duration.minutes(2),
    environment: {
      ENV_NAME: props.envName,
      COGNITO_DOMAIN: props.cognitoDomain,
      COGNITO_REGION: props.cognitoRegion,
      STREAM_SERVICE_COGNITO_CLIENT_ID: props.streamServiceCognitoClientId,
      STREAM_SERVICE_COGNITO_CLIENT_SECRET:
        props.streamServiceCognitoClientSecret,
      FOOTWEDGE_API_URL: footwedgeApiUrl,
      FOOTWEDGE_SEARCH_URL: searchServiceApiUrl,
    },
  })
  fn.addEventSource(
    new DynamoEventSource(props.footwedgeTable, {
      startingPosition: lambda.StartingPosition.TRIM_HORIZON,
      batchSize: 5,
      bisectBatchOnError: true,
      // onFailure: new SqsDlq(deadLetterQueue),
      retryAttempts: 5,
    })
  )
  return fn
}

export function generateScrapeGolfClubsLambda(
  scope: cdk.Construct,
  footwedgeGolfClubSourceBucket: Bucket,
  envName: string,
  serviceName: string
): lambda.Function {
  const id = 'scrape-golf-clubs'
  const scrapeGolfClubsLambda = new lambda.Function(scope, id, {
    runtime: lambda.Runtime.PYTHON_3_6,
    code: lambda.Code.fromAsset(path.join(__dirname, `../../../${id}/target`)),
    handler: 'app.lambda_handler',
    functionName: `${envName}-${serviceName}-${id}`,
    memorySize: 512,
    timeout: cdk.Duration.minutes(10),
    environment: {
      FOOTWEDGE_GOLF_CLUB_SOURCE_BUCKET_NAME:
        footwedgeGolfClubSourceBucket.bucketName,
      ENV_NAME: envName,
    },
  })

  footwedgeGolfClubSourceBucket.grantPut(scrapeGolfClubsLambda)
  footwedgeGolfClubSourceBucket.grantWrite(scrapeGolfClubsLambda)

  return scrapeGolfClubsLambda
}

export interface UploadGolfClubProps {
  envName: string
  serviceName: string
  golfClubQueue: Queue
  golfClubSourceBucket: Bucket
  scrapeServiceCognitoClientId: string
  scrapeServiceCognitoClientSecret: string
  footwedgeApiDomainName: string
  cognitoDomain: string
}

export function generateUploadGolfClubsLambda(
  scope: cdk.Construct,
  props: UploadGolfClubProps
): lambda.Function {
  const id = 'uploadGolfClubs'
  const footwedgeApiUrl = `https://${props.footwedgeApiDomainName}/v1`
  const uploadGolfClubLambda = new lambda.Function(scope, id, {
    runtime: lambda.Runtime.NODEJS_14_X,
    code: lambda.Code.fromAsset(path.join(__dirname, `../../../dist/${id}`)),
    handler: 'index.lambdaHandler',
    functionName: `${props.envName}-${props.serviceName}-${id}`,
    memorySize: 512,
    timeout: cdk.Duration.minutes(5),
    environment: {
      ENV_NAME: props.envName,
      SCRAPE_SERVICE_COGNITO_CLIENT_ID: props.scrapeServiceCognitoClientId,
      SCRAPE_SERVICE_COGNITO_CLIENT_SECRET:
        props.scrapeServiceCognitoClientSecret,
      FOOTWEDGE_API_URL: footwedgeApiUrl,
      COGNITO_DOMAIN: props.cognitoDomain,
    },
  })

  uploadGolfClubLambda.addEventSource(
    new SqsEventSource(props.golfClubQueue, {
      batchSize: 10,
      maxBatchingWindow: cdk.Duration.minutes(2),
    })
  )

  props.golfClubSourceBucket.grantRead(uploadGolfClubLambda)

  return uploadGolfClubLambda
}
