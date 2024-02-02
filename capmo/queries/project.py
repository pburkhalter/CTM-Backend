GET_PROJECTS_QUERY = """
        query ProjectsPaginated($input: OwnProjectPaginatedInput!) {
          result: ownProjects(input: $input) {
            after
            count
            total
            items {
              id
              name
              isArchived
            }
          }
        }
"""

GET_PROJECT_ATTRIBUTES_QUERY = """
        query ProjectAttributesQuery($input: projectInput!) {
          result: project(input: $input) {
            ticketStatuses {
              id
              name
            }
            members {
              id
              user {
                id
                fullName
                email
              }
            }
          }
        }
"""

GET_PROJECT_MEMBERS_QUERY = """
    query MemberListQuery($input: membershipsInput!) {
        result: memberships(input: $input) {
            id
            createdAt
            user {
                id
                fullName
                signedUp
                email
                __typename
            }
            roleEnum
            participatingCompany {
                name
                __typename
            }
            hasFullCdePermission
            __typename
        }
    }
"""

GET_PROJECT_SETTINGS_QUERY = """
    query ProjectSettingsQuery($projectInput: projectInput!) {
        result: project(input: $projectInput) {
            id
            name
            client
            projectVolume
            address
            latitude
            longitude
            startDate
            projectKey
            isArchived
            isTemplate
            __typename
        }
    }
"""
