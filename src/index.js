import app from "./app.js"
import { APP_PORT } from './constants.js'

const port = APP_PORT

app.listen(port, () => {
  console.log(`Server listening on http://localhost:${port}/`)
})