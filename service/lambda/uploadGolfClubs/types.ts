export type CognitoTokenRespBody = {
  readonly access_token: string
  readonly expires_in: number
  readonly token_type: string
}

export type TeeBox = {
  tee_box_color: string
  gender: string
  par: number
  distance: number | null
  units: string
  course_rating: string
  slope: number
}

export type GolfCourse = {
  golf_course_name: string
  num_holes: number
  tee_boxes: TeeBox[]
}

export type GolfClub = {
  golf_club_name: string
  city: string
  state_code: string
  courses: GolfCourse[]
}
