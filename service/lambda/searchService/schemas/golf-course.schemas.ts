import Joi from 'types-joi'

const golfCourseSchema = Joi.object({
  golf_course_id: Joi.string().required(),
  golf_course_name: Joi.string().required(),
  num_holes: Joi.number().required(),
})

export { golfCourseSchema }
