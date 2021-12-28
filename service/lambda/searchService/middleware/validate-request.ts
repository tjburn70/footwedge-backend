import type { Request, Response, NextFunction } from 'express'
import type { ObjectSchema } from 'types-joi'

/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable indent */
const validate =
  (schema: ObjectSchema<any>) =>
  (request: Request, response: Response, next: NextFunction) => {
    const result = schema.validate(request.body, { abortEarly: false })
    if (result.error) {
      return response.status(400).send(result.error.details)
    }
    return next()
  }

export { validate }
