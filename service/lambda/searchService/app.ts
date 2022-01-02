import cors from 'cors'
import type { CorsOptions } from 'cors'
import express from 'express'
import type { Application } from 'express'

import { golfClubRouter } from './routes/golf-club.routes'

const app: Application = express()

const allowedOrigins = ['http://localhost:3000', 'https://www.footwedge.io']
const options: CorsOptions = {
  origin: allowedOrigins,
}

app.use(cors(options))
app.use(express.json())
app.use(golfClubRouter)

export { app }
