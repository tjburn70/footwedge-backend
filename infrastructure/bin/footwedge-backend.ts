import { App } from '@aws-cdk/core'
import { FootwedgeBackendStack } from '../lib/footwedge-backend-stack'

const app = new App()

const ENV = app.node.tryGetContext('ENV_NAME')
const SERVICE = app.node.tryGetContext('SERVICE_NAME')
const REGION = app.node.tryGetContext('REGION')
const ACCOUNT = app.node.tryGetContext('ACCOUNT')
const ALGOLIA_FOOTWEDGE_APP_ID = app.node.tryGetContext(
  'ALGOLIA_FOOTWEDGE_APP_ID'
)
const ALGOLIA_API_KEY = app.node.tryGetContext('ALGOLIA_API_KEY')

new FootwedgeBackendStack(app, `${ENV}-${SERVICE}`, {
  env: ENV,
  service: SERVICE,
  region: REGION,
  account: ACCOUNT,
  algoliaAppId: ALGOLIA_FOOTWEDGE_APP_ID,
  algoliaApiKey: ALGOLIA_API_KEY,
})
