import { Stack, Construct } from '@aws-cdk/core'
import {
  generateFootwedgeApi,
  generateSearchServiceApi,
} from './resources/api'
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
    const footwedgeTableName = `${props.env}-${props.service}-table`
    const dynamoDbUrl = `https://dynamodb.${props.region}.amazonaws.com`
    const footwedgeApiLambda = generateFootwedgeApiLambda(
      this,
      {
        envName: props.env,
        serviceName: props.service,
        cognitoRegion: props.region,
        cognitoUserPoolId: '',
        cognitoWebClientId: '',
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
    generatePostConfirmationLambda(
      this,
      props.env,
      props.service,
    )
  }
}
