
const typeDefs = `
    type Link {
        id: ID!
        url: String!
        description: String!
    }

    type Sports {
        sport_id: ID!
        sport_abbr: String!
        sport_name: String!
    }

    type Query {
        allLinks: [Link!]!
        whichLink(id: ID!): [Link!]!
        chooseLink(id: ID!): [Link!]!

        sports(season: Int!): [Sports!]!
    }
`;

module.exports = typeDefs;