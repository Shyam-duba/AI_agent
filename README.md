# **AI Agent for Data Extraction and Web Search**<br>
**Introduction**<br>
Welcome to the AI Agent Project! This application is designed to make user life easier for fetching many queries and compute result for specific use. The AI agent processes a dataset (CSV or Google Sheets), performs web searches to retrieve specific information for each entity in a chosen column, and formats the extracted data into a structured output.<br>

 **Key Features:**<br>
    1.Leverages a Large Language Model (LLM) for parsing web search results based on user queries.<br>
    2.Provides a simple and user-friendly dashboard for:<br>
    3.Uploading datasets.<br>
    4.Configuring search queries.<br>
    5.Viewing and downloading structured results.<br>
    6.Supports seamless integration with APIs for efficient data retrieval and processing.<br>
    7.This project demonstrates how AI can be utilized to automate data collection and formatting, saving time and improving accuracy.<br>

How to Run the Application Locally<br>

## **Prerequisites**<br>
Ensure the following are installed on your system:<br>

  Python 3.8 or higher<br>
  Virtual environment tools (venv or virtualenv)<br>
  Required APIs and their credentials (e.g., Google Sheets API, SerpAPI)<br>
  Steps to Run Locally<br>


## Clone the Repository:<br>

  ```git clone https://github.com/your-username/AI_agent.git```
  cd your-repository
Set Up a Virtual Environment:

  python -m venv myenv<br>
  source myenv/bin/activate   # On Windows: myenv\Scripts\activate<br>
Install Dependencies:<br>


```pip install -r requirements.txt```<br>
Set Up Environment Variables: Create a .env file in the project root and add your API keys and configuration details:<br>

makefile an .env file<br>
  SERPAPI_KEY=your-serpapi-key<br>
  GOOGLE_API_KEY=your-google-api-key<br>
Run the Backend:<br>
 ```python app.py```
Run the Frontend (if applicable): Navigate to the frontend directory and install dependencies:


Access the Application: Open your browser and navigate to:


http://localhost:5000  # Or the specified backend/frontend port

# below file shows how to use the Application

[View the PDF](./pdf/userguide.pdf)
# LOOM video
[Watch the Video]([https://www.youtube.com/watch?v=your_video_id](https://youtu.be/gqQVfRz35Qw))
