from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}


events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]


def find_event(event_id: int):
    """Return the Event object with matching id, or None."""
    for event in events:
        if event.id == event_id:
            return event
    return None


def next_event_id() -> int:
    """Generate the next id."""
    if not events:
        return 1
    return max(e.id for e in events) + 1


# GET / - Welcome message
@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to the Event Management API!"}), 200


# GET /events - Return all events
@app.route("/events", methods=["GET"])
def get_events():
    return jsonify([e.to_dict() for e in events]), 200


# POST /events - Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json(silent=True)

    # Validate input
    if not data or "title" not in data:
        return jsonify({"error": "Missing required field: title"}), 400

    title = str(data["title"]).strip()
    if not title:
        return jsonify({"error": "Title cannot be empty"}), 400

    new_event = Event(next_event_id(), title)
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# PATCH /events/<id> - Update the title of an event
@app.route("/events/<int:id>", methods=["PATCH"])
def update_event(id):
    event = find_event(id)
    if event is None:
        return jsonify({"error": f"Event with id {id} not found"}), 404

    data = request.get_json(silent=True)
    if not data or "title" not in data:
        return jsonify({"error": "Missing required field: title"}), 400

    title = str(data["title"]).strip()
    if not title:
        return jsonify({"error": "Title cannot be empty"}), 400

    event.title = title
    return jsonify(event.to_dict()), 200


# DELETE /events/<id> - Remove an event from the list
@app.route("/events/<int:id>", methods=["DELETE"])
def delete_event(id):
    event = find_event(id)
    if event is None:
        return jsonify({"error": f"Event with id {id} not found"}), 404

    events.remove(event)

    # Lab expects 204 No Content
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)

 