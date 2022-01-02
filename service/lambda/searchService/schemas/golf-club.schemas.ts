import Joi from 'types-joi'

import { golfCourseSchema } from './golf-course.schemas'

const golfClubSchema = Joi.object({
  golf_club_id: Joi.string().required(),
  golf_club_name: Joi.string().required(),
  golf_courses: Joi.array().items(golfCourseSchema),
  created_ts: Joi.date(),
  touched_ts: Joi.date().allow(null),
})

export { golfClubSchema }
