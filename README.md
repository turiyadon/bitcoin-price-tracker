Bitcoin Price Tracker

This project tracks Bitcoin prices and displays the live price graph. It fetches data from the CoinGecko API, stores the historical price data, and presents it through a beautiful dashboard built with React, Tailwind CSS, and FastAPI.

Features:
- Displays Bitcoin price history in a graph.
- Automatically fetches Bitcoin prices every 5 minutes.
- Provides a manual fetch option for the latest Bitcoin price.
- Responsive design using React and Tailwind CSS.
- Uses FastAPI for the backend.
- Tracks Bitcoin prices with `pdldb` for data management.

Tech Stack:
- Frontend: React, Tailwind CSS
- Backend: FastAPI
- Data Management: `pdldb` (for saving Bitcoin prices)
- Cloud Infrastructure: AWS EC2, GitHub

Setup Instructions:

1. Clone the Repository:
To get started with the project, clone the repository to your local machine or EC2 instance:

git clone https://github.com/turiyadon/bitcoin-price-tracker.git
cd bitcoin-price-tracker

2. Set up the Backend (FastAPI):

Install dependencies:
Create a virtual environment and install the required Python dependencies:

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Run the Backend Server:
uvicorn server:app --host 0.0.0.0 --port 8000

The FastAPI server will now be running and accessible at http://localhost:8000/.

3. Set up the Frontend (React):

Install dependencies:
In the frontend directory, run:
npm install

Start the React App:
npm run dev

Your React app will be running at http://localhost:5173/ (or your EC2 public IP if running on AWS).

4. View the App:
Once both the backend and frontend are running, open a web browser and go to:
- Frontend: http://localhost:5173/ (or your EC2 public IP)
- Backend: http://localhost:8000/ (or your EC2 public IP)

The app will display the live Bitcoin price graph and allow you to manually fetch the latest price.

How the Project Was Created on AWS:

1. AWS EC2 Setup:
   - This project was deployed on an **AWS EC2 instance** running **Ubuntu 22.04.5 LTS**.
   - The EC2 instance is connected to the internet with a **public IP** and **SSH access** using a **.pem key** for secure connection.
   - Ports 5173 (React frontend) and 8000 (FastAPI backend) were **exposed** in the **AWS Security Group** to allow external access.

2. Backend (FastAPI):
   - FastAPI was used to fetch Bitcoin prices from the **CoinGecko API** and serve the data via endpoints.
   - The data is stored and managed using the `pdldb` library, which provides easy data handling and storage. It saves the data in a CSV file.
   - The FastAPI backend was deployed on the EC2 instance and exposed to the public via HTTP on port 8000.

3. Frontend (React):
   - React was used for the frontend, styled using **Tailwind CSS**.
   - The frontend fetches the Bitcoin price data from the FastAPI backend and displays it as a graph.
   - The React app was also deployed on the EC2 instance and exposed to the public via HTTP on port 5173.

4. Security & Network Configuration:
   - The **AWS Security Group** was configured to allow inbound traffic on **ports 80, 8000, and 5173** to expose both the FastAPI backend and React frontend to the internet.
   - **SSH access** was configured with the `.pem` key, allowing secure access to the EC2 instance for setup and deployment.

5. GitHub Repository:
   - The code was committed to a **GitHub repository** for version control.
   - The repository includes detailed instructions on setting up and running the project on AWS EC2.

Acknowledgments:
- `pdldb`: This project uses the `pdldb` package for managing Bitcoin price data. Special thanks to the author 0x6761746F (https://github.com/0x6761746F) for creating this useful tool.
  `pdldb` is used to store historical Bitcoin prices in a CSV file, making it easy to retrieve and visualize the data.

License:
This project is licensed under the MIT License.

Future Improvements:
- Auto-scale graph: Add different time windows for displaying the historical graph (e.g., 1h, 6h, 12h, 1d, 7d).
- Data storage improvements: Explore using a database like PostgreSQL for storing Bitcoin price data instead of a CSV file.
- Frontend Enhancements: Improve the frontend UI to provide better interaction and presentation using React and Tailwind CSS.
