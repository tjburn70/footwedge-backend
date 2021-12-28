import { app } from './app'
import { appConfig } from './modules/config'

const port: number = appConfig.port
const host: string = appConfig.host

app.listen(port, host, () => {
  console.log(`Search API listening at http://${host}:${port}`)
})
