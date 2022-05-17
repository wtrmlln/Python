HEADLESS_OPTION = True

if HEADLESS_OPTION == True:
    CHROMEOPTIONS_ARGS = ["--no-sandbox", "--headless", "--disable-gpu", "--disable-crash-reporter", "--disable-extensions", 
                        "--disable-in-process-stack-traces", "--disable-logging", "--disable-dev-shm-usage", "--log-level=3"]
elif HEADLESS_OPTION == False:
    CHROMEOPTIONS_ARGS = ["--no-sandbox", "--disable-gpu", "--disable-crash-reporter", "--disable-extensions", 
                        "--disable-in-process-stack-traces", "--disable-logging", "--disable-dev-shm-usage", "--log-level=3"]