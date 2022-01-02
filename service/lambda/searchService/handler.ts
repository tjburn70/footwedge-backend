import serverlessExpress from '@vendia/serverless-express'
import { Context, Handler } from 'aws-lambda'

import { app } from './app'

let cachedServer: Handler

async function bootstrap() {
  if (!cachedServer) {
    cachedServer = serverlessExpress({ app })
  }

  return cachedServer
}

export const handler = async (event: any, context: Context, callback: any) => {
  const server = await bootstrap()
  return server(event, context, callback)
}
