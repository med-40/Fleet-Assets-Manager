name: Web Application Test

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:

  web-test:

    runs-on: ubuntu-latest

    steps:

      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Check Python syntax
        run: |
          python -m compileall app web

      - name: Check FastAPI import
        run: |
          python -c "from web.main import app; print('FastAPI:', app.title)"

      - name: Create database
        run: |
          python create_database.py

      - name: Start FastAPI server
        run: |
          nohup python -m uvicorn web.main:app \
            --host 127.0.0.1 \
            --port 8000 \
            > web_server.log 2>&1 &

          echo $! > web_server.pid

      - name: Wait for FastAPI
        run: |
          python - <<'PY'
          import time
          import urllib.request

          url = "http://127.0.0.1:8000/health"

          for attempt in range(30):

              try:

                  response = urllib.request.urlopen(
                      url,
                      timeout=2
                  )

                  print("FastAPI HTTP status:", response.status)

                  print(
                      response.read().decode("utf-8")
                  )

                  break

              except Exception as error:

                  print(
                      f"Waiting for FastAPI... "
                      f"{attempt + 1}/30"
                  )

                  print(error)

                  time.sleep(1)

          else:

              print("")
              print("===== FASTAPI LOG =====")

              with open(
                  "web_server.log",
                  "r"
              ) as file:

                  print(file.read())

              raise RuntimeError(
                  "FastAPI server did not start"
              )

          PY

      - name: Test Dashboard
        run: |
          python - <<'PY'
          import urllib.request
          import urllib.error

          url = "http://127.0.0.1:8000/dashboard"

          print("====================================")
          print("TESTING DASHBOARD")
          print("====================================")

          print("Opening:", url)

          try:

              response = urllib.request.urlopen(
                  url,
                  timeout=10
              )

              content = response.read().decode(
                  "utf-8"
              )

              print("")
              print("Dashboard HTTP status:")
              print(response.status)

              print("")
              print("===== DASHBOARD RESPONSE =====")
              print(content)
              print("===== END DASHBOARD RESPONSE =====")

              if response.status != 200:
                  raise RuntimeError(
                      "Dashboard returned invalid status"
                  )

              print("")
              print("Dashboard HTTP test OK")

          except urllib.error.HTTPError as error:

              print("")
              print("====================================")
              print("DASHBOARD HTTP ERROR")
              print("====================================")

              print("HTTP status:", error.code)

              try:

                  error_body = error.read().decode(
                      "utf-8",
                      errors="replace"
                  )

                  print("")
                  print("===== ERROR RESPONSE =====")
                  print(error_body)
                  print("===== END ERROR RESPONSE =====")

              except Exception as read_error:

                  print(
                      "Could not read error response:"
                  )

                  print(read_error)

              print("")
              print("====================================")
              print("===== FASTAPI SERVER LOG =====")
              print("====================================")

              try:

                  with open(
                      "web_server.log",
                      "r"
                  ) as file:

                      print(file.read())

              except Exception as log_error:

                  print(
                      "Could not read FastAPI log:"
                  )

                  print(log_error)

              print("====================================")
              print("===== END FASTAPI SERVER LOG =====")
              print("====================================")

              raise

          except Exception as error:

              print("")
              print("Dashboard test error:")
              print(error)

              print("")
              print("===== FASTAPI SERVER LOG =====")

              try:

                  with open(
                      "web_server.log",
                      "r"
                  ) as file:

                      print(file.read())

              except Exception as log_error:

                  print(log_error)

              raise

          PY

      - name: Test Equipment Types
        run: |
          python - <<'PY'
          import urllib.request

          url = "http://127.0.0.1:8000/equipment-types"

          print("====================================")
          print("TESTING EQUIPMENT TYPES")
          print("====================================")

          response = urllib.request.urlopen(
              url,
              timeout=10
          )

          print("HTTP status:", response.status)

          print(
              response.read().decode("utf-8")
          )

          print("Equipment Types HTTP test OK")

          PY

      - name: Test Drivers
        run: |
          python - <<'PY'
          import urllib.request

          url = "http://127.0.0.1:8000/drivers"

          print("====================================")
          print("TESTING DRIVERS")
          print("====================================")

          response = urllib.request.urlopen(
              url,
              timeout=10
          )

          print("HTTP status:", response.status)

          print(
              response.read().decode("utf-8")
          )

          print("Drivers HTTP test OK")

          PY

      - name: Show FastAPI log
        if: always()
        run: |
          echo "===================================="
          echo "===== FASTAPI SERVER LOG ====="
          echo "===================================="

          if [ -f web_server.log ]; then
              cat web_server.log
          else
              echo "web_server.log does not exist"
          fi

          echo "===================================="
          echo "===== END FASTAPI SERVER LOG ====="
          echo "===================================="

      - name: Stop FastAPI
        if: always()
        run: |
          if [ -f web_server.pid ]; then
              kill "$(cat web_server.pid)" || true
          fi
