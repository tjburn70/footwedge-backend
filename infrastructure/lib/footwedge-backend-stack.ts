import { Stack, Construct } from '@aws-cdk/core'
import { generateFootwedgeApi, generateSearchServiceApi } from './resources/api'
import {
  generateCognitoUserPool,
  addDomain,
  generateScope,
  addResourceServer,
  addWebClient,
  addStreamServiceClient,
  addScrapeServiceClient,
} from './resources/cognito'
import { generateTable } from './resources/dynamo'
import {
  generateFootwedgeApiLambda,
  generateSearchServiceLambda,
  generatePostConfirmationLambda,
  generateStreamServiceLambda,
  generateScrapeGolfClubsLambda,
  generateUploadGolfClubsLambda,
} from './resources/lambda'
import { getFootwedgeHostedZone } from './resources/route53'
import { generateGolfClubQueue, generateDynamoStreamsDeadLetterQueue } from './resources/sqs'
import { generateNewGolfClubTopic } from './resources/sns'
import { generateGolfClubSourceBucket } from './resources/s3'

export interface FootwedgeBackendStackProps {
  readonly env: string
  readonly service: string
  readonly region: string
  readonly account: string
  readonly algoliaAppId: string
  readonly algoliaApiKey: string
  readonly streamServiceCognitoClientSecret: string
  readonly scrapeServiceCognitoClientSecret: string
}

export class FootwedgeBackendStack extends Stack {
  constructor(scope: Construct, id: string, props: FootwedgeBackendStackProps) {
    super(scope, id, {
      stackName: `${props.env}-${props.service}`,
      env: {
        region: props.region,
        account: props.account,
      },
    })
    const footwedgeApiDomainName = `${props.env}-api.footwedge.io`
    const postConfirmationLambda = generatePostConfirmationLambda(
      this,
      props.env,
      props.service,
      footwedgeApiDomainName
    )
    const footwedgeUserPool = generateCognitoUserPool(
      this,
      props.env,
      postConfirmationLambda
    )
    const footwedgeCognitoDomain = addDomain(footwedgeUserPool, props.env)
    const golfRoundsReadScope = generateScope(
      'golf-rounds.read',
      'Read user golf-rounds'
    )
    const handicapWriteScope = generateScope(
      'handicap.write',
      'Write user handicap'
    )
    const golfClubWriteScope = generateScope(
      'golf-clubs.write',
      'Write golf clubs'
    )
    const footwedgeCognitoResourceServer = addResourceServer(
      footwedgeUserPool,
      golfRoundsReadScope,
      handicapWriteScope,
      golfClubWriteScope
    )
    const footwedgeWebClient = addWebClient(footwedgeUserPool)
    const streamServiceClient = addStreamServiceClient(
      footwedgeUserPool,
      footwedgeCognitoResourceServer,
      golfRoundsReadScope,
      handicapWriteScope
    )
    const scrapeServiceClient = addScrapeServiceClient(
      footwedgeUserPool,
      footwedgeCognitoResourceServer,
      golfClubWriteScope
    )

    const footwedgeTableName = `${props.env}-${props.service}-table`
    const dynamoDbUrl = `https://dynamodb.${props.region}.amazonaws.com`
    const footwedgeApiLambda = generateFootwedgeApiLambda(this, {
      envName: props.env,
      serviceName: props.service,
      cognitoRegion: props.region,
      cognitoUserPoolId: footwedgeUserPool.userPoolId,
      cognitoWebClientId: footwedgeWebClient.userPoolClientId,
      dynamoDbUrl: dynamoDbUrl,
      footwedgeDynamoTableName: footwedgeTableName,
    })
    const footwedgeHostedZone = getFootwedgeHostedZone(this)
    generateFootwedgeApi(
      this,
      footwedgeApiLambda,
      footwedgeApiDomainName,
      footwedgeHostedZone
    )

    const searchServiceLambda = generateSearchServiceLambda(
      this,
      props.env,
      props.service,
      props.algoliaAppId,
      props.algoliaApiKey
    )
    const searchServiceDomainName = `${props.env}-search.footwedge.io`
    generateSearchServiceApi(
      this,
      searchServiceLambda,
      searchServiceDomainName,
      footwedgeHostedZone
    )

    const footwedgeTable = generateTable(
      this,
      footwedgeTableName,
      footwedgeApiLambda
    )

    const streamServiceLambda = generateStreamServiceLambda(this, {
      envName: props.env,
      serviceName: props.service,
      cognitoRegion: props.region,
      cognitoDomain: footwedgeCognitoDomain.domainName,
      streamServiceCognitoClientId: streamServiceClient.userPoolClientId,
      streamServiceCognitoClientSecret: props.streamServiceCognitoClientSecret,
      footwedgeTable: footwedgeTable,
      footwedgeApiDomainName: footwedgeApiDomainName,
      searchServiceDomainName: searchServiceDomainName,
      deadLetterQueue: generateDynamoStreamsDeadLetterQueue(this)
    })

    footwedgeTable.grantStreamRead(streamServiceLambda)

    const golfClubQueue = generateGolfClubQueue(this)
    const golfClubTopic = generateNewGolfClubTopic(this, golfClubQueue)
    const golfClubSourceBucket = generateGolfClubSourceBucket(
      this,
      `${props.env}-footwedge-golf-club-source`,
      golfClubTopic
    )
    generateScrapeGolfClubsLambda(
      this,
      golfClubSourceBucket,
      props.env,
      props.service
    )
    generateUploadGolfClubsLambda(this, {
      envName: props.env,
      serviceName: props.service,
      golfClubQueue: golfClubQueue,
      golfClubSourceBucket: golfClubSourceBucket,
      scrapeServiceCognitoClientId: scrapeServiceClient.userPoolClientId,
      scrapeServiceCognitoClientSecret: props.scrapeServiceCognitoClientSecret,
      footwedgeApiDomainName: footwedgeApiDomainName,
      cognitoDomain: footwedgeCognitoDomain.domainName,
    })
  }
}
