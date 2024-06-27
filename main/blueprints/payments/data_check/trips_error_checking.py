

def trips_error_checking(ticket_type, ticket_id):
  errors_list = []

  # Check ticket type first
  if not isinstance(ticket_type, str):
    errors_list.append('The ticket type: {} must be a string value'.format(ticket_type))

  if ticket_type not in ("round_trip", "one_way"):
    errors_list.append('The ticket type: {} is not "round_trip" or "one_way"'.format(ticket_type))

  # Check ticket ID
  if not ticket_id.isdigit() or int(ticket_id) < 1:
    errors_list.append("The ticket id: {} is invalid. It must be a number greater than or equal to 1".format(ticket_id))

  return errors_list