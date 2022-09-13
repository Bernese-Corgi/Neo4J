import winston from "winston";


const recordLogger = (level, message) => {
  const cur = new Date()
  const time = `${cur.getMonth() + 1}월 ${cur.getDate()}일 ${cur.getHours()}시 ${cur.getMinutes()}분 ${cur.getSeconds()}초`

  const logger = winston.createLogger({
    level,
    format: winston.format.simple(),
    transports: [
      new winston.transports.File({ filename: 'error.log', level: 'error' }),
      new winston.transports.File({ filename: 'combined.log' })
    ],
  })

  logger.log(level, `${time} | ${message}`)
}

export default recordLogger;