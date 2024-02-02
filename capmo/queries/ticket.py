GET_TICKETS_QUERY = """
        query TicketsPaginatedQuery($input: TicketsPageInput!) {
          result: ticketsV2(input: $input) {
            count
            total
            items {
              id
              projectId
              ticketNumber
              ticketKey
              name
              deadline
              createdAt
              description
              cost
              hasComments
              status {
                id
                name
              }
              type {
                id
                name
              }
              category {
                id
                name
              }
              responsible {
                id
                fullName: name
              }
            }
          }
        }
"""

CREATE_TICKET_QUERY = """
        mutation TicketDetailCreateTicketMutation($input: createTicketInput!) {
          result: createTicket(input: $input) {
            id
            name
            description
            ticketKey
            category {
              id
              name
            }
            ticketNumber
            projectId
            typeId
            type {
              id
              name
            }
            status {
              id
              name
            }
            createdAt
            updatedAt
            deadline
            responsible {
              email
              fullName
              firstName
              lastName
              id
            }
            company {
              name
            }
            attachments {
              id
              creator {
                id
                fullName
              }
              createdAt
              file {
                id
                type
                downloadUrl
                signedUrl
                imageUrl
                name
              }
              originalName
            }
            hasComments
            cost
          }
        }
"""

UPDATE_TICKET_QUERY = """
        mutation TicketDetailUpdateTicketMutation($input: updateTicketInput!) {
          result: updateTicket(input: $input) {
            id
            name
            description
            ticketKey
            categoryId
            category {
              id
              name
            }
            typeId
            type {
              id
              name
            }
            projectId
            ticketNumber
            hasComments
            statusId
            status {
              id
              name
            }
            createdAt
            updatedAt
            deadline
            responsibleId
            responsible {
              id
              fullName
              firstName
              lastName
              email
            }
            attachments {
              id
              creator {
                id
                fullName
              }
              createdAt
              file {
                id
                type
                downloadUrl
                signedUrl
                imageUrl
                name
              }
              originalName
            }
            cost
          }
        }
"""

UPDATE_TICKET_STATUS_QUERY = """
        mutation TicketDetailUpdateTicketMutation($ticketId: ID!, $statusId: ID!) {
          result: updateTicket(input: { ticketId: $ticketId, statusId: $statusId }) {
            id
            statusId
            __typename
          }
        }
"""

DELETE_TICKET_QUERY = """
        mutation ArchiveTicketMutation($input: archiveTicketInput!) {
          result: archiveTicket(input: $input) {
            id
            __typename
          }
        }
"""