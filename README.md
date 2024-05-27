# Git and More

gitandMore is a Python tool designed to fuzz subdomains for accessible .git files. It helps identify potential security risks by checking if subdomains expose sensitive Git repository information.

## Features

- Fuzz subdomains for accessible .git files
- Multi-threaded for faster scanning
- Customizable number of threads
- Color-coded output for easy identification
- Save results to a file

## Usage

1. **Clone the Repository:**

    ```bash
    https://github.com/k2ito/gitandMore.git
    ```

2. **Navigate to the Directory:**

    ```bash
    cd gitandMore
    ```

3. **Install Dependencies:**

    ```bash
    pip3 install -r requirements.txt
    ```

4. **Run the Tool:**
    ```python3
    python3 gitandMore.py -l subdomains.txt
    ```
    
    ```bash
    chmod +x gitandMore.py
    ./gitandMore.py -l subdomains.txt
    ```

    Replace `subdomains.txt` with the file containing your list of subdomains.

    Optional flags:
    - `-o, --output`: Specify the output file (default: accessible_git_files.txt).
    - `-t, --threads`: Number of threads to use (default: 10).

## Example

```bash
./gitandMore.py -l subdomains.txt
