import { Stack, Construct } from '@aws-cdk/core'
import {
  generateFootwedgeApi,
  generateSearchServiceApi,
} from './resources/api'
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
} from './resources/lambda'

export interface FootwedgeBackendStackProps {
  readonly env: string
  readonly service: string
  readonly region: string
  readonly account: string
  readonly algoliaAppId: string
  readonly algoliaApiKey: string
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
    const postConfirmationLambda = generatePostConfirmationLambda(
      this,
      props.env,
      props.service,
    )
    const footwedgeUserPool = generateCognitoUserPool(
      this,
      props.env,
      postConfirmationLambda,
    )
    const footwedgeCognitoDomain = addDomain(footwedgeUserPool, props.env)
    const golfRoundsReadScope = generateScope('golf-rounds.read', 'Read user golf-rounds')
    const handicapWriteScope = generateScope('handicap.write', 'Write user handicap')
    const golfClubWriteScope = generateScope('golf-clubs.write', 'Write golf clubs')
    const footwedgeCognitoResourceServer = addResourceServer(
      footwedgeUserPool,
      golfRoundsReadScope,
      handicapWriteScope,
      golfClubWriteScope,
    )
    const footwedgeWebClient = addWebClient(footwedgeUserPool)
    const streamServiceClient = addStreamServiceClient(
      footwedgeUserPool,
      footwedgeCognitoResourceServer,
      golfRoundsReadScope,
      handicapWriteScope,
    )
    const searchServiceClient = addScrapeServiceClient(
      footwedgeUserPool,
      footwedgeCognitoResourceServer,
      golfClubWriteScope,
    )

    const footwedgeTableName = `${props.env}-${props.service}-table`
    const dynamoDbUrl = `https://dynamodb.${props.region}.amazonaws.com`
    const footwedgeApiLambda = generateFootwedgeApiLambda(
      this,
      {
        envName: props.env,
        serviceName: props.service,
        cognitoRegion: props.region,
        cognitoUserPoolId: footwedgeUserPool.userPoolId,
        cognitoWebClientId: footwedgeWebClient.userPoolClientId,
        dynamoDbUrl: dynamoDbUrl,
        footwedgeDynamoTableName: footwedgeTableName,
      }
    )
    generateFootwedgeApi(this, footwedgeApiLambda)
    
    generateTable(
      this,
      footwedgeTableName,
      footwedgeApiLambda,
    )

    const searchServiceLambda = generateSearchServiceLambda(
      this,
      props.env,
      props.service,
      props.algoliaAppId,
      props.algoliaApiKey
    )
    generateSearchServiceApi(this, searchServiceLambda)
  }
}
