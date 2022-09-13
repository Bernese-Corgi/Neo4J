// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'
import { Neo4jGraphQL } from '@neo4j/graphql'
import neo4j from 'neo4j-driver'
import { ApolloServer, gql } from 'apollo-server-micro'

type Data = {
  name: string
}

const driver = neo4j.driver(
  process.env.NEO4J_URI,
  neo4j.auth.basic(process.env.NEO4J_USER, process.env.NEO4J_PASSWORD)
)

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  res.setHeader("Access-Control-Allow-Credentials", "true");
  res.setHeader("Access-Control-Allow-Origin", "https://studio.apollographql.com");
  res.setHeader("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");

  if (req.method === 'OPTIONS') {
    res.end()
    return false
  }

  const neoSchema = new Neo4jGraphQL({ typeDefs: gql``, driver })
  const apolloServer = new ApolloServer({ schema: await neoSchema.getSchema() })

  await apolloServer.start()
  await apolloServer.createHandler({ path: '/api/graphql' })(req, res)
}

export const config = {
  api: {
    bodyParser: false
  }
}
