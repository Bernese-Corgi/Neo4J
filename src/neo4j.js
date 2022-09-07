import neo4j from 'neo4j-driver'

let driver

export const initDriver = (uri, username, password) => {
  const authToken = neo4j.auth.basic(username, password)

  driver = neo4j.driver(
    uri,
    authToken,
    { logging: { level: 'info', logger: (level, msg) => console.log(`${level} | ${msg}`) } }
  )
  
  return driver.verifyConnectivity().then(() => driver)
}

export const getDriver = () => {
  return driver
}