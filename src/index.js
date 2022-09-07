import app from "./app.js"
import { APP_PORT } from './constant.js'

const port = APP_PORT

app.listen(port, () => {
  console.log(`Server listening on http://localhost:${port}/`)
})