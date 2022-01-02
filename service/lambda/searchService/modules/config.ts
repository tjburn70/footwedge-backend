// import dotenv from 'dotenv';

import { AppConfig } from '../types/app-config'

// dotenv.config();

type ConfigKeys = keyof AppConfig

const getConfig = (): AppConfig => {
  const config = {
    host: process.env.FOOTWEDGE_SEARCH_API_HOST ?? 'localhost',
    port: parseInt(process.env.FOOTWEDGE_SEARCH_API_PORT ?? '8080'),
    environment: process.env.ENV ?? 'development',
    algoliaAppId: process.env.ALGOLIA_FOOTWEDGE_APP_ID ?? '',
    algoliaApiKey: process.env.ALGOLIA_API_KEY ?? '',
  }

  const requiredKeys: ConfigKeys[] = ['algoliaAppId', 'algoliaApiKey']
  requiredKeys.forEach((requiredKey) => {
    if (config[requiredKey] === '') {
      throw new Error(`The key: ${requiredKey} is not set, check environment`)
    }
  })

  return config
}

export const appConfig = getConfig()
