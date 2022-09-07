import neo4j from 'neo4j-driver'
import recordLogger from './logger.js'

let driver

export const initDriver = async (uri, username, password) => {
  const authToken = neo4j.auth.basic(username, password)

  driver = neo4j.driver(
    uri,
    authToken,
    { logging: { level: 'info', logger: (level, msg) => recordLogger(level, msg)} }
  )
  
  await driver.verifyConnectivity()
  
  return driver
}

export const getDriver = () => {
  return driver
}