import { Router } from 'express'

import {
  addGolfClubHandler,
  addGolfCourseHandler,
  searchGolfClubHandler,
} from '../controllers/golf-club.controllers'
import { validate } from '../middleware/validate-request'
import { golfClubSchema } from '../schemas/golf-club.schemas'
import { golfCourseSchema } from '../schemas/golf-course.schemas'

const golfClubRouter = Router()

golfClubRouter.post('/golf-club', validate(golfClubSchema), addGolfClubHandler)
golfClubRouter.patch(
  '/golf-club/:golfClubId/golf-course',
  validate(golfCourseSchema),
  addGolfCourseHandler
)
golfClubRouter.get('/golf-club', searchGolfClubHandler)

export { golfClubRouter }
