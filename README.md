# Lateshow API 🎙️

A Flask RESTful API for managing talk show episodes, guests, and their appearances. This backend supports full CRUD functionality, with proper validations and relational data integrity using SQLAlchemy.

---

##  Project Structure

lateshow/ 

├── app/ │ ├── init.py │ ├── models.py │ ├── routes.py ├── seed.py ├── migrations/ ├── config.py ├── README.md


---

##  Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/lateshow.git
cd lateshow
2. Create Virtual Environment & Install Dependencies
bash
Copy code
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
3. Set Up Database & Migrate
bash
Copy code
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
4. Seed the Database
bash
Copy code
python seed.py
5. Run the Server
bash
Copy code
flask run
🔧 Technologies Used
Python 3

Flask

Flask-Migrate

Flask-SQLAlchemy

SQLite3 (can be swapped with PostgreSQL/MySQL)

Postman for testing

# API Endpoints
✅ Get All Episodes
GET /episodes
Returns a list of episodes with guest info and ratings.

✅ Get a Single Episode
GET /episodes/<int:id>
Returns one episode, including guest appearance data.

✅ Delete an Episode
DELETE /episodes/<int:id>
Deletes a specific episode by ID.

✅ Get All Guests
GET /guests
Returns all available guests.

✅ Create a New Appearance
POST /appearances
Request Body (JSON):

json
Copy code
{
  "rating": 8,
  "guest_id": 1,
  "episode_id": 2
}
Returns newly created appearance with guest and episode info.

✅ Validations & Error Handling
Prevents missing fields in POST /appearances.

404 error if GET /episodes/<id> or DELETE /episodes/<id> uses invalid ID.

Returns proper HTTP status codes for each request.
# Author
Hoseah Biwott
GitHub