import { Stack, Construct } from '@aws-cdk/core'
import { generateSearchServiceApi } from './resources/api'
import { 
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
