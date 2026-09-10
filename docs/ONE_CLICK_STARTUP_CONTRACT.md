# One-Click Startup Contract

`run_app.bat` is mandatory. A normal Windows user should be able to double-click it to:
1. detect Python;
2. create `.venv`;
3. install/update `requirements.txt` only when required;
4. initialize directories/config;
5. start FastAPI;
6. verify `/health`;
7. install npm packages if the web UI needs them;
8. start Next.js;
9. open the working UI;
10. log startup failures to `logs/startup.log`.

System runtimes such as Python and Node are prerequisites and are not silently installed system-wide.
