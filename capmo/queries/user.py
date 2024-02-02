GET_USER_DETAILS_QUERY = """
        query AppcuesIdentifyQuery {
          result: me {
            id
            email
            firstName
            lastName
            primaryOrganisationMembership {
              id
              organisationId
            }
          }
        }
"""