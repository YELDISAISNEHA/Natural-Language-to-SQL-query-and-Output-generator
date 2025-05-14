# Natural-Language-to-SQL-query-and-Output-generator
- Step 1 : Create virtual Environment -> python -m venv myenv
	 Activate virtual environment -> myenv\Scripts\activate
	 Install requirements.txt
	 pip install -r requirements.txt

- Step 2 : Install and Start MySQL Server
	 Win+R -> type services.msc -> Enter -> Right click on Mysql -> Click "Start" (Windows)
	 sudo apt update -> sudo apt install mysql-server -> sudo systemctl start mysql (Linux)

- Step 3 : Install and run Ollama locally in computer and Pull the "mistral" model
	 Go to the official website: https://ollama.com -> Download and install Ollama (Windows)
	 Open cmd -> ollama pull mistral -> ollama run mistral

	 Ollama Install : curl -fsSL https://ollama.com/install.sh | sh (Linux)
	 ollama run mistral 

- Step 4 : Run app.py in VSCode
	 Open the localhost website

- Step 5 : Upload the "sample_data" file

- Step 6 : Ask any question from the question.txt or any other question 

- Step 7 : Result is displayed
