from pprint import pprint

from peewee import IntegrityError
from playhouse.shortcuts import model_to_dict

from capmo.ticket import CapmoTicketClient
from models.ticket import Ticket

from exceptions.ticket import TicketSyncException, TicketCleanException, TicketFetchException


class TicketService:
    def __init__(self, project_id=None):
        self.project_id = project_id
        self.client = CapmoTicketClient()

    def sync(self):
        try:
            gql_data = self.client.get_tickets(self.project_id)
            gql_tickets = gql_data['items']
            gql_ticket_ids = {ticket['id'] for ticket in gql_tickets}

            with Ticket._meta.database.atomic():
                for gql_ticket in gql_tickets:
                    responsible = None
                    if gql_ticket['responsible']:
                        print("DEBUG")
                        print(gql_ticket['responsible']['id'])
                        responsible = gql_ticket['responsible']['id']

                    status = None
                    if gql_ticket['status']:
                        status = gql_ticket['status']['id']

                    ticket, created = Ticket.get_or_create(id=gql_ticket['id'], defaults={
                        'ticketNumber': gql_ticket['ticketNumber'],
                        'ticketKey': gql_ticket['ticketKey'],
                        'name': gql_ticket['name'],
                        'deadline': gql_ticket['deadline'],
                        'createdAt': gql_ticket['createdAt'],
                        'description': gql_ticket['description'],
                        'cost': gql_ticket['cost'],
                        'hasComments': gql_ticket['hasComments'],
                        'type': gql_ticket['type'],
                        'category': gql_ticket['ticketNumber'],
                        'project': gql_ticket['projectId'],
                        'responsible': responsible,
                        'status': status
                    })

                    if not created:
                        ticket.ticketNumber = gql_ticket['ticketNumber']
                        ticket.ticketKey = gql_ticket['ticketKey']
                        ticket.name = gql_ticket['name']
                        ticket.deadline = gql_ticket['deadline']
                        ticket.createdAt = gql_ticket['createdAt']
                        ticket.description = gql_ticket['description']
                        ticket.cost = gql_ticket['cost']
                        ticket.hasComments = gql_ticket['hasComments']
                        ticket.type = gql_ticket['type']
                        ticket.category = gql_ticket['ticketNumber']

                        ticket.responsible = responsible
                        ticket.status = status
                        ticket.project = gql_ticket['projectId']

                        ticket.save()

                # Delete tickets that are not in the GraphQL data anymore
                Ticket.delete().where(
                    (Ticket.project_id == self.project_id) &
                    (Ticket.id.not_in(gql_ticket_ids))
                ).execute()
        except IntegrityError as e:
            raise TicketSyncException(f"Database error occurred: {e}")
        except Exception as e:
            raise TicketSyncException(f"An error occurred: {e}")

    def get_ticket_by_id(self, ticket_id):
        try:
            ticket = Ticket.select().where(Ticket.id == ticket_id).execute()
            return ticket
        except IntegrityError as e:
            raise TicketFetchException(f"Database error occurred: {e}")
        except Exception as e:
            raise TicketFetchException(f"An error occurred: {e}")

    def get_tickets(self):
        try:
            query = Ticket.select()
            if self.project_id is not None:
                # Filter tickets by the project ID if it's provided
                query = query.where(Ticket.project == self.project_id)
            results = [model_to_dict(ticket) for ticket in query]
            return results
        except IntegrityError as e:
            raise TicketFetchException(f"Database error occurred: {e}")
        except Exception as e:
            raise TicketFetchException(f"An error occurred: {e}")

    def create_ticket(self, project_id, name, description, responsible_id, status_id, deadline):
        try:
            ctc = CapmoTicketClient()
            new_ticket = ctc.create_ticket(
                project_id=project_id,
                status_id=status_id,
                responsible_id=responsible_id,
                ticket_name=name,
                ticket_description=description,
                deadline=deadline
            )

            pprint(new_ticket)

            if new_ticket:
                ticket = Ticket()
                ticket.ticketKey = new_ticket['ticketKey']
                ticket.ticketNumber = new_ticket['ticketNumber']
                ticket.name = new_ticket['name']
                ticket.id = new_ticket['id']
                ticket.description = new_ticket['description']
                ticket.deadline = new_ticket['deadline']
                ticket.project = new_ticket['projectId']
                ticket.hasComments = new_ticket['hasComments']
                ticket.cost = new_ticket['cost']

                if 'responsible' in new_ticket and new_ticket['responsible'].get('id'):
                    ticket.responsible = new_ticket['responsible']['id']

                if 'status' in new_ticket and new_ticket['status'].get('id'):
                    ticket.status = new_ticket['status']['id']

                ticket.save(force_insert=True)
                return model_to_dict(ticket)
        except IntegrityError as e:
            raise TicketSyncException(f"Database error occurred: {e}")
        except Exception as e:
            raise TicketSyncException(f"An error occurred: {e}")

    def update_ticket(self, ticket_id, update_data):
        try:
            with Ticket._meta.database.atomic():
                # Fetch the ticket to be updated
                ticket = Ticket.get_by_id(ticket_id)

                # Update the ticket with new data
                for key, value in update_data.items():
                    setattr(ticket, key, value)
                ticket.save()

                return model_to_dict(ticket)
        except Ticket.DoesNotExist:
            raise TicketFetchException(f"Ticket with id {ticket_id} does not exist")
        except IntegrityError as e:
            raise TicketSyncException(f"Database error occurred: {e}")
        except Exception as e:
            raise TicketSyncException(f"An error occurred: {e}")

    def count(self):
        # Modify this method to count based on project_id
        query = Ticket.select()
        if self.project_id is not None:
            query = query.where(Ticket.project == self.project_id)
        return query.count()

    def clean(self):
        try:
            Ticket.delete().execute()
        except IntegrityError as e:
            raise TicketCleanException(f"Database error occurred: {e}")
        except Exception as e:
            raise TicketCleanException(f"An error occurred: {e}")
