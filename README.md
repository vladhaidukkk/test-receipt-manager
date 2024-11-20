# Receipt Manager (Test Task)

**Tech Stack:** Python, FastAPI, SQLAlchemy, Alembic, PostgreSQL, Docker.

## Environment Setup

To get started with the project, you'll need to install [uv](https://docs.astral.sh/uv/). It's also recommended to install [just](https://just.systems/man/en/) for an enhanced development experience, although it's not mandatory.

You won't need to manually create a virtual environment, as `uv` will handle this automatically the first time you run it. Additionally, if you don't have a compatible Python version installed, `uv` will take care of that by installing it within the virtual environment, so you can proceed without any concerns.

## Running the Database

The server requires a running PostgreSQL database to function correctly. You can easily start one using Docker Compose. There's a command available in the `justfile` that you can execute with `just up`, or you can copy it and run manually. This will create a Docker container with PostgreSQL for you.

Before starting the server, you also need to run database migrations to ensure the schema is up to date. You can do this by running `just migrate`, or by copying the command from the `justfile` and executing it manually.

## Running the Server

To run the server, you need to configure the environment. If you used Docker Compose, you can skip creating the `.env` file, as the application will use the settings from `.env.example`. However, if your database connection values differ from those in `.env.example`, please create a `.env` file and overwrite the necessary values.

Finally, to start the server, run `just serve`. If you don't have `just` installed, you can copy the command from the `justfile` and run it manually.

## Working with the Server

Once the server is running, you can access its documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). This documentation allows you to explore and test all available endpoints.

### Authentication

Some endpoints may require an `Authorization-Token`, indicating that they are accessible only to logged-in users. To obtain your token, follow these steps:

**Step 1:** Register or Log In

- If you are a new user, register for an account.
- If you already have an account, log in.

**Step 2:** Obtain Your Token

After registering or logging in, you will receive a temporary access token in the response.

**Step 3:** Use the Token

To access endpoints that require authentication, include your token in the `Authorization-Token` header in the format: `Bearer <token>`.

By following these steps, you will be able to successfully authenticate and interact with the secured endpoints of the server.
